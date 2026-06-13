#!/usr/bin/env python3
"""
16AI-QW-38G-R6A-LORA-FS-02A
Python Torch CUDA Trainer Bridge / Fast Safetensors Export Seal

Drop this file into:
  workspace/scripts/lora_fs02_train_export.py

Purpose:
  Train/export a shared_hidden_token_head_lora adapter from ASH feature-store shards.

This script DOES NOT modify the base checkpoint, tokenizer, lm_head, or final_norm.
It only writes a separate adapter safetensors + adapter manifest + receipts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

PATCH_ID = "16AI-QW-38G-R6A-LORA-FS-02A"
ADAPTER_FAMILY = "shared_hidden_token_head_lora"
TARGET_KEY = "classifier.shared_hidden_token_head"
TENSOR_A = "adapter.shared_hidden_token_head.lora_A"
TENSOR_B = "adapter.shared_hidden_token_head.lora_B"
TENSOR_ALPHA = "adapter.shared_hidden_token_head.alpha"


def now_ms() -> int:
    return int(time.time() * 1000)


def read_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")
    tmp.replace(path)


def append_jsonl(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
        f.write("\n")


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def resolve_path_maybe(base: Path, value: Optional[str]) -> Optional[Path]:
    if value is None:
        return None
    p = Path(value)
    if p.is_absolute():
        return p
    return (base / p).resolve()


def list_feature_shards(feature_root: Path, manifest: Dict[str, Any]) -> List[Dict[str, Any]]:
    shards = manifest.get("shards")
    if isinstance(shards, list) and shards:
        out: List[Dict[str, Any]] = []
        for idx, item in enumerate(shards):
            if isinstance(item, dict):
                raw_path = item.get("path") or item.get("file") or item.get("name")
                if raw_path is None:
                    raw_path = f"feature_{idx:05d}.safetensors"
                shard_id = int(item.get("shard_id", item.get("id", idx)))
                out.append({"shard_id": shard_id, "path": str(raw_path), "manifest": item})
            elif isinstance(item, str):
                out.append({"shard_id": idx, "path": item, "manifest": {}})
        return sorted(out, key=lambda x: x["shard_id"])

    paths = sorted(feature_root.glob("feature_*.safetensors"))
    return [
        {"shard_id": idx, "path": str(path.name), "manifest": {}}
        for idx, path in enumerate(paths)
    ]


def select_device(requested: str):
    import torch

    requested = requested.lower()
    cuda_available = torch.cuda.is_available()
    if requested == "cuda":
        if not cuda_available:
            raise RuntimeError("FAIL_CUDA_NOT_AVAILABLE: --device cuda was requested but torch.cuda.is_available() is false")
        return torch.device("cuda")
    if requested == "auto":
        return torch.device("cuda" if cuda_available else "cpu")
    if requested == "cpu":
        return torch.device("cpu")
    raise ValueError(f"Unsupported --device value: {requested}")


def make_vocab_subset(target_ids, vocab_size: int, negative_samples: int, generator, device):
    """Return subset ids and target positions inside that subset."""
    import torch

    target_ids = target_ids.long()
    unique_targets = torch.unique(target_ids)
    neg_count = max(0, int(negative_samples))
    if neg_count > 0:
        negatives = torch.randint(
            low=0,
            high=vocab_size,
            size=(neg_count,),
            generator=generator,
            device=device,
            dtype=torch.long,
        )
        subset = torch.unique(torch.cat([unique_targets, negatives], dim=0))
    else:
        subset = unique_targets

    # Build compact id->position map. Vocab is ~48k, so this is cheap and deterministic.
    pos_map = torch.full((vocab_size,), -1, device=device, dtype=torch.long)
    pos_map[subset] = torch.arange(subset.numel(), device=device, dtype=torch.long)
    target_positions = pos_map[target_ids]
    if (target_positions < 0).any():
        raise RuntimeError("Internal error: at least one target id was not included in sampled vocab subset")
    return subset, target_positions


def verify_adapter_file(path: Path, expected_rank: int, expected_hidden: int, expected_vocab: int) -> Dict[str, Any]:
    from safetensors.torch import safe_open

    with safe_open(str(path), framework="pt", device="cpu") as f:
        keys = list(f.keys())
        checks: Dict[str, Any] = {"keys": keys, "ok": True, "errors": []}
        for key in (TENSOR_A, TENSOR_B, TENSOR_ALPHA):
            if key not in keys:
                checks["ok"] = False
                checks["errors"].append(f"missing tensor key: {key}")
        if TENSOR_A in keys:
            shape = list(f.get_tensor(TENSOR_A).shape)
            checks["lora_A_shape"] = shape
            if shape != [expected_rank, expected_hidden]:
                checks["ok"] = False
                checks["errors"].append(f"lora_A shape mismatch: {shape}")
        if TENSOR_B in keys:
            shape = list(f.get_tensor(TENSOR_B).shape)
            checks["lora_B_shape"] = shape
            if shape != [expected_vocab, expected_rank]:
                checks["ok"] = False
                checks["errors"].append(f"lora_B shape mismatch: {shape}")
        if TENSOR_ALPHA in keys:
            shape = list(f.get_tensor(TENSOR_ALPHA).shape)
            checks["alpha_shape"] = shape
            if shape not in [[], [1]]:
                checks["ok"] = False
                checks["errors"].append(f"alpha scalar shape mismatch: {shape}")
        return checks


@dataclass
class TrainStats:
    steps: int = 0
    shards_seen: int = 0
    tokens_seen: int = 0
    epochs_completed: int = 0
    final_loss: Optional[float] = None
    final_grad_norm: Optional[float] = None
    loss_is_finite: bool = True
    grad_norm_is_finite: bool = True


def train_and_export(args: argparse.Namespace) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    import torch
    import torch.nn.functional as F
    from safetensors.torch import safe_open, save_file

    started_ms = now_ms()
    run_base = Path.cwd()

    feature_root = resolve_path_maybe(run_base, args.feature_root)
    feature_manifest_path = resolve_path_maybe(run_base, args.feature_manifest)
    export_plan_path = resolve_path_maybe(run_base, args.export_plan)
    out_path = resolve_path_maybe(run_base, args.out)
    manifest_out = resolve_path_maybe(run_base, args.manifest_out)
    receipt_out = resolve_path_maybe(run_base, args.receipt_out)
    trainer_receipt_out = resolve_path_maybe(run_base, args.trainer_receipt_out)
    loss_ledger = resolve_path_maybe(run_base, args.loss_ledger)

    assert feature_root is not None
    assert feature_manifest_path is not None
    assert export_plan_path is not None
    assert out_path is not None
    assert manifest_out is not None
    assert receipt_out is not None
    assert trainer_receipt_out is not None
    assert loss_ledger is not None

    export_plan = read_json(export_plan_path)
    feature_manifest = read_json(feature_manifest_path)

    # Pull expected geometry from export plan first, then manifest fallback.
    hidden_size = int(export_plan.get("hidden_size", feature_manifest.get("hidden_size", feature_manifest.get("input_dim", 2048))))
    vocab_size = int(export_plan.get("vocab_size", feature_manifest.get("vocab_size", feature_manifest.get("output_dim", 48259))))
    rank = int(args.rank)
    alpha = float(args.alpha)
    trainable_parameter_count = rank * hidden_size + vocab_size * rank

    if export_plan.get("adapter_family") not in (None, ADAPTER_FAMILY):
        raise RuntimeError(f"FAIL_EXPORT_PLAN_ADAPTER_FAMILY_UNSUPPORTED: {export_plan.get('adapter_family')}")
    if export_plan.get("adapter_target_key") not in (None, TARGET_KEY):
        raise RuntimeError(f"FAIL_EXPORT_PLAN_TARGET_KEY_UNSUPPORTED: {export_plan.get('adapter_target_key')}")
    if feature_manifest.get("target_key") not in (None, TARGET_KEY):
        raise RuntimeError(f"FAIL_FEATURE_STORE_TARGET_KEY_UNSUPPORTED: {feature_manifest.get('target_key')}")

    device = select_device(args.device)
    cuda_available = torch.cuda.is_available()
    cuda_device_name = torch.cuda.get_device_name(0) if cuda_available else None

    random.seed(args.seed)
    torch.manual_seed(args.seed)
    if cuda_available:
        torch.cuda.manual_seed_all(args.seed)

    # Keep train params in fp32 for numerical stability; export as requested dtype later.
    lora_A = (torch.randn((rank, hidden_size), device=device, dtype=torch.float32) * 0.01).requires_grad_(True)
    lora_B = torch.zeros((vocab_size, rank), device=device, dtype=torch.float32, requires_grad=True)
    optimizer = torch.optim.AdamW([lora_A, lora_B], lr=args.lr, weight_decay=args.weight_decay)

    shards = list_feature_shards(feature_root, feature_manifest)
    if args.max_shards is not None:
        shards = shards[: int(args.max_shards)]
    if not shards:
        raise RuntimeError("FAIL_NO_FEATURE_SHARDS_SELECTED")

    generator_device = "cuda" if device.type == "cuda" else "cpu"
    rng = torch.Generator(device=generator_device)
    rng.manual_seed(args.seed)

    stats = TrainStats()
    max_batches = args.max_batches if args.max_batches is None else int(args.max_batches)
    global_batch_count = 0
    scale = alpha / float(rank)

    for epoch in range(int(args.epochs)):
        for shard_entry in shards:
            if max_batches is not None and global_batch_count >= max_batches:
                break
            shard_id = int(shard_entry.get("shard_id", stats.shards_seen))
            shard_rel = shard_entry.get("path")
            shard_path = Path(str(shard_rel))
            if not shard_path.is_absolute():
                shard_path = feature_root / shard_path
            if not shard_path.exists():
                raise RuntimeError(f"FAIL_FEATURE_STORE_SHARD_MISSING: {shard_path}")

            # One shard is ~69MB in the current feature store, acceptable to load once.
            with safe_open(str(shard_path), framework="pt", device="cpu") as f:
                if "hidden_states" not in f.keys() or "target_ids" not in f.keys():
                    raise RuntimeError(f"FAIL_FEATURE_STORE_TENSOR_KEY_MISSING in {shard_path}")
                hidden_cpu = f.get_tensor("hidden_states")
                target_cpu = f.get_tensor("target_ids")

            if hidden_cpu.ndim != 2 or int(hidden_cpu.shape[1]) != hidden_size:
                raise RuntimeError(f"FAIL_HIDDEN_SHAPE_MISMATCH: shard={shard_id} shape={list(hidden_cpu.shape)}")
            if target_cpu.ndim != 1 or int(target_cpu.shape[0]) != int(hidden_cpu.shape[0]):
                raise RuntimeError(f"FAIL_TARGET_SHAPE_MISMATCH: shard={shard_id} shape={list(target_cpu.shape)}")

            n = int(hidden_cpu.shape[0])
            stats.shards_seen += 1
            for start in range(0, n, int(args.batch_tokens)):
                if max_batches is not None and global_batch_count >= max_batches:
                    break
                end = min(start + int(args.batch_tokens), n)
                hidden = hidden_cpu[start:end].to(device=device, dtype=torch.float32, non_blocking=True)
                target = target_cpu[start:end].to(device=device, dtype=torch.long, non_blocking=True)
                if (target < 0).any() or (target >= vocab_size).any():
                    raise RuntimeError(f"FAIL_TARGET_ID_OUT_OF_RANGE: shard={shard_id} batch_start={start}")

                subset_ids, target_positions = make_vocab_subset(
                    target,
                    vocab_size=vocab_size,
                    negative_samples=int(args.negative_samples),
                    generator=rng,
                    device=device,
                )

                z = hidden.matmul(lora_A.t())  # [batch, rank]
                b_subset = lora_B.index_select(0, subset_ids)  # [subset, rank]
                logits_subset = z.matmul(b_subset.t()) * scale  # [batch, subset]
                loss = F.cross_entropy(logits_subset, target_positions)

                if not torch.isfinite(loss):
                    stats.loss_is_finite = False
                    raise RuntimeError(f"FAIL_LOSS_NONFINITE: shard={shard_id} batch_start={start} loss={loss.item()}")

                optimizer.zero_grad(set_to_none=True)
                loss.backward()
                grad_norm = torch.nn.utils.clip_grad_norm_([lora_A, lora_B], float(args.grad_clip_norm))
                if not torch.isfinite(grad_norm):
                    stats.grad_norm_is_finite = False
                    raise RuntimeError(f"FAIL_GRAD_NORM_NONFINITE: shard={shard_id} batch_start={start} grad_norm={grad_norm}")
                optimizer.step()

                stats.steps += 1
                global_batch_count += 1
                batch_tokens = end - start
                stats.tokens_seen += batch_tokens
                stats.final_loss = float(loss.detach().cpu().item())
                stats.final_grad_norm = float(grad_norm.detach().cpu().item() if hasattr(grad_norm, "detach") else grad_norm)

                ledger_row = {
                    "patch_id": PATCH_ID,
                    "step": stats.steps,
                    "epoch": epoch,
                    "shard_id": shard_id,
                    "token_offset": start,
                    "batch_tokens": batch_tokens,
                    "loss": stats.final_loss,
                    "grad_norm": stats.final_grad_norm,
                    "learning_rate": float(args.lr),
                    "negative_sample_count": int(args.negative_samples),
                    "device": str(device),
                    "ts_ms": now_ms(),
                }
                append_jsonl(loss_ledger, ledger_row)

                if args.log_every > 0 and (stats.steps % args.log_every == 0 or stats.steps == 1):
                    print(
                        f"[lora_fs02a] step={stats.steps} epoch={epoch} shard={shard_id} "
                        f"tokens={stats.tokens_seen} loss={stats.final_loss:.6f} grad_norm={stats.final_grad_norm:.6f}",
                        flush=True,
                    )

            # Release shard CPU tensors explicitly.
            del hidden_cpu, target_cpu

        stats.epochs_completed = epoch + 1
        if max_batches is not None and global_batch_count >= max_batches:
            break

    out_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.parent.mkdir(parents=True, exist_ok=True)

    export_dtype = args.dtype.lower()
    if export_dtype == "f16":
        export_A = lora_A.detach().to("cpu", dtype=torch.float16).contiguous()
        export_B = lora_B.detach().to("cpu", dtype=torch.float16).contiguous()
    elif export_dtype == "f32":
        export_A = lora_A.detach().to("cpu", dtype=torch.float32).contiguous()
        export_B = lora_B.detach().to("cpu", dtype=torch.float32).contiguous()
    else:
        raise ValueError(f"Unsupported --dtype: {args.dtype}")
    alpha_tensor = torch.tensor(float(alpha), dtype=torch.float32)

    save_file(
        {
            TENSOR_A: export_A,
            TENSOR_B: export_B,
            TENSOR_ALPHA: alpha_tensor,
        },
        str(out_path),
        metadata={
            "format": "ash_domain_adapter_safetensors_v1",
            "adapter_family": ADAPTER_FAMILY,
            "target_key": TARGET_KEY,
            "rank": str(rank),
            "alpha": str(int(alpha) if alpha.is_integer() else alpha),
            "base_model_id": str(export_plan.get("base_model_id", feature_manifest.get("model_id", "model_tinyllama_1p1b_v4"))),
            "hidden_size": str(hidden_size),
            "vocab_size": str(vocab_size),
            "source_patch_id": PATCH_ID,
        },
    )

    verify = verify_adapter_file(out_path, rank, hidden_size, vocab_size)
    if not verify.get("ok"):
        raise RuntimeError("FAIL_EXPORTED_ADAPTER_VERIFICATION: " + "; ".join(verify.get("errors", [])))

    out_hash = sha256_file(out_path)
    adapter_id = out_path.stem
    adapter_manifest = {
        "format": "ash_domain_adapter_manifest_v1",
        "adapter_id": adapter_id,
        "adapter_family": ADAPTER_FAMILY,
        "target_key": TARGET_KEY,
        "source_patch_id": PATCH_ID,
        "source_feature_store_manifest": str(feature_manifest_path),
        "source_export_plan": str(export_plan_path),
        "base_model_id": str(export_plan.get("base_model_id", feature_manifest.get("model_id", "model_tinyllama_1p1b_v4"))),
        "base_hidden_size": hidden_size,
        "base_vocab_size": vocab_size,
        "rank": rank,
        "alpha": alpha,
        "dtype": export_dtype,
        "recommended_scale_for_infer": float(export_plan.get("recommended_scale_for_infer", 0.35)),
        "runtime_attach_mode": "domain_adapter_logit_delta",
        "safetensors_path": str(out_path),
        "safetensors_sha256": out_hash,
        "tensor_keys": {
            "lora_A": TENSOR_A,
            "lora_B": TENSOR_B,
            "alpha": TENSOR_ALPHA,
        },
        "planned_runtime_formula": "final_logits = base_logits + scale * (alpha / rank) * (B @ (A @ hidden))",
        "base_checkpoint_modified": False,
        "tokenizer_modified": False,
    }
    write_json(manifest_out, adapter_manifest)

    completed_ms = now_ms()
    common = {
        "patch_id": PATCH_ID,
        "runner": "python_torch_cuda_lora_fs_trainer",
        "request_id": args.request_id,
        "dry_run": bool(args.dry_run),
        "source_feature_store_status": "PASS_FEATURE_STORE_EXPORT_PLAN_READY",
        "source_export_plan_status": str(export_plan.get("export_plan_status", "READY_FOR_LORA_FS_02")),
        "python_trainer_backend": "torch",
        "torch_available": True,
        "torch_version": torch.__version__,
        "cuda_available": bool(cuda_available),
        "cuda_device_name": cuda_device_name,
        "device": str(device),
        "safetensors_available": True,
        "adapter_family": ADAPTER_FAMILY,
        "target_key": TARGET_KEY,
        "rank": rank,
        "alpha": alpha,
        "dtype": export_dtype,
        "trainable_tensor_count": 2,
        "trainable_parameter_count": trainable_parameter_count,
        "lora_A_shape": [rank, hidden_size],
        "lora_B_shape": [vocab_size, rank],
        "trainer_loss_mode": "sampled_softmax_ce",
        "negative_sample_count": int(args.negative_samples),
        "streaming_loader_used": True,
        "full_feature_store_loaded_into_ram": False,
        "full_vocab_logits_materialized": False,
        "shards_selected": len(shards),
        "shards_seen": stats.shards_seen,
        "tokens_seen": stats.tokens_seen,
        "epochs_completed": stats.epochs_completed,
        "steps": stats.steps,
        "final_loss": stats.final_loss,
        "final_grad_norm": stats.final_grad_norm,
        "loss_is_finite": stats.loss_is_finite,
        "grad_norm_is_finite": stats.grad_norm_is_finite,
        "output_safetensors_path": str(out_path),
        "output_manifest_path": str(manifest_out),
        "output_safetensors_sha256": out_hash,
        "output_safetensors_written": True,
        "output_manifest_written": True,
        "export_tensor_keys_verified": True,
        "export_tensor_shapes_verified": True,
        "started_at_unix_ms": started_ms,
        "completed_at_unix_ms": completed_ms,
        "elapsed_ms": completed_ms - started_ms,
        "status": "PASS_PYTORCH_CUDA_SHARED_HIDDEN_HEAD_LORA_EXPORTED" if device.type == "cuda" else "PASS_PYTORCH_SHARED_HIDDEN_HEAD_LORA_EXPORTED_CPU_OR_NONCUDA",
        "adjudication": "PASS_FAST_SINGLE_DOMAIN_ADAPTER_SAFETENSORS_EXPORTED",
        "checkpoint_modified": False,
        "tokenizer_modified": False,
        "base_safetensors_modified": False,
        "lm_head_modified": False,
        "final_norm_modified": False,
        "ban_mask_modified": False,
    }

    trainer_receipt = dict(common)
    trainer_receipt.update({
        "lora_A_init": "normal_std_0.01",
        "lora_B_init": "zeros",
        "initial_delta_logits_zeroish": True,
        "learning_rate": float(args.lr),
        "weight_decay": float(args.weight_decay),
        "grad_clip_norm": float(args.grad_clip_norm),
        "batch_tokens": int(args.batch_tokens),
        "max_shards": args.max_shards,
        "max_batches": args.max_batches,
        "loss_ledger_path": str(loss_ledger),
    })
    export_receipt = dict(common)
    export_receipt.update({
        "adapter_manifest": adapter_manifest,
        "verification": verify,
    })

    write_json(trainer_receipt_out, trainer_receipt)
    write_json(receipt_out, export_receipt)
    return trainer_receipt, export_receipt


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ASH LORA-FS-02A Python Torch CUDA trainer/export bridge")
    parser.add_argument("--request-id", default="lora_fs02a_train_export")
    parser.add_argument("--feature-root", required=True)
    parser.add_argument("--feature-manifest", required=True)
    parser.add_argument("--export-plan", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--manifest-out", required=True)
    parser.add_argument("--receipt-out", required=True)
    parser.add_argument("--trainer-receipt-out", required=True)
    parser.add_argument("--loss-ledger", required=True)
    parser.add_argument("--rank", type=int, default=8)
    parser.add_argument("--alpha", type=float, default=16.0)
    parser.add_argument("--max-shards", type=int, default=None)
    parser.add_argument("--max-batches", type=int, default=None)
    parser.add_argument("--batch-tokens", type=int, default=2048)
    parser.add_argument("--epochs", type=int, default=1)
    parser.add_argument("--negative-samples", type=int, default=128)
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--weight-decay", type=float, default=0.0)
    parser.add_argument("--grad-clip-norm", type=float, default=1.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--device", choices=["cuda", "cpu", "auto"], default="cuda")
    parser.add_argument("--dtype", choices=["f16", "f32"], default="f16")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--log-every", type=int, default=10)
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    try:
        trainer_receipt, export_receipt = train_and_export(args)
        print(json.dumps({
            "ok": True,
            "type": "response",
            "id": args.request_id,
            "status": export_receipt.get("status"),
            "output_safetensors_path": export_receipt.get("output_safetensors_path"),
            "output_manifest_path": export_receipt.get("output_manifest_path"),
            "tokens_seen": export_receipt.get("tokens_seen"),
            "final_loss": export_receipt.get("final_loss"),
        }, ensure_ascii=False))
        return 0
    except Exception as e:
        failure = {
            "ok": False,
            "patch_id": PATCH_ID,
            "runner": "python_torch_cuda_lora_fs_trainer",
            "request_id": getattr(args, "request_id", "unknown"),
            "status": "FAIL_PYTORCH_LORA_FS02A_TRAIN_EXPORT",
            "error": str(e),
            "checkpoint_modified": False,
            "tokenizer_modified": False,
            "base_safetensors_modified": False,
            "lm_head_modified": False,
            "final_norm_modified": False,
            "ban_mask_modified": False,
        }
        # Best-effort failure receipt.
        for attr in ("receipt_out", "trainer_receipt_out"):
            try:
                path_value = getattr(args, attr, None)
                if path_value:
                    write_json(Path(path_value), failure)
            except Exception:
                pass
        print(json.dumps(failure, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
