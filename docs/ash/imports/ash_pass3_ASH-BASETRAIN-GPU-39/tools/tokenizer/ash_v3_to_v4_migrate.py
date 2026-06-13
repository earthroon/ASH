#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import os
from dataclasses import dataclass
from pathlib import Path
import random
import shutil
import sys
import tomllib
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

try:
    import numpy as np
except Exception as exc:  # pragma: no cover
    raise SystemExit("numpy is required for this draft migration script") from exc

try:
    from safetensors.numpy import load_file, save_file
except Exception:
    load_file = None
    save_file = None

EMBED_KEYS = [
    "model.embed_tokens.weight",
    "tok_embeddings.weight",
    "embed_tokens.weight",
]
LM_HEAD_KEYS = [
    "lm_head.weight",
    "output.weight",
]

SPECIAL_EXPECTED = {
    "<pad>": 0,
    "<bos>": 1,
    "<eos>": 2,
    "<unk>": 3,
}

GROUP_DONORS = {
    "identity": ["task", "language", "control"],
    "bridge": ["control"],
    "guard": ["control"],
    "style": ["task", "control"],
    "signal": ["control", "cue"],
    "task": ["task"],
    "language": ["language"],
    "glossary": ["glossary"],
    "tm": ["tm"],
    "cue": ["cue"],
    "control": ["control"],
    "core": ["core"],
}


@dataclass
class ManifestToken:
    token: str
    id: int
    score: Optional[float]
    is_reserved: bool
    group: Optional[str] = None


@dataclass
class ManifestBundle:
    path: Path
    raw: dict
    tokens_by_id: Dict[int, ManifestToken]
    tokens_by_str: Dict[str, ManifestToken]
    reserved_by_token: Dict[str, dict]


@dataclass
class ResizeReport:
    source_checkpoint: str
    source_manifest: str
    target_manifest: str
    source_rows: int
    target_rows: int
    hidden_size: int
    embedding_key: str
    lm_head_key: str
    copied_tokens: int
    initialized_tokens: int
    dropped_source_tokens: int
    source_manifest_vocab_entries: int
    target_manifest_vocab_entries: int
    preserved_reserved_ok: bool
    note: str
    copied_examples: List[str]
    initialized_examples: List[str]
    dropped_examples: List[str]

    def to_json(self) -> dict:
        return {
            "source_checkpoint": self.source_checkpoint,
            "source_manifest": self.source_manifest,
            "target_manifest": self.target_manifest,
            "source_rows": self.source_rows,
            "target_rows": self.target_rows,
            "hidden_size": self.hidden_size,
            "embedding_key": self.embedding_key,
            "lm_head_key": self.lm_head_key,
            "copied_tokens": self.copied_tokens,
            "initialized_tokens": self.initialized_tokens,
            "dropped_source_tokens": self.dropped_source_tokens,
            "source_manifest_vocab_entries": self.source_manifest_vocab_entries,
            "target_manifest_vocab_entries": self.target_manifest_vocab_entries,
            "preserved_reserved_ok": self.preserved_reserved_ok,
            "note": self.note,
            "copied_examples": self.copied_examples,
            "initialized_examples": self.initialized_examples,
            "dropped_examples": self.dropped_examples,
        }


def load_toml(path: Path) -> dict:
    with path.open("rb") as f:
        return tomllib.load(f)


def load_manifest(path: Path) -> ManifestBundle:
    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    reserved_map: Dict[str, dict] = {}
    for item in raw.get("reserved_tokens", []):
        reserved_map[item["token"]] = item

    tokens_by_id: Dict[int, ManifestToken] = {}
    tokens_by_str: Dict[str, ManifestToken] = {}
    for item in raw.get("vocab", []):
        token = ManifestToken(
            token=item["token"],
            id=int(item["id"]),
            score=item.get("score"),
            is_reserved=bool(item.get("is_reserved", False)),
            group=reserved_map.get(item["token"], {}).get("group"),
        )
        tokens_by_id[token.id] = token
        tokens_by_str[token.token] = token

    return ManifestBundle(
        path=path,
        raw=raw,
        tokens_by_id=tokens_by_id,
        tokens_by_str=tokens_by_str,
        reserved_by_token=reserved_map,
    )


def manifest_from_reserved_only(path: Path) -> ManifestBundle:
    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)
    reserved_map: Dict[str, dict] = {}
    tokens_by_id: Dict[int, ManifestToken] = {}
    tokens_by_str: Dict[str, ManifestToken] = {}
    for item in raw.get("reserved_tokens", []):
        reserved_map[item["token"]] = item
        tok = ManifestToken(
            token=item["token"],
            id=int(item["id"]),
            score=None,
            is_reserved=True,
            group=item.get("group"),
        )
        tokens_by_id[tok.id] = tok
        tokens_by_str[tok.token] = tok
    return ManifestBundle(path=path, raw=raw, tokens_by_id=tokens_by_id, tokens_by_str=tokens_by_str, reserved_by_token=reserved_map)


def find_tensor_key(tensors: Dict[str, np.ndarray], candidates: Sequence[str]) -> str:
    for key in candidates:
        if key in tensors:
            return key
    raise KeyError(f"none of the tensor keys were found: {candidates}")


def validate_special_tokens(bundle: ManifestBundle) -> None:
    for token, expected_id in SPECIAL_EXPECTED.items():
        found = bundle.tokens_by_str.get(token)
        if found is None:
            raise ValueError(f"manifest {bundle.path} missing special token {token}")
        if found.id != expected_id:
            raise ValueError(
                f"manifest {bundle.path} special token {token} has id {found.id}, expected {expected_id}"
            )


def validate_preserved_reserved(v3: ManifestBundle, v4: ManifestBundle, preserved_max_id: int = 31) -> None:
    for i in range(preserved_max_id + 1):
        a = v3.tokens_by_id.get(i)
        b = v4.tokens_by_id.get(i)
        if a is None or b is None:
            raise ValueError(f"reserved preservation check failed at id {i}: token missing")
        if a.token != b.token:
            raise ValueError(f"reserved preservation check failed at id {i}: {a.token!r} != {b.token!r}")


def infer_group(token: ManifestToken) -> str:
    if token.group:
        return token.group
    if token.is_reserved:
        return "reserved"
    return "general"


def build_group_centroids(
    source_rows: np.ndarray,
    source_manifest: ManifestBundle,
    source_row_limit: int,
) -> Dict[str, np.ndarray]:
    buckets: Dict[str, List[np.ndarray]] = {}
    for token in source_manifest.tokens_by_id.values():
        if token.id >= source_row_limit:
            continue
        group = infer_group(token)
        buckets.setdefault(group, []).append(source_rows[token.id])

    centroids: Dict[str, np.ndarray] = {}
    for group, rows in buckets.items():
        centroids[group] = np.stack(rows, axis=0).mean(axis=0)

    copied_rows = [source_rows[i] for i in range(source_row_limit)]
    centroids["__global__"] = np.stack(copied_rows, axis=0).mean(axis=0)
    return centroids


def donor_centroid_for_group(group: str, centroids: Dict[str, np.ndarray]) -> np.ndarray:
    donors = GROUP_DONORS.get(group, [])
    donor_rows = [centroids[g] for g in donors if g in centroids]
    if donor_rows:
        return np.stack(donor_rows, axis=0).mean(axis=0)
    return centroids["__global__"]


def noise_like(base: np.ndarray, sigma: float, scale: float, rng: np.random.Generator) -> np.ndarray:
    if sigma <= 0.0 or scale <= 0.0:
        return np.zeros_like(base)
    return rng.normal(loc=0.0, scale=sigma * scale, size=base.shape).astype(base.dtype)


def init_row(
    token: ManifestToken,
    centroids: Dict[str, np.ndarray],
    sigma: float,
    init_scale: float,
    rng: np.random.Generator,
) -> np.ndarray:
    group = infer_group(token)
    if token.is_reserved:
        base = donor_centroid_for_group(group, centroids)
    else:
        base = centroids["__global__"]
    return base + noise_like(base, sigma=sigma, scale=init_scale, rng=rng)


def resize_tensor_by_token_remap(
    src_tensor: np.ndarray,
    source_manifest: ManifestBundle,
    target_manifest: ManifestBundle,
    target_rows: int,
    init_scale: float,
    seed: int,
) -> Tuple[np.ndarray, int, int, List[str], List[str], List[str]]:
    if src_tensor.ndim != 2:
        raise ValueError(f"expected 2D tensor, got shape {src_tensor.shape}")

    source_row_limit = int(src_tensor.shape[0])
    hidden_size = int(src_tensor.shape[1])
    out = np.zeros((target_rows, hidden_size), dtype=src_tensor.dtype)
    rng = np.random.default_rng(seed)
    sigma = float(src_tensor.astype(np.float32).std())

    centroids = build_group_centroids(src_tensor, source_manifest, source_row_limit)

    copied = 0
    initialized = 0
    copied_examples: List[str] = []
    initialized_examples: List[str] = []

    for new_id in range(target_rows):
        target_token = target_manifest.tokens_by_id.get(new_id)
        if target_token is None:
            raise ValueError(
                f"target manifest {target_manifest.path} missing token entry for row id {new_id}; full V4 vocab is required"
            )

        src = source_manifest.tokens_by_str.get(target_token.token)
        if src is not None and src.id < source_row_limit:
            out[new_id] = src_tensor[src.id]
            copied += 1
            if len(copied_examples) < 16:
                copied_examples.append(f"{target_token.token}@{src.id}->{new_id}")
        else:
            out[new_id] = init_row(target_token, centroids, sigma=sigma, init_scale=init_scale, rng=rng)
            initialized += 1
            if len(initialized_examples) < 16:
                initialized_examples.append(f"{target_token.token}@{new_id}:{infer_group(target_token)}")

    dropped_examples: List[str] = []
    dropped = 0
    for src_id in range(source_row_limit):
        src_token = source_manifest.tokens_by_id.get(src_id)
        if src_token is None:
            continue
        tgt = target_manifest.tokens_by_str.get(src_token.token)
        if tgt is None or tgt.id >= target_rows:
            dropped += 1
            if len(dropped_examples) < 16:
                dropped_examples.append(f"{src_token.token}@{src_id}")

    return out, copied, initialized, copied_examples, initialized_examples, dropped_examples


def maybe_copy_switch_files(args: argparse.Namespace, out_dir: Path) -> None:
    if not args.copy_switch_files:
        return
    out_dir.mkdir(parents=True, exist_ok=True)
    for p in [args.target_manifest, args.target_model_spec, args.target_runtime_profile]:
        dest = out_dir / Path(p).name
        shutil.copy2(p, dest)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="ASH V3 -> V4 token-string remap migration draft")
    p.add_argument("--source-checkpoint", required=True)
    p.add_argument("--source-manifest", required=True)
    p.add_argument("--target-manifest", required=True)
    p.add_argument("--source-model-spec", required=True)
    p.add_argument("--target-model-spec", required=True)
    p.add_argument("--target-runtime-profile", required=True)
    p.add_argument("--out-checkpoint", required=True)
    p.add_argument("--out-report", required=True)
    p.add_argument("--copy-switch-files", action="store_true")
    p.add_argument("--reserved-only-dry-run", action="store_true", help="allow a reserved-only target manifest scaffold with no full vocab array")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--init-scale", type=float, default=0.01)
    p.add_argument("--seed", type=int, default=42)
    return p.parse_args()


def main() -> int:
    args = parse_args()

    src_ckpt_path = Path(args.source_checkpoint)
    src_manifest_path = Path(args.source_manifest)
    tgt_manifest_path = Path(args.target_manifest)
    src_model_spec_path = Path(args.source_model_spec)
    tgt_model_spec_path = Path(args.target_model_spec)
    tgt_runtime_profile_path = Path(args.target_runtime_profile)
    out_ckpt_path = Path(args.out_checkpoint)
    out_report_path = Path(args.out_report)

    source_manifest = load_manifest(src_manifest_path)
    if args.reserved_only_dry_run:
        target_manifest = manifest_from_reserved_only(tgt_manifest_path)
    else:
        target_manifest = load_manifest(tgt_manifest_path)
        if not target_manifest.tokens_by_id:
            raise SystemExit(
                "target manifest has no vocab array; use --reserved-only-dry-run only for scaffold validation, not full resize"
            )

    validate_special_tokens(source_manifest)
    validate_special_tokens(target_manifest)
    validate_preserved_reserved(source_manifest, target_manifest, preserved_max_id=31)

    src_spec = load_toml(src_model_spec_path)
    tgt_spec = load_toml(tgt_model_spec_path)
    _tgt_runtime = load_toml(tgt_runtime_profile_path)

    target_rows = int(tgt_spec["dimensions"]["vocab_size"])

    if load_file is None or save_file is None:
        raise SystemExit(
            "safetensors is required for checkpoint read/write in this draft script. Install with: pip install safetensors"
        )

    tensors = load_file(str(src_ckpt_path))
    embedding_key = find_tensor_key(tensors, EMBED_KEYS)
    lm_head_key = find_tensor_key(tensors, LM_HEAD_KEYS)

    embedding = tensors[embedding_key]
    lm_head = tensors[lm_head_key]
    if embedding.ndim != 2 or lm_head.ndim != 2:
        raise SystemExit("embedding and lm_head must both be rank-2 tensors")
    if embedding.shape[1] != lm_head.shape[1]:
        raise SystemExit(
            f"hidden-size mismatch: embedding {embedding.shape}, lm_head {lm_head.shape}"
        )

    source_rows = int(embedding.shape[0])
    hidden_size = int(embedding.shape[1])

    if args.reserved_only_dry_run:
        report = ResizeReport(
            source_checkpoint=str(src_ckpt_path),
            source_manifest=str(src_manifest_path),
            target_manifest=str(tgt_manifest_path),
            source_rows=source_rows,
            target_rows=target_rows,
            hidden_size=hidden_size,
            embedding_key=embedding_key,
            lm_head_key=lm_head_key,
            copied_tokens=0,
            initialized_tokens=0,
            dropped_source_tokens=0,
            source_manifest_vocab_entries=len(source_manifest.tokens_by_id),
            target_manifest_vocab_entries=len(target_manifest.tokens_by_id),
            preserved_reserved_ok=True,
            note="reserved-only dry-run: target manifest scaffold has no full vocab array, so no full checkpoint remap was performed",
            copied_examples=[],
            initialized_examples=[],
            dropped_examples=[],
        )
        out_report_path.parent.mkdir(parents=True, exist_ok=True)
        out_report_path.write_text(json.dumps(report.to_json(), ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(report.to_json(), ensure_ascii=False, indent=2))
        return 0

    resized_embedding, emb_copied, emb_init, emb_copied_ex, emb_init_ex, emb_dropped_ex = resize_tensor_by_token_remap(
        embedding, source_manifest, target_manifest, target_rows=target_rows, init_scale=args.init_scale, seed=args.seed
    )
    resized_lm_head, lm_copied, lm_init, _, _, _ = resize_tensor_by_token_remap(
        lm_head, source_manifest, target_manifest, target_rows=target_rows, init_scale=args.init_scale, seed=args.seed + 1
    )

    out_tensors = dict(tensors)
    out_tensors[embedding_key] = resized_embedding
    out_tensors[lm_head_key] = resized_lm_head

    report = ResizeReport(
        source_checkpoint=str(src_ckpt_path),
        source_manifest=str(src_manifest_path),
        target_manifest=str(tgt_manifest_path),
        source_rows=source_rows,
        target_rows=target_rows,
        hidden_size=hidden_size,
        embedding_key=embedding_key,
        lm_head_key=lm_head_key,
        copied_tokens=min(emb_copied, lm_copied),
        initialized_tokens=max(emb_init, lm_init),
        dropped_source_tokens=len(emb_dropped_ex),
        source_manifest_vocab_entries=len(source_manifest.tokens_by_id),
        target_manifest_vocab_entries=len(target_manifest.tokens_by_id),
        preserved_reserved_ok=True,
        note=(
            "token-string remap completed. Rows were copied by token equality, not raw id. "
            "Initialized rows used donor-group warm start + small gaussian noise."
        ),
        copied_examples=emb_copied_ex,
        initialized_examples=emb_init_ex,
        dropped_examples=emb_dropped_ex,
    )

    out_report_path.parent.mkdir(parents=True, exist_ok=True)
    out_report_path.write_text(json.dumps(report.to_json(), ensure_ascii=False, indent=2), encoding="utf-8")

    if not args.dry_run:
        out_ckpt_path.parent.mkdir(parents=True, exist_ok=True)
        save_file(out_tensors, str(out_ckpt_path))
        maybe_copy_switch_files(args, out_ckpt_path.parent)

    print(json.dumps(report.to_json(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
