#!/usr/bin/env python3
"""EVAL-TRANS-00/R1 actual output runner.

Orchestrates a real Ash translation eval command if provided and records runtime
availability. It never fabricates model output and never copies reference_ko into
model_output.

Default behavior without ASH_EVAL_TRANS_COMMAND is a blocked execution receipt.
Template variables available in --command / ASH_EVAL_TRANS_COMMAND:
  {eval_path} {output_path} {receipt_path} {vocab_size} {patch_id}
"""
from __future__ import annotations
import argparse, json, os, shutil, shlex, subprocess
from pathlib import Path

DOMAIN = "en_to_ko_translation_subtitle_machine"

def count_jsonl(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())

def read_jsonl(path: Path):
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows

def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def validate_output(eval_rows, output_path: Path):
    rows = read_jsonl(output_path)
    eval_ids = [r.get("case_id") for r in eval_rows]
    eval_id_set = set(eval_ids)
    seen = set()
    duplicate = 0
    missing_required = 0
    reference_leak = 0
    for r in rows:
        cid = r.get("case_id")
        if cid in seen:
            duplicate += 1
        seen.add(cid)
        for key in ["case_id", "source_text", "model_output", "decode_config"]:
            if key not in r:
                missing_required += 1
                break
        if "reference_ko" in r and "model_output" in r and str(r.get("reference_ko", "")).strip() and str(r.get("reference_ko", "")).strip() == str(r.get("model_output", "")).strip():
            reference_leak += 1
    missing = len([cid for cid in eval_ids if cid not in seen])
    unexpected = len([r for r in rows if r.get("case_id") not in eval_id_set])
    schema_valid = len(rows) == len(eval_rows) and missing == 0 and unexpected == 0 and duplicate == 0 and missing_required == 0
    return {
        "output_case_count": len(rows),
        "output_schema_valid": schema_valid,
        "missing_output_case_count": missing,
        "unexpected_output_case_count": unexpected,
        "duplicate_output_case_id_count": duplicate,
        "rows_missing_required_fields": missing_required,
        "reference_leak_as_model_output_count": reference_leak,
        "reference_leak_as_model_output": reference_leak > 0
    }

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--eval", default="eval/eval_trans_00/en_ko_subtitle_actual_eval_138.jsonl")
    ap.add_argument("--output", default="workspace/eval_trans_00_model_outputs.jsonl")
    ap.add_argument("--receipt", default="workspace/eval_trans_00_r1_execution_receipt.json")
    ap.add_argument("--vocab-size", type=int, default=48259)
    ap.add_argument("--patch-id", default="16AI-QW-38G-R6A-EVAL-TRANS-00-R1")
    ap.add_argument("--command", default=os.environ.get("ASH_EVAL_TRANS_COMMAND"))
    ap.add_argument("--checkpoint", default="checkpoints/ash_1p1b.safetensors")
    ap.add_argument("--tokenizer", default="artifacts/tokenizer_manifest_v5_final.json")
    args = ap.parse_args()

    eval_path = Path(args.eval)
    output_path = Path(args.output)
    receipt_path = Path(args.receipt)
    workspace = receipt_path.parent
    output_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    workspace.mkdir(parents=True, exist_ok=True)

    eval_rows = read_jsonl(eval_path)
    output_path.write_text("", encoding="utf-8")

    cargo_path = shutil.which("cargo")
    rustc_path = shutil.which("rustc")
    checkpoint_path = Path(args.checkpoint)
    tokenizer_path = Path(args.tokenizer)
    runtime_bin_available = False
    # We cannot know crate bin existence without cargo metadata; keep false unless command is provided.
    if args.command:
        runtime_bin_available = True

    status = "BLOCKED_CARGO_UNAVAILABLE" if not cargo_path else "BLOCKED_RUNTIME_BIN_UNAVAILABLE"
    reason = "cargo_unavailable" if not cargo_path else "runtime_command_not_provided"
    completed = None

    stdout_log = workspace / "eval_trans_00_r1_stdout.log"
    stderr_log = workspace / "eval_trans_00_r1_stderr.log"
    stdout_log.write_text("", encoding="utf-8")
    stderr_log.write_text("", encoding="utf-8")

    if args.command and cargo_path:
        cmd = args.command.format(eval_path=str(eval_path), output_path=str(output_path), receipt_path=str(receipt_path), vocab_size=args.vocab_size, patch_id=args.patch_id)
        try:
            completed = subprocess.run(shlex.split(cmd), text=True, capture_output=True, timeout=7200)
            stdout_log.write_text(completed.stdout, encoding="utf-8")
            stderr_log.write_text(completed.stderr, encoding="utf-8")
            reason = "runtime_command_executed" if completed.returncode == 0 else "runtime_command_failed"
        except Exception as exc:
            reason = f"runtime_command_exception:{type(exc).__name__}"
            stderr_log.write_text(str(exc), encoding="utf-8")
    elif not checkpoint_path.exists() and cargo_path:
        status = "BLOCKED_CHECKPOINT_UNAVAILABLE"
        reason = "checkpoint_unavailable"
    elif cargo_path and not args.command:
        status = "BLOCKED_RUNTIME_BIN_UNAVAILABLE"
        reason = "runtime_command_not_provided"

    validation = validate_output(eval_rows, output_path)
    generated = validation["output_schema_valid"] and validation["output_case_count"] == len(eval_rows) and len(eval_rows) > 0 and not validation["reference_leak_as_model_output"]
    if generated and completed and completed.returncode == 0:
        status = "PASS_ACTUAL_MODEL_OUTPUT_GENERATED"
    elif validation["output_case_count"] > 0 and not validation["output_schema_valid"]:
        status = "BLOCKED_OUTPUT_FORMAT_MISMATCH"

    receipt = {
        "patch_id": args.patch_id,
        "title": "Actual Output Runner Execution / Runtime Availability Receipt Seal",
        "domain_ssot": DOMAIN,
        "preceded_by": "16AI-QW-38G-R6A-EVAL-TRANS-00",
        "model_family": "Ash 1.1B",
        "vocab_size": args.vocab_size,
        "stale_300m_spec_used_as_ssot": False,
        "eval_dataset_exists": eval_path.exists(),
        "eval_dataset_path": str(eval_path),
        "eval_case_count": len(eval_rows),
        "runner_executed": True,
        "runtime_command_provided": bool(args.command),
        "cargo_available": bool(cargo_path),
        "rustc_available": bool(rustc_path),
        "cargo_path": cargo_path,
        "rustc_path": rustc_path,
        "runtime_bin_available": runtime_bin_available,
        "checkpoint_available": checkpoint_path.exists(),
        "checkpoint_path": str(checkpoint_path),
        "tokenizer_available": tokenizer_path.exists(),
        "tokenizer_path": str(tokenizer_path),
        "model_outputs_generated": generated,
        "output_case_count": validation["output_case_count"],
        "output_schema_valid": validation["output_schema_valid"],
        "missing_output_case_count": validation["missing_output_case_count"],
        "duplicate_output_case_id_count": validation["duplicate_output_case_id_count"],
        "reference_leak_as_model_output": validation["reference_leak_as_model_output"],
        "reference_leak_as_model_output_count": validation["reference_leak_as_model_output_count"],
        "fake_model_output": False,
        "false_output_claim": False,
        "false_runtime_claim": False,
        "translation_quality_scored": False,
        "reason": reason,
        "eval_trans_r1_status": status,
        "next_recommended_patch": {
            "PASS_ACTUAL_MODEL_OUTPUT_GENERATED": "16AI-QW-38G-R6A-EVAL-TRANS-01",
            "BLOCKED_CARGO_UNAVAILABLE": "16AI-QW-38G-R6A-BUILD-ENV-02-R1",
            "BLOCKED_RUNTIME_BIN_UNAVAILABLE": "16AI-QW-38G-R6A-RUNTIME-EVAL-00",
            "BLOCKED_CHECKPOINT_UNAVAILABLE": "16AI-QW-38G-R6A-CHECKPOINT-00",
            "BLOCKED_OUTPUT_FORMAT_MISMATCH": "16AI-QW-38G-R6A-EVAL-TRANS-00-R2"
        }.get(status, "16AI-QW-38G-R6A-EVAL-TRANS-00-R2")
    }
    write_json(receipt_path, receipt)
    write_json(workspace / "eval_trans_00_r1_runtime_availability_report.json", {
        "patch_id": args.patch_id,
        "cargo_available": bool(cargo_path),
        "rustc_available": bool(rustc_path),
        "runtime_bin_available": runtime_bin_available,
        "checkpoint_available": checkpoint_path.exists(),
        "tokenizer_available": tokenizer_path.exists(),
        "eval_dataset_available": eval_path.exists(),
        "blocked_reason": reason,
        "status": status
    })
    write_json(workspace / "eval_trans_00_r1_output_schema_validation.json", {"patch_id": args.patch_id, **validation})
    write_json(workspace / "eval_trans_00_r1_reference_leak_scan.json", {
        "patch_id": args.patch_id,
        "reference_leak_as_model_output": validation["reference_leak_as_model_output"],
        "reference_leak_as_model_output_count": validation["reference_leak_as_model_output_count"],
        "fake_model_output": False
    })
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
