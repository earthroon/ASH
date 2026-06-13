#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

BYTE_RE = re.compile(r"^<byte:([0-9A-F]{2})>$")


@dataclass
class CandidateEntry:
    token: str
    score: Optional[float]
    source: str
    order: int


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def dump_json(data: Any, path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def sha256_json(data: Any) -> str:
    blob = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(blob).hexdigest()


def is_byte_token(token: str) -> bool:
    return BYTE_RE.match(token) is not None


def validate_reserved_tokens(reserved_tokens: List[Dict[str, Any]]) -> None:
    ids = [int(item["id"]) for item in reserved_tokens]
    tokens = [str(item["token"]) for item in reserved_tokens]
    if len(ids) != len(set(ids)):
        raise ValueError("reserved_tokens contains duplicate ids")
    if len(tokens) != len(set(tokens)):
        raise ValueError("reserved_tokens contains duplicate token strings")
    expected = list(range(len(reserved_tokens)))
    if ids != expected:
        raise ValueError(f"reserved token ids must be contiguous from 0..{len(reserved_tokens)-1}, got first mismatch around {ids[:10]}")



def load_candidates_from_manifest(path: Path) -> List[CandidateEntry]:
    data = load_json(path)
    if "vocab" not in data or not isinstance(data["vocab"], list):
        raise ValueError(f"candidate manifest {path} missing vocab list")
    out: List[CandidateEntry] = []
    for idx, item in enumerate(data["vocab"]):
        token = str(item["token"])
        score = item.get("score")
        if score is not None:
            score = float(score)
        out.append(CandidateEntry(token=token, score=score, source=f"manifest:{path.name}", order=idx))
    return out


def load_candidates_from_json(path: Path) -> List[CandidateEntry]:
    data = load_json(path)
    out: List[CandidateEntry] = []

    def push(token: str, score: Optional[float], idx: int) -> None:
        out.append(CandidateEntry(token=token, score=score, source=f"json:{path.name}", order=idx))

    if isinstance(data, list):
        for idx, item in enumerate(data):
            if isinstance(item, str):
                push(item, None, idx)
            elif isinstance(item, dict):
                token = str(item["token"])
                score = item.get("score")
                push(token, None if score is None else float(score), idx)
            else:
                raise ValueError(f"unsupported candidate item in {path}: {type(item).__name__}")
        return out

    if isinstance(data, dict):
        # Hugging Face tokenizer.json / tokenizers export handling.
        model = data.get("model")
        if isinstance(model, dict) and "vocab" in model:
            vocab = model["vocab"]
            if isinstance(vocab, dict):
                # BPE-style dict token->id. Re-sort by id for deterministic order.
                items = sorted(vocab.items(), key=lambda kv: int(kv[1]))
                for idx, (token, _id) in enumerate(items):
                    push(str(token), None, idx)
                return out
            if isinstance(vocab, list):
                # sentencepiece-ish [[token, score], ...]
                for idx, item in enumerate(vocab):
                    if isinstance(item, list) and len(item) >= 1:
                        token = str(item[0])
                        score = float(item[1]) if len(item) > 1 and item[1] is not None else None
                        push(token, score, idx)
                    elif isinstance(item, dict):
                        token = str(item["token"])
                        score = item.get("score")
                        push(token, None if score is None else float(score), idx)
                    else:
                        raise ValueError(f"unsupported model.vocab item in {path}: {item!r}")
                return out

    raise ValueError(f"unsupported candidate json format: {path}")



def load_candidates_from_tsv(path: Path) -> List[CandidateEntry]:
    out: List[CandidateEntry] = []
    with path.open("r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        for idx, row in enumerate(reader):
            if not row:
                continue
            token = row[0]
            score: Optional[float] = None
            if len(row) >= 2 and row[1] != "":
                score = float(row[1])
            out.append(CandidateEntry(token=token, score=score, source=f"tsv:{path.name}", order=idx))
    return out



def load_candidates_from_jsonl(path: Path) -> List[CandidateEntry]:
    out: List[CandidateEntry] = []
    with path.open("r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)
            token = str(item["token"])
            score = item.get("score")
            if score is not None:
                score = float(score)
            out.append(CandidateEntry(token=token, score=score, source=f"jsonl:{path.name}", order=idx))
    return out



def merge_unique_candidates(candidates: Iterable[CandidateEntry], prefer_higher_score: bool) -> Tuple[List[CandidateEntry], Dict[str, int]]:
    merged: Dict[str, CandidateEntry] = {}
    dedupe_stats = {
        "input_candidates": 0,
        "duplicate_candidates": 0,
        "score_promotions": 0,
    }
    for item in candidates:
        dedupe_stats["input_candidates"] += 1
        prev = merged.get(item.token)
        if prev is None:
            merged[item.token] = item
            continue
        dedupe_stats["duplicate_candidates"] += 1
        replace = False
        if prefer_higher_score:
            prev_score = float("-inf") if prev.score is None else prev.score
            next_score = float("-inf") if item.score is None else item.score
            if next_score > prev_score:
                replace = True
                dedupe_stats["score_promotions"] += 1
        if not replace and item.order < prev.order:
            replace = True
        if replace:
            merged[item.token] = item
    ordered = sorted(merged.values(), key=lambda c: (c.order, c.token))
    return ordered, dedupe_stats



def coerce_special_tokens(special_tokens: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    result: Dict[str, Dict[str, Any]] = {}
    for key, value in special_tokens.items():
        if isinstance(value, dict):
            result[key] = {"token": str(value["token"]), "id": int(value["id"])}
        else:
            raise ValueError(f"draft special_tokens[{key}] must be object with token/id")
    return result



def build_manifest(
    source_manifest: Dict[str, Any],
    target_draft: Dict[str, Any],
    ordered_candidates: List[CandidateEntry],
    *,
    allow_shortfall: bool,
    manifest_id: str,
    imported_from: Optional[str],
    imported_format: Optional[str],
    default_top_k: Optional[int],
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    reserved_tokens = list(target_draft["reserved_tokens"])
    validate_reserved_tokens(reserved_tokens)
    reserved_token_set = {str(item["token"]) for item in reserved_tokens}
    source_vocab = list(source_manifest["vocab"])

    source_byte_entries = [entry for entry in source_vocab if is_byte_token(str(entry["token"]))]
    source_nonbyte_entries = [
        entry for entry in source_vocab
        if not bool(entry.get("is_reserved")) and not is_byte_token(str(entry["token"]))
    ]
    byte_count = len(source_byte_entries)

    target_vocab_size = int(target_draft["trainer"]["vocab_size"])
    reserved_count = len(reserved_tokens)
    target_nonreserved = target_vocab_size - reserved_count
    target_nonbyte_slots = target_nonreserved - byte_count
    if target_nonbyte_slots < 0:
        raise ValueError(
            f"target vocab too small: target_nonreserved={target_nonreserved} but byte_count={byte_count}"
        )

    external_nonbyte: List[CandidateEntry] = []
    external_byte: List[CandidateEntry] = []
    for item in ordered_candidates:
        if item.token in reserved_token_set:
            continue
        if is_byte_token(item.token):
            external_byte.append(item)
        else:
            external_nonbyte.append(item)

    source_nonbyte_candidates = [
        CandidateEntry(
            token=str(entry["token"]),
            score=None if entry.get("score") is None else float(entry["score"]),
            source="source_manifest",
            order=idx,
        )
        for idx, entry in enumerate(source_nonbyte_entries)
    ]

    selected_nonbyte: List[CandidateEntry] = []
    seen: set[str] = set()

    def push_items(items: Sequence[CandidateEntry]) -> None:
        for item in items:
            if item.token in seen:
                continue
            seen.add(item.token)
            selected_nonbyte.append(item)
            if len(selected_nonbyte) >= target_nonbyte_slots:
                break

    push_items(external_nonbyte)
    if len(selected_nonbyte) < target_nonbyte_slots:
        push_items(source_nonbyte_candidates)

    shortfall = target_nonbyte_slots - len(selected_nonbyte)
    if shortfall > 0 and not allow_shortfall:
        raise ValueError(
            f"insufficient non-byte tokens for V4 manifest: need {target_nonbyte_slots}, got {len(selected_nonbyte)} (shortfall={shortfall})"
        )

    # Reuse the source byte block order unless external candidates explicitly replace by token.
    byte_by_token: Dict[str, CandidateEntry] = {
        item.token: CandidateEntry(token=item.token, score=item.score, source=item.source, order=item.order)
        for item in external_byte
    }
    selected_bytes: List[CandidateEntry] = []
    for idx, entry in enumerate(source_byte_entries):
        token = str(entry["token"])
        cand = byte_by_token.get(token)
        if cand is not None:
            selected_bytes.append(cand)
        else:
            selected_bytes.append(
                CandidateEntry(
                    token=token,
                    score=None if entry.get("score") is None else float(entry["score"]),
                    source="source_manifest",
                    order=idx,
                )
            )

    vocab_entries: List[Dict[str, Any]] = []
    for item in reserved_tokens:
        vocab_entries.append({
            "token": str(item["token"]),
            "id": int(item["id"]),
            "score": None,
            "is_reserved": True,
        })

    next_id = reserved_count
    for item in selected_nonbyte:
        vocab_entries.append({
            "token": item.token,
            "id": next_id,
            "score": item.score,
            "is_reserved": False,
        })
        next_id += 1
    for item in selected_bytes:
        vocab_entries.append({
            "token": item.token,
            "id": next_id,
            "score": item.score,
            "is_reserved": False,
        })
        next_id += 1

    target_final_size = next_id
    special_tokens = coerce_special_tokens(target_draft["special_tokens"])

    lineage = dict(target_draft.get("lineage", {}))
    lineage.update({
        "generator": "ash_full_v4_manifest_generator.py",
        "generated_from_manifest": source_manifest.get("manifest_id"),
        "source_vocab_size": len(source_vocab),
        "source_reserved_count": len(source_manifest.get("reserved_tokens", [])),
        "target_reserved_count": reserved_count,
        "byte_block_count": byte_count,
        "imported_from": imported_from,
        "import_format": imported_format,
    })

    hot_token_cache = dict(target_draft.get("hot_token_cache", {}))
    if default_top_k is not None:
        hot_token_cache["default_top_k"] = int(default_top_k)
    if hot_token_cache.get("enabled"):
        top_k = int(hot_token_cache.get("default_top_k", 0))
        hot_token_cache["derived_artifact_id"] = f"hotcache_{manifest_id}_{top_k}"

    manifest: Dict[str, Any] = {
        "manifest_id": manifest_id,
        "tokenizer_spec_id": str(target_draft["tokenizer_spec_id"]),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "description": str(target_draft.get("description") or "Generated V4 tokenizer manifest"),
        "trainer": dict(target_draft["trainer"]),
        "normalization": dict(target_draft["normalization"]),
        "special_tokens": special_tokens,
        "reserved_tokens": reserved_tokens,
        "vocab": vocab_entries,
        "lineage": lineage,
        "hot_token_cache": hot_token_cache,
        "hashes": {},
    }

    report = {
        "manifest_id": manifest_id,
        "source_manifest_id": source_manifest.get("manifest_id"),
        "target_tokenizer_spec_id": target_draft.get("tokenizer_spec_id"),
        "target_declared_vocab_size": target_vocab_size,
        "generated_vocab_size": target_final_size,
        "shortfall": shortfall,
        "reserved_count": reserved_count,
        "byte_block_count": byte_count,
        "target_nonbyte_slots": target_nonbyte_slots,
        "selected_nonbyte_count": len(selected_nonbyte),
        "selected_byte_count": len(selected_bytes),
        "source_nonbyte_count": len(source_nonbyte_entries),
        "external_candidate_nonbyte_count": len(external_nonbyte),
        "external_candidate_byte_count": len(external_byte),
        "used_external_nonbyte_count": sum(1 for item in selected_nonbyte if item.source != "source_manifest"),
        "used_source_nonbyte_fallback_count": sum(1 for item in selected_nonbyte if item.source == "source_manifest"),
        "notes": [],
    }
    if target_final_size != target_vocab_size:
        report["notes"].append(
            f"generated vocab size {target_final_size} does not match draft trainer.vocab_size {target_vocab_size}"
        )
    if shortfall > 0:
        report["notes"].append(
            f"shortfall={shortfall}; provide more candidate non-byte tokens or raise target/source strategy"
        )

    manifest["hashes"] = {
        "reserved_tokens_hash": sha256_json(manifest["reserved_tokens"]),
        "vocab_hash": sha256_json(manifest["vocab"]),
    }
    manifest_for_hash = dict(manifest)
    manifest_for_hash["hashes"] = dict(manifest["hashes"])
    manifest_for_hash["hashes"].pop("manifest_hash", None)
    manifest["hashes"]["manifest_hash"] = sha256_json(manifest_for_hash)

    return manifest, report



def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate a full tokenizer_manifest_clean_v4.json from V3 manifest + V4 draft scaffold + optional candidate token lists."
    )
    parser.add_argument("--source-manifest", required=True, type=Path, help="Existing V3 manifest JSON")
    parser.add_argument("--target-draft", required=True, type=Path, help="V4 draft scaffold JSON")
    parser.add_argument("--out-manifest", required=True, type=Path, help="Output full V4 manifest JSON")
    parser.add_argument("--out-report", type=Path, default=None, help="Optional JSON report path")
    parser.add_argument("--candidate-json", type=Path, action="append", default=[], help="JSON candidate token list or tokenizer.json export")
    parser.add_argument("--candidate-manifest", type=Path, action="append", default=[], help="Existing manifest JSON to harvest candidate vocab from")
    parser.add_argument("--candidate-tsv", type=Path, action="append", default=[], help="TSV token[tab]score candidate file")
    parser.add_argument("--candidate-jsonl", type=Path, action="append", default=[], help="JSONL candidate file with token/score objects")
    parser.add_argument("--manifest-id", default=None, help="Override manifest_id")
    parser.add_argument("--imported-from", default=None, help="Optional lineage.imported_from value")
    parser.add_argument("--import-format", default=None, help="Optional lineage.import_format value")
    parser.add_argument("--default-top-k", type=int, default=None, help="Override hot_token_cache.default_top_k")
    parser.add_argument("--prefer-higher-score", action="store_true", help="Prefer higher candidate score when duplicate tokens appear")
    parser.add_argument("--allow-shortfall", action="store_true", help="Write partial manifest even if not enough non-byte tokens are available")
    parser.add_argument("--dry-run", action="store_true", help="Do not write manifest; only emit report")
    args = parser.parse_args(argv)

    source_manifest = load_json(args.source_manifest)
    target_draft = load_json(args.target_draft)

    all_candidates: List[CandidateEntry] = []
    for path in args.candidate_json:
        all_candidates.extend(load_candidates_from_json(path))
    for path in args.candidate_manifest:
        all_candidates.extend(load_candidates_from_manifest(path))
    for path in args.candidate_tsv:
        all_candidates.extend(load_candidates_from_tsv(path))
    for path in args.candidate_jsonl:
        all_candidates.extend(load_candidates_from_jsonl(path))

    ordered_candidates, dedupe_stats = merge_unique_candidates(all_candidates, prefer_higher_score=args.prefer_higher_score)

    manifest_id = args.manifest_id or (
        f"tok_v4_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
    )
    manifest, report = build_manifest(
        source_manifest,
        target_draft,
        ordered_candidates,
        allow_shortfall=args.allow_shortfall,
        manifest_id=manifest_id,
        imported_from=args.imported_from,
        imported_format=args.import_format,
        default_top_k=args.default_top_k,
    )
    report["candidate_dedupe"] = dedupe_stats
    report["dry_run"] = bool(args.dry_run)

    if args.out_report is not None:
        dump_json(report, args.out_report)

    if args.dry_run:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    dump_json(manifest, args.out_manifest)
    print(json.dumps({
        "ok": True,
        "manifest_path": str(args.out_manifest),
        "report_path": None if args.out_report is None else str(args.out_report),
        "generated_vocab_size": report["generated_vocab_size"],
        "target_declared_vocab_size": report["target_declared_vocab_size"],
        "shortfall": report["shortfall"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
