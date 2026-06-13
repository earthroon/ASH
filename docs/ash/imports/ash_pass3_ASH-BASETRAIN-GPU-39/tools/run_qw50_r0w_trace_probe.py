#!/usr/bin/env python3
"""Run QW-50-R0W infer_only and persist nativeDecodeR0wTrace.

This wrapper is trace-only. It does not alter decode policy, guard policy, LoRA scale,
or token bans. It expects the R0W patched infer_only --json output to include
nativeDecodeR0wTrace.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "workspace" / "trace"
TRACE_DIR.mkdir(parents=True, exist_ok=True)


def default_profile(mode: str) -> Path:
    if mode == "no_guard":
        return ROOT / "specs" / "runtime_profile_debug_no_guard.toml"
    return ROOT / "specs" / "runtime_profile.toml"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["no_guard", "guarded"], default="no_guard")
    parser.add_argument("--text", default="Translate naturally: I need a quick status update.")
    parser.add_argument("--task", default="translation_assist")
    parser.add_argument("--max-new-tokens", type=int, default=96)
    parser.add_argument("--runtime-profile", type=Path)
    parser.add_argument("--infer-exe", type=Path, default=ROOT / "target" / "release" / "examples" / "infer_only.exe")
    args = parser.parse_args()

    profile = args.runtime_profile or default_profile(args.mode)
    cmd = [
        str(args.infer_exe),
        "--runtime-profile", str(profile),
        "--task", args.task,
        "--text", args.text,
        "--max-new-tokens", str(args.max_new_tokens),
        "--json",
    ]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    stdout_path = TRACE_DIR / f"qw50_r0w_{args.mode}_stdout.json"
    stderr_path = TRACE_DIR / f"qw50_r0w_{args.mode}_stderr.log"
    trace_path = TRACE_DIR / f"qw50_r0w_{args.mode}_trace.json"
    stdout_path.write_text(proc.stdout, encoding="utf-8")
    stderr_path.write_text(proc.stderr, encoding="utf-8")

    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        trace_path.write_text(json.dumps({"error": "stdout_not_json", "detail": str(exc)}, ensure_ascii=False, indent=2), encoding="utf-8")
        return proc.returncode or 1

    trace = payload.get("nativeDecodeR0wTrace")
    if trace is None:
        trace = {"error": "nativeDecodeR0wTrace_missing", "available_keys": sorted(payload.keys())}
    trace_path.write_text(json.dumps(trace, ensure_ascii=False, indent=2), encoding="utf-8")
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
