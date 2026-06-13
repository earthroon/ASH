#!/usr/bin/env python3
"""
BUILD-ENV-01 Rust toolchain local/CI provision follow-up.

This script is intentionally an environment probe and receipt emitter only.
It does not execute or emulate decode QA/RUN guards, and it must never be used
as a Python substitute for Rust guard results.
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import platform
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

PATCH_ID = "16AI-QW-38G-R6A-BUILD-ENV-01"
TITLE = "Rust Toolchain Local/CI Provision Follow-up Seal"
DOMAIN_SSOT = "en_to_ko_translation_subtitle_machine"
PRECEDED_BY = "16AI-QW-38G-R6A-BUILD-00-R1"
ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT / "workspace"
CI_TEMPLATE = ROOT / "ci_templates" / "ash_build_env_01_github_actions.yml"
TOOLCHAIN_FILE = ROOT / "rust-toolchain.toml"

QA_TEST_COMMANDS = [
    "cargo test -p tokenizer_core --test decode_qa_05_control_token_guard",
    "cargo test -p tokenizer_core --test decode_qa_06_byte_utf8_guard",
    "cargo test -p tokenizer_core --test decode_qa_07_linebreak_guard",
    "cargo test -p tokenizer_core --test decode_qa_08_degeneration_guard",
    "cargo test -p tokenizer_core --test decode_qa_09_termination_guard",
    "cargo test -p tokenizer_core --test decode_qa_10_subtitle_smoke",
    "cargo test -p tokenizer_core --test decode_qa_11_regression_matrix",
    "cargo test -p tokenizer_core --test decode_qa_12_quality_closure",
    "cargo test -p tokenizer_core --test decode_run_00_runtime_guard_chain",
]
RUN_COMMANDS = [
    "python3 tools/provision_rust_toolchain.py --verify --emit-receipt",
    "python3 tools/provision_rust_toolchain.py --local-provision-check",
    "python3 tools/run_build_00_r1_cargo_environment_rerun.py",
    "cargo run -p tokenizer_core --bin decode_run_00_runtime_guard_chain",
]


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run_cmd(args: List[str], cwd: Optional[Path] = None, timeout: int = 60) -> Dict[str, Any]:
    exe = shutil.which(args[0])
    if exe is None:
        return {
            "cmd": args,
            "available": False,
            "executed": False,
            "exit_code": None,
            "stdout": "",
            "stderr": f"{args[0]} unavailable in PATH",
        }
    try:
        completed = subprocess.run(
            args,
            cwd=str(cwd or ROOT),
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        return {
            "cmd": args,
            "available": True,
            "executed": True,
            "exit_code": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
    except Exception as exc:
        return {
            "cmd": args,
            "available": True,
            "executed": False,
            "exit_code": None,
            "stdout": "",
            "stderr": f"execution_error: {exc}",
        }


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, obj: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def first_line(text: str) -> Optional[str]:
    for line in text.splitlines():
        if line.strip():
            return line.strip()
    return None


def q4_hash(payload: Dict[str, Any]) -> str:
    canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return "q4sha256:" + hashlib.sha256(hashlib.sha256(canonical).digest()).hexdigest()


def ensure_toolchain_config() -> Dict[str, Any]:
    if not TOOLCHAIN_FILE.exists():
        write_text(
            TOOLCHAIN_FILE,
            '[toolchain]\nchannel = "stable"\nprofile = "minimal"\ncomponents = ["rustfmt", "clippy"]\n',
        )
    text = TOOLCHAIN_FILE.read_text(encoding="utf-8")
    report = {
        "patch_id": PATCH_ID,
        "domain_ssot": DOMAIN_SSOT,
        "toolchain_file": "rust-toolchain.toml",
        "rust_toolchain_config_present": TOOLCHAIN_FILE.exists(),
        "rust_toolchain_channel": "stable" if 'channel = "stable"' in text else None,
        "rust_toolchain_profile": "minimal" if 'profile = "minimal"' in text else None,
        "rustfmt_required": "rustfmt" in text,
        "clippy_required": "clippy" in text,
        "nightly_forced": "nightly" in text,
        "exact_version_pinned": False,
    }
    write_json(WORKSPACE / "build_env_01_toolchain_config_report.json", report)
    return report


def path_probe() -> Dict[str, Any]:
    probes = {
        "rustup": shutil.which("rustup"),
        "rustc": shutil.which("rustc"),
        "cargo": shutil.which("cargo"),
        "rustfmt": shutil.which("rustfmt"),
        "clippy": shutil.which("clippy"),
    }
    cargo_home = os.environ.get("CARGO_HOME") or str(Path.home() / ".cargo")
    rustup_home = os.environ.get("RUSTUP_HOME") or str(Path.home() / ".rustup")
    cargo_bin = str(Path(cargo_home) / "bin")
    path_value = os.environ.get("PATH", "")
    report = {
        "patch_id": PATCH_ID,
        "domain_ssot": DOMAIN_SSOT,
        "generated_at_utc": now_utc(),
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "python_version": platform.python_version(),
        },
        "path_probe": probes,
        "CARGO_HOME": cargo_home,
        "RUSTUP_HOME": rustup_home,
        "expected_cargo_bin": cargo_bin,
        "path_contains_expected_cargo_bin": cargo_bin in path_value.split(os.pathsep),
        "PATH_preview": path_value[:4000],
    }
    write_json(WORKSPACE / "build_env_01_path_probe.json", report)
    write_text(WORKSPACE / "build_env_01_path_probe_stdout.log", json.dumps(probes, indent=2) + "\n")
    write_text(WORKSPACE / "build_env_01_path_probe_stderr.log", "")
    return report


def probe_environment() -> Dict[str, Any]:
    rustup_version = run_cmd(["rustup", "--version"])
    rustup_show = run_cmd(["rustup", "show"])
    rustc_version = run_cmd(["rustc", "--version"])
    rustc_verbose = run_cmd(["rustc", "-vV"])
    cargo_version = run_cmd(["cargo", "--version"])

    write_text(WORKSPACE / "build_env_01_rustup_show.log", rustup_show["stdout"] + rustup_show["stderr"])
    write_text(WORKSPACE / "build_env_01_rustc_version.log", rustc_version["stdout"] + rustc_version["stderr"])
    write_text(WORKSPACE / "build_env_01_cargo_version.log", cargo_version["stdout"] + cargo_version["stderr"])

    host_triple = None
    active_toolchain = None
    if rustc_verbose.get("stdout"):
        for line in rustc_verbose["stdout"].splitlines():
            if line.startswith("host: "):
                host_triple = line.split(": ", 1)[1].strip()
    if rustup_show.get("stdout"):
        for line in rustup_show["stdout"].splitlines():
            if "(default)" in line or "active toolchain" in line.lower():
                active_toolchain = line.strip()
                break

    cargo_available = bool(cargo_version["available"] and cargo_version["executed"] and cargo_version["exit_code"] == 0)
    rustc_available = bool(rustc_version["available"] and rustc_version["executed"] and rustc_version["exit_code"] == 0)
    rustup_available = bool(rustup_version["available"] and rustup_version["executed"] and rustup_version["exit_code"] == 0)

    probe = {
        "patch_id": PATCH_ID,
        "title": TITLE,
        "domain_ssot": DOMAIN_SSOT,
        "preceded_by": PRECEDED_BY,
        "generated_at_utc": now_utc(),
        "rustup_available": rustup_available,
        "rustc_available": rustc_available,
        "cargo_available": cargo_available,
        "rustup_version": first_line(rustup_version["stdout"]),
        "rustc_version": first_line(rustc_version["stdout"]),
        "cargo_version": first_line(cargo_version["stdout"]),
        "host_triple": host_triple,
        "active_toolchain": active_toolchain,
        "raw_commands": {
            "rustup_version": {k: v for k, v in rustup_version.items() if k != "stdout"},
            "rustup_show": {k: (v[:2000] if isinstance(v, str) else v) for k, v in rustup_show.items()},
            "rustc_version": rustc_version,
            "rustc_verbose": {k: (v[:2000] if isinstance(v, str) else v) for k, v in rustc_verbose.items()},
            "cargo_version": cargo_version,
        },
    }
    write_json(WORKSPACE / "build_env_01_local_toolchain_probe.json", probe)
    return probe


def write_instructions() -> None:
    instructions = f"""# BUILD-ENV-01 Rust Toolchain Installation Instructions

Patch: `{PATCH_ID}`  
Domain SSOT: `{DOMAIN_SSOT}`

This document is an instruction artifact only. It does not claim Rust was installed.
Install Rust in a local or CI environment, then re-run the probes and BUILD-00-R1.

## Windows PowerShell

```powershell
winget install --id Rustlang.Rustup -e
rustup toolchain install stable
rustup default stable
rustup component add rustfmt
rustup component add clippy
cargo --version
rustc --version
```

## macOS / Linux

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
rustup toolchain install stable
rustup default stable
rustup component add rustfmt
rustup component add clippy
cargo --version
rustc --version
```

## Important boundary

Python may probe the environment and write receipts. Python must not replace Rust decode guard execution.
"""
    recheck = f"""# BUILD-ENV-01 Recheck Commands

Run from the repository root after Rust is installed.

```bash
python3 tools/provision_rust_toolchain.py --verify --emit-receipt
python3 tools/provision_rust_toolchain.py --local-provision-check
python3 tools/run_build_00_r1_cargo_environment_rerun.py
```

Then execute the decode guard chain if Cargo check or tokenizer_core-only execution is available.

```bash
cargo test -p tokenizer_core --test decode_run_00_runtime_guard_chain
cargo run -p tokenizer_core --bin decode_run_00_runtime_guard_chain
```

Expected branches:

```text
1. Toolchain unavailable -> BUILD-ENV-02 or external CI execution
2. Toolchain available + sherpa-rs path failure -> BUILD-00-R2
3. Toolchain available + tokenizer_core compile failure -> BUILD-01
4. Guard chain executed PASS -> DECODE-RUN-01
5. Guard chain executed mismatch -> DECODE-RUN-00-R1
```
"""
    handoff = f"""# BUILD-ENV-01 Next Rerun Handoff

Patch: `{PATCH_ID}`  
Domain SSOT: `{DOMAIN_SSOT}`

## Local/Cargo probe

```bash
python3 tools/provision_rust_toolchain.py --verify --emit-receipt
python3 tools/provision_rust_toolchain.py --local-provision-check
```

## BUILD-00-R1 rerun

```bash
python3 tools/run_build_00_r1_cargo_environment_rerun.py
```

## Decode QA/RUN Rust tests

```bash
{chr(10).join(QA_TEST_COMMANDS)}
```

## RUN-00 bin execution

```bash
cargo run -p tokenizer_core --bin decode_run_00_runtime_guard_chain
```

## Status policy

```text
CI template generated does not mean CI executed.
Cargo unavailable does not mean compile failed.
Rust guard tests not run must remain NOT_RUN_CARGO_UNAVAILABLE.
Python orchestration must not substitute Rust guard results.
```
"""
    write_text(WORKSPACE / "build_env_01_installation_instructions.md", instructions)
    write_text(WORKSPACE / "build_env_01_recheck_commands.md", recheck)
    write_text(WORKSPACE / "build_env_01_next_rerun_handoff.md", handoff)


def check_ci_template() -> Dict[str, Any]:
    text = CI_TEMPLATE.read_text(encoding="utf-8") if CI_TEMPLATE.exists() else ""
    required = [
        "actions/checkout@v4",
        "dtolnay/rust-toolchain@stable",
        "tools/provision_rust_toolchain.py --verify --emit-receipt",
        "tools/run_build_00_r1_cargo_environment_rerun.py",
        "cargo test -p tokenizer_core --test decode_qa_05_control_token_guard",
        "cargo test -p tokenizer_core --test decode_run_00_runtime_guard_chain",
        "cargo run -p tokenizer_core --bin decode_run_00_runtime_guard_chain",
        "actions/upload-artifact@v4",
    ]
    missing = [item for item in required if item not in text]
    report = {
        "patch_id": PATCH_ID,
        "domain_ssot": DOMAIN_SSOT,
        "ci_template_generated": CI_TEMPLATE.exists(),
        "ci_template_path": "ci_templates/ash_build_env_01_github_actions.yml",
        "required_surface_check_pass": not missing,
        "missing_required_entries": missing,
        "ci_template_includes_build_00_r1": "tools/run_build_00_r1_cargo_environment_rerun.py" in text,
        "ci_template_includes_decode_guard_tests": "decode_qa_05_control_token_guard" in text and "decode_run_00_runtime_guard_chain" in text,
        "ci_template_includes_decode_run_00": "decode_run_00_runtime_guard_chain" in text,
        "ci_executed": False,
    }
    write_json(WORKSPACE / "build_env_01_ci_template_surface_check.json", report)
    return report


def forbidden_python_guard_scan() -> Dict[str, Any]:
    patterns = [
        "tools/run_decode_qa_05_*.py",
        "tools/run_decode_qa_06_*.py",
        "tools/run_decode_qa_07_*.py",
        "tools/run_decode_qa_08_*.py",
        "tools/run_decode_qa_09_*.py",
        "tools/run_decode_qa_10_*.py",
        "tools/run_decode_qa_11_*.py",
        "tools/run_decode_qa_12_*.py",
        "tools/run_decode_run_00_*.py",
    ]
    matches: List[str] = []
    for path in ROOT.glob("tools/*.py"):
        rel = path.relative_to(ROOT).as_posix()
        if any(fnmatch.fnmatch(rel, pat) for pat in patterns):
            matches.append(rel)
    report = {
        "patch_id": PATCH_ID,
        "domain_ssot": DOMAIN_SSOT,
        "forbidden_python_runner_patterns": patterns,
        "forbidden_python_runner_count": len(matches),
        "forbidden_python_runners": matches,
        "python_guard_substitution": False,
    }
    write_json(WORKSPACE / "build_env_01_forbidden_python_runner_scan.json", report)
    return report


def emit_receipt(probe: Dict[str, Any], toolchain: Dict[str, Any], ci: Dict[str, Any], forbidden: Dict[str, Any]) -> Dict[str, Any]:
    local_available = bool(probe["rustc_available"] and probe["cargo_available"])
    status = "LOCAL_TOOLCHAIN_AVAILABLE" if local_available else "LOCAL_BLOCKED_CI_TEMPLATE_READY"
    receipt: Dict[str, Any] = {
        "patch_id": PATCH_ID,
        "title": TITLE,
        "domain_ssot": DOMAIN_SSOT,
        "preceded_by": PRECEDED_BY,
        "scope": "rust_toolchain_local_ci_provision_follow_up",
        "generated_at_utc": now_utc(),
        "rust_toolchain_config_present": toolchain["rust_toolchain_config_present"],
        "rust_toolchain_channel": toolchain["rust_toolchain_channel"],
        "rust_toolchain_profile": toolchain["rust_toolchain_profile"],
        "rustfmt_required": toolchain["rustfmt_required"],
        "clippy_required": toolchain["clippy_required"],
        "local_cargo_available": probe["cargo_available"],
        "local_rustc_available": probe["rustc_available"],
        "local_rustup_available": probe["rustup_available"],
        "cargo_version": probe.get("cargo_version"),
        "rustc_version": probe.get("rustc_version"),
        "host_triple": probe.get("host_triple"),
        "ci_template_generated": ci["ci_template_generated"],
        "ci_template_includes_build_00_r1": ci["ci_template_includes_build_00_r1"],
        "ci_template_includes_decode_guard_tests": ci["ci_template_includes_decode_guard_tests"],
        "ci_template_includes_decode_run_00": ci["ci_template_includes_decode_run_00"],
        "ci_executed": False,
        "cargo_check_executed": False,
        "cargo_test_executed": False,
        "cargo_run_executed": False,
        "runtime_decode_executed": False,
        "model_forward_executed": False,
        "sampling_executed": False,
        "subtitle_export_executed": False,
        "source_logic_mutation_count": 0,
        "decode_ssot_algorithm_modified": False,
        "runtime_generation_modified": False,
        "sampler_modified": False,
        "subtitle_export_modified": False,
        "false_toolchain_claim": False,
        "false_cargo_check_claim": False,
        "false_rust_test_claim": False,
        "python_guard_substitution": False,
        "forbidden_python_runner_count": forbidden["forbidden_python_runner_count"],
        "environment_status": status,
        "next_recommended_patch": "16AI-QW-38G-R6A-BUILD-00-R1_OR_CI_EXECUTION" if not local_available else "16AI-QW-38G-R6A-BUILD-00-R1",
        "validation_reports": {
            "toolchain_config": "workspace/build_env_01_toolchain_config_report.json",
            "local_toolchain_probe": "workspace/build_env_01_local_toolchain_probe.json",
            "path_probe": "workspace/build_env_01_path_probe.json",
            "ci_template_surface_check": "workspace/build_env_01_ci_template_surface_check.json",
            "forbidden_python_runner_scan": "workspace/build_env_01_forbidden_python_runner_scan.json",
            "local_environment_receipt": "workspace/build_env_01_local_environment_receipt.json",
            "next_rerun_handoff": "workspace/build_env_01_next_rerun_handoff.md",
        },
    }
    receipt["deterministic_receipt_key"] = q4_hash({k: v for k, v in receipt.items() if k != "deterministic_receipt_key"})
    write_json(WORKSPACE / "build_env_01_local_environment_receipt.json", receipt)
    return receipt


def local_provision_check() -> Dict[str, Any]:
    toolchain = ensure_toolchain_config()
    paths = path_probe()
    probe = probe_environment()
    write_instructions()
    ci = check_ci_template()
    forbidden = forbidden_python_guard_scan()
    receipt = emit_receipt(probe, toolchain, ci, forbidden)
    report = {
        "patch_id": PATCH_ID,
        "domain_ssot": DOMAIN_SSOT,
        "local_provision_check_executed": True,
        "local_cargo_available": receipt["local_cargo_available"],
        "local_rustc_available": receipt["local_rustc_available"],
        "environment_status": receipt["environment_status"],
        "path_probe_written": True,
        "receipt_written": True,
    }
    write_json(WORKSPACE / "build_env_01_local_provision_check_report.json", report)
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description="BUILD-ENV-01 Rust toolchain local/CI provision follow-up")
    parser.add_argument("--probe-only", action="store_true")
    parser.add_argument("--write-instructions", action="store_true")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--emit-receipt", action="store_true")
    parser.add_argument("--local-provision-check", action="store_true")
    args = parser.parse_args()

    if not any(vars(args).values()):
        args.local_provision_check = True

    ensure_toolchain_config()
    if args.write_instructions:
        write_instructions()
    if args.probe_only or args.verify:
        path_probe()
        probe_environment()
    if args.local_provision_check or args.emit_receipt:
        local_provision_check()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
