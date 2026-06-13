#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
checks = []

def contains(path: str, needle: str) -> bool:
    text = (ROOT / path).read_text(encoding="utf-8")
    return needle in text

required = [
    ("crates/runtime/src/infer.rs", "mod qw50_r0w_trace;"),
    ("crates/runtime/src/infer.rs", "native_decode_r0w_trace"),
    ("crates/runtime/src/infer.rs", "build_native_decode_r0w_trace"),
    ("crates/runtime/src/infer/qw50_r0w_trace.rs", "topKCandidatesByStep"),
    ("crates/runtime/src/infer/qw50_r0w_trace.rs", "rawModelOutputBeforeGuard"),
    ("crates/runtime/src/infer/qw50_r0w_trace.rs", "decode_policy_mutation"),
    ("crates/runtime/examples/infer_only.rs", "nativeDecodeR0wTrace"),
    ("tools/run_qw50_r0w_trace_probe.py", "nativeDecodeR0wTrace"),
]
for path, needle in required:
    checks.append({"path": path, "needle": needle, "ok": contains(path, needle)})
status = "PASS" if all(c["ok"] for c in checks) else "FAIL"
out = {"patch_id": "QW-50-R0W", "status": status, "checks": checks, "cargo_check": "NOT_RUN_CARGO_NOT_AVAILABLE_IN_SANDBOX"}
print(json.dumps(out, ensure_ascii=False, indent=2))
raise SystemExit(0 if status == "PASS" else 1)
