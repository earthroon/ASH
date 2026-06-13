#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = ROOT / "workspace" / "trace"

def load(name: str):
    path = TRACE_DIR / name
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None

def main() -> int:
    no_guard = load("qw50_r0w_no_guard_trace.json")
    guarded = load("qw50_r0w_guarded_trace.json")
    out = {
        "patch_id": "QW-50-R0W",
        "no_guard_present": no_guard is not None,
        "guarded_present": guarded is not None,
        "comparison": {}
    }
    if no_guard and guarded:
        out["comparison"] = {
            "no_guard_raw": no_guard.get("outputSplit", {}).get("rawModelOutputBeforeGuard"),
            "guarded_raw": guarded.get("outputSplit", {}).get("rawModelOutputBeforeGuard"),
            "guarded_final": guarded.get("outputSplit", {}).get("finalOutputAfterGuard"),
            "guarded_fallback": guarded.get("outputSplit", {}).get("outputGuardFallbackApplied"),
            "no_guard_repeat": no_guard.get("repeatAnalysis"),
            "guarded_repeat": guarded.get("repeatAnalysis"),
        }
    target = TRACE_DIR / "qw50_r0w_guarded_no_guard_comparison.json"
    target.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
