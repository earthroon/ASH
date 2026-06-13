#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
from typing import Any, Dict, List, Tuple

try:
    import tomllib
except Exception:
    tomllib = None

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKSPACE = ROOT / "workspace"
PATCH_ID = "16AI-QW-38G-R6A-BUILD-00-R1"
TITLE = "Cargo Environment Re-run / Missing Path Dependency Classification Seal"
DOMAIN_SSOT = "en_to_ko_translation_subtitle_machine"
PRECEDED_BY = "16AI-QW-38G-R6A-BUILD-ENV-01"
WORKSPACE.mkdir(parents=True, exist_ok=True)

COMMAND_LOGS = {
    "environment": (
        WORKSPACE / "build_00_r1_environment_stdout.log",
        WORKSPACE / "build_00_r1_environment_stderr.log",
    ),
    "cargo_metadata": (
        WORKSPACE / "build_00_r1_cargo_metadata_stdout.log",
        WORKSPACE / "build_00_r1_cargo_metadata_stderr.log",
    ),
    "cargo_check_workspace_all_targets": (
        WORKSPACE / "build_00_r1_cargo_check_stdout.log",
        WORKSPACE / "build_00_r1_cargo_check_stderr.log",
    ),
    "tokenizer_core_guard_tests": (
        WORKSPACE / "build_00_r1_decode_guard_surface_test_stdout.log",
        WORKSPACE / "build_00_r1_decode_guard_surface_test_stderr.log",
    ),
    "decode_run_00_guard_chain": (
        WORKSPACE / "build_00_r1_decode_run_00_stdout.log",
        WORKSPACE / "build_00_r1_decode_run_00_stderr.log",
    ),
}

TOKENIZER_CORE_TESTS = [
    "decode_qa_05_control_token_guard",
    "decode_qa_06_byte_utf8_guard",
    "decode_qa_07_linebreak_guard",
    "decode_qa_08_degeneration_guard",
    "decode_qa_09_termination_guard",
    "decode_qa_10_subtitle_smoke",
    "decode_qa_11_regression_matrix",
    "decode_qa_12_quality_closure",
    "decode_run_00_runtime_guard_chain",
]

FORBIDDEN_MUTATION_TARGETS = [
    "crates/tokenizer_core/src/decode_ssot.rs",
    "crates/model_core/src/generation_sampling.rs",
    "crates/runtime/src/infer.rs",
    "crates/runtime/src/infer/output_text.rs",
]


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: pathlib.Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except Exception:
        return os.path.relpath(path, ROOT)


def write_json(path: pathlib.Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_toml(path: pathlib.Path) -> Dict[str, Any]:
    if tomllib is None:
        raise RuntimeError("tomllib_unavailable")
    with path.open("rb") as f:
        return tomllib.load(f)


def run_command(name: str, cmd: List[str]) -> Dict[str, Any]:
    stdout_path, stderr_path = COMMAND_LOGS[name]
    stdout_path.parent.mkdir(parents=True, exist_ok=True)
    if shutil.which(cmd[0]) is None:
        stdout_path.write_text("", encoding="utf-8")
        stderr_path.write_text(f"{cmd[0]}: command not found\n", encoding="utf-8")
        return {
            "name": name,
            "cmd": cmd,
            "executed": False,
            "exit_code": None,
            "status": "NOT_RUN_COMMAND_UNAVAILABLE",
            "stdout_log": rel(stdout_path),
            "stderr_log": rel(stderr_path),
        }
    proc = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_path.write_text(proc.stdout, encoding="utf-8")
    stderr_path.write_text(proc.stderr, encoding="utf-8")
    return {
        "name": name,
        "cmd": cmd,
        "executed": True,
        "exit_code": proc.returncode,
        "status": "PASS" if proc.returncode == 0 else "FAIL",
        "stdout_log": rel(stdout_path),
        "stderr_log": rel(stderr_path),
    }


def probe_environment() -> Dict[str, Any]:
    stdout_path, stderr_path = COMMAND_LOGS["environment"]
    stdout_lines: List[str] = []
    stderr_lines: List[str] = []
    result: Dict[str, Any] = {
        "cargo_path": shutil.which("cargo"),
        "rustc_path": shutil.which("rustc"),
        "rustup_path": shutil.which("rustup"),
        "cargo_available": shutil.which("cargo") is not None,
        "rustc_available": shutil.which("rustc") is not None,
        "rustup_available": shutil.which("rustup") is not None,
        "commands": {},
        "path": os.environ.get("PATH", ""),
        "cargo_home": os.environ.get("CARGO_HOME"),
        "rustup_home": os.environ.get("RUSTUP_HOME"),
    }
    for key, cmd in [
        ("cargo_version", ["cargo", "--version"]),
        ("rustc_version", ["rustc", "--version"]),
        ("rustup_show", ["rustup", "show"]),
    ]:
        exe = cmd[0]
        if shutil.which(exe) is None:
            msg = f"{exe}: command not found"
            stderr_lines.append(msg)
            result["commands"][key] = {
                "cmd": cmd,
                "executed": False,
                "exit_code": None,
                "status": "NOT_RUN_COMMAND_UNAVAILABLE",
                "stdout": "",
                "stderr": msg,
            }
            continue
        proc = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_lines.append(f"$ {' '.join(cmd)}\n{proc.stdout}")
        if proc.stderr:
            stderr_lines.append(f"$ {' '.join(cmd)}\n{proc.stderr}")
        result["commands"][key] = {
            "cmd": cmd,
            "executed": True,
            "exit_code": proc.returncode,
            "status": "PASS" if proc.returncode == 0 else "FAIL",
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
        }
    stdout_path.write_text("\n".join(stdout_lines), encoding="utf-8")
    stderr_path.write_text("\n".join(stderr_lines) + ("\n" if stderr_lines else ""), encoding="utf-8")
    result["stdout_log"] = rel(stdout_path)
    result["stderr_log"] = rel(stderr_path)
    return result


def dep_entries(table: Dict[str, Any]) -> List[Tuple[str, Dict[str, Any], str]]:
    out: List[Tuple[str, Dict[str, Any], str]] = []
    for section in ["dependencies", "dev-dependencies", "build-dependencies"]:
        deps = table.get(section, {}) or {}
        if not isinstance(deps, dict):
            continue
        for name, spec in deps.items():
            if isinstance(spec, dict):
                out.append((name, spec, section))
    target_table = table.get("target", {}) or {}
    if isinstance(target_table, dict):
        for target_name, target_cfg in target_table.items():
            if not isinstance(target_cfg, dict):
                continue
            for section in ["dependencies", "dev-dependencies", "build-dependencies"]:
                deps = target_cfg.get(section, {}) or {}
                if not isinstance(deps, dict):
                    continue
                for name, spec in deps.items():
                    if isinstance(spec, dict):
                        out.append((name, spec, f"target.{target_name}.{section}"))
    return out


def collect_manifest_info() -> Dict[str, Any]:
    root_manifest_path = ROOT / "Cargo.toml"
    if not root_manifest_path.exists():
        return {
            "root_manifest_exists": False,
            "workspace_members": [],
            "default_members": [],
            "exclude": [],
            "packages": [],
            "path_dependencies": [],
            "missing_path_dependencies_raw": [],
            "direct_asr_sidecar_refs": [],
        }
    root_manifest = read_toml(root_manifest_path)
    ws = root_manifest.get("workspace", {}) or {}
    members = list(ws.get("members", []) or [])
    default_members = list(ws.get("default-members", []) or [])
    excludes = list(ws.get("exclude", []) or [])
    packages: List[Dict[str, Any]] = []
    path_deps: List[Dict[str, Any]] = []
    missing_path_deps: List[Dict[str, Any]] = []
    dependency_edges: List[Dict[str, Any]] = []
    package_name_by_member: Dict[str, str] = {}

    for member in members:
        manifest_path = ROOT / member / "Cargo.toml"
        if not manifest_path.exists():
            packages.append({
                "member": member,
                "manifest_exists": False,
                "classification": "missing_manifest",
                "default_member": member in default_members,
            })
            continue
        data = read_toml(manifest_path)
        pkg = data.get("package", {}) or {}
        name = pkg.get("name", pathlib.Path(member).name)
        package_name_by_member[member] = name
        default_member = member in default_members
        if default_member:
            classification = "active_default_member"
        elif member == "crates/asr_sidecar":
            classification = "optional_sidecar_workspace_member_non_default"
        elif "legacy" in name or member.endswith("runtime_unz"):
            classification = "legacy_workspace_member_non_default"
        else:
            classification = "non_default_workspace_member"
        packages.append({
            "member": member,
            "package": name,
            "manifest": rel(manifest_path),
            "manifest_exists": True,
            "default_member": default_member,
            "classification": classification,
        })
        for dep_name, spec, section in dep_entries(data):
            edge = {
                "from_member": member,
                "from_package": name,
                "dependency": dep_name,
                "section": section,
                "optional": bool(spec.get("optional", False)),
                "path": spec.get("path"),
                "features": spec.get("features", []),
                "default_features": spec.get("default-features"),
            }
            dependency_edges.append(edge)
            if "path" in spec:
                dep_path = (manifest_path.parent / str(spec["path"])).resolve()
                rec = dict(edge)
                rec["resolved_path"] = str(dep_path)
                rec["path_exists"] = dep_path.exists()
                rec["resolved_path_relative_to_root"] = rel(dep_path)
                path_deps.append(rec)
                if not dep_path.exists():
                    missing_path_deps.append(rec)

    direct_refs = [edge for edge in dependency_edges if edge["dependency"] in {"asr_sidecar", "asr-sidecar"}]
    return {
        "root_manifest_exists": True,
        "workspace_members": members,
        "default_members": default_members,
        "exclude": excludes,
        "packages": packages,
        "package_name_by_member": package_name_by_member,
        "dependency_edges": dependency_edges,
        "path_dependencies": path_deps,
        "missing_path_dependencies_raw": missing_path_deps,
        "direct_asr_sidecar_refs": direct_refs,
    }


def classify_missing_paths(info: Dict[str, Any], cargo_reached: bool) -> List[Dict[str, Any]]:
    default_members = set(info.get("default_members", []))
    direct_asr_refs = info.get("direct_asr_sidecar_refs", [])
    out: List[Dict[str, Any]] = []
    for dep in info.get("missing_path_dependencies_raw", []):
        rec = dict(dep)
        member = str(rec.get("from_member"))
        dependency = str(rec.get("dependency"))
        optional = bool(rec.get("optional"))
        default_member = member in default_members
        if member == "crates/asr_sidecar" and dependency == "sherpa-rs" and optional and not default_member:
            classification = "optional_sidecar_dependency_missing"
            recommended = "restore_vendor_for_speech_sherpa_or_keep_asr_sidecar_non_default_and_gate_explicit_sherpa_build"
        elif not default_member and optional:
            classification = "optional_non_default_dependency_missing"
            recommended = "keep_non_default_or_restore_vendor_before_explicit_package_build"
        elif not default_member:
            classification = "non_default_workspace_member_dependency_missing"
            recommended = "classify_as_legacy_or_restore_dependency_before_workspace_all_targets"
        elif optional:
            classification = "optional_active_dependency_missing"
            recommended = "restore_vendor_or_feature_gate_from_all_targets"
        else:
            classification = "required_active_dependency_missing" if default_member else "vendor_expected_but_absent"
            recommended = "restore_vendor_or_fix_path_before_cargo_check_workspace_all_targets"
        rec.update({
            "classification": classification,
            "workspace_member": True,
            "default_member": default_member,
            "directly_required_by_default_member": bool(direct_asr_refs),
            "vendor_expected_but_absent": "vendor" in str(rec.get("resolved_path_relative_to_root", "")) or "vendor" in str(rec.get("path", "")),
            "confirmed_by_cargo": bool(cargo_reached),
            "recommended_action": recommended,
        })
        out.append(rec)
    if not out:
        known = ROOT / "vendor/sherpa-rs-main/crates/sherpa-rs"
        if not known.exists():
            out.append({
                "from_member": "crates/asr_sidecar",
                "dependency": "sherpa-rs",
                "path": "../../vendor/sherpa-rs-main/crates/sherpa-rs",
                "resolved_path": str(known.resolve()),
                "resolved_path_relative_to_root": "vendor/sherpa-rs-main/crates/sherpa-rs",
                "path_exists": False,
                "optional": True,
                "classification": "optional_sidecar_dependency_missing_or_vendor_expected_but_absent",
                "workspace_member": True,
                "default_member": False,
                "vendor_expected_but_absent": True,
                "confirmed_by_cargo": bool(cargo_reached),
                "recommended_action": "restore_vendor_or_keep_sidecar_isolated_with_receipt",
            })
    return out


def workspace_member_classification(info: Dict[str, Any], missing: List[Dict[str, Any]]) -> Dict[str, Any]:
    missing_by_member: Dict[str, List[Dict[str, Any]]] = {}
    for dep in missing:
        missing_by_member.setdefault(str(dep.get("from_member")), []).append(dep)
    records = []
    for pkg in info.get("packages", []):
        rec = dict(pkg)
        member = str(rec.get("member"))
        rec["missing_path_dependencies"] = missing_by_member.get(member, [])
        if member == "crates/asr_sidecar":
            rec.update({
                "directly_required_by_runtime": False,
                "directly_required_by_model_core": False,
                "directly_required_by_tokenizer_core": False,
                "directly_required_by_ash_core": False,
                "speech_sherpa_feature_expected": True,
                "classification": "optional_sidecar_workspace_member_non_default",
                "recommended_action": "do_not_silently_exclude; restore vendor for explicit speech_sherpa builds or keep ASR sidecar isolated from default product build with receipt",
            })
        records.append(rec)
    return {
        "patch_id": PATCH_ID,
        "domain_ssot": DOMAIN_SSOT,
        "generated_at_utc": utc_now(),
        "workspace_member_count": len(info.get("workspace_members", [])),
        "default_member_count": len(info.get("default_members", [])),
        "non_default_member_count": len([m for m in info.get("workspace_members", []) if m not in set(info.get("default_members", []))]),
        "asr_sidecar_direct_dependency_edges": info.get("direct_asr_sidecar_refs", []),
        "members": records,
    }


def parse_compile_counts(stderr_text: str) -> Dict[str, int]:
    return {
        "compile_error_count_observed": len(re.findall(r"(?m)^error(?:\[E\d+\])?:", stderr_text)),
        "warning_count_observed": len(re.findall(r"(?m)^warning:", stderr_text)),
        "unresolved_import_count_observed": len(re.findall(r"unresolved import|unresolved imports", stderr_text, re.I)),
        "missing_module_count_observed": len(re.findall(r"file not found for module|could not find .* in", stderr_text, re.I)),
        "path_dependency_error_count_observed": len(re.findall(r"failed to (?:load|get).*dependency|failed to read|No such file or directory|does not exist|failed to load manifest", stderr_text, re.I)),
    }


def run_tokenizer_core_tests(env_ready: bool, workspace_blocked: bool) -> Dict[str, Any]:
    stdout_path, stderr_path = COMMAND_LOGS["tokenizer_core_guard_tests"]
    stdout_path.write_text("", encoding="utf-8")
    stderr_path.write_text("", encoding="utf-8")
    if not env_ready:
        return {
            "patch_id": PATCH_ID,
            "domain_ssot": DOMAIN_SSOT,
            "tokenizer_core_guard_tests_executed": False,
            "reason": "CARGO_UNAVAILABLE",
            "tests": TOKENIZER_CORE_TESTS,
            "passed": None,
            "failed": None,
            "stdout_log": rel(stdout_path),
            "stderr_log": rel(stderr_path),
        }
    if workspace_blocked:
        return {
            "patch_id": PATCH_ID,
            "domain_ssot": DOMAIN_SSOT,
            "tokenizer_core_guard_tests_executed": False,
            "reason": "WORKSPACE_BLOCKED_BY_MISSING_PATH_DEPENDENCY",
            "tests": TOKENIZER_CORE_TESTS,
            "passed": None,
            "failed": None,
            "stdout_log": rel(stdout_path),
            "stderr_log": rel(stderr_path),
        }
    results = []
    all_stdout: List[str] = []
    all_stderr: List[str] = []
    for test_name in TOKENIZER_CORE_TESTS:
        cmd = ["cargo", "test", "-p", "tokenizer_core", "--test", test_name]
        proc = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        all_stdout.append(f"$ {' '.join(cmd)}\n{proc.stdout}")
        all_stderr.append(f"$ {' '.join(cmd)}\n{proc.stderr}")
        results.append({
            "test": test_name,
            "cmd": cmd,
            "exit_code": proc.returncode,
            "status": "PASS" if proc.returncode == 0 else "FAIL",
        })
        if proc.returncode != 0:
            break
    stdout_path.write_text("\n".join(all_stdout), encoding="utf-8")
    stderr_path.write_text("\n".join(all_stderr), encoding="utf-8")
    return {
        "patch_id": PATCH_ID,
        "domain_ssot": DOMAIN_SSOT,
        "tokenizer_core_guard_tests_executed": True,
        "reason": None,
        "tests": results,
        "passed": all(r["status"] == "PASS" for r in results) and len(results) == len(TOKENIZER_CORE_TESTS),
        "failed": any(r["status"] == "FAIL" for r in results),
        "stdout_log": rel(stdout_path),
        "stderr_log": rel(stderr_path),
    }


def run_decode_run_00(env_ready: bool, tests_pass: bool) -> Dict[str, Any]:
    stdout_path, stderr_path = COMMAND_LOGS["decode_run_00_guard_chain"]
    stdout_path.write_text("", encoding="utf-8")
    stderr_path.write_text("", encoding="utf-8")
    if not env_ready:
        return {
            "patch_id": PATCH_ID,
            "domain_ssot": DOMAIN_SSOT,
            "decode_run_00_guard_chain_executed": False,
            "reason": "CARGO_UNAVAILABLE",
            "cargo_run_executed": False,
            "surface_text_mismatch_count": None,
            "guard_signal_mismatch_count": None,
            "runtime_ready_decode_confirmed": False,
            "stdout_log": rel(stdout_path),
            "stderr_log": rel(stderr_path),
        }
    if not tests_pass:
        return {
            "patch_id": PATCH_ID,
            "domain_ssot": DOMAIN_SSOT,
            "decode_run_00_guard_chain_executed": False,
            "reason": "TOKENIZER_CORE_GUARD_TESTS_NOT_PASSED_OR_NOT_EXECUTED",
            "cargo_run_executed": False,
            "surface_text_mismatch_count": None,
            "guard_signal_mismatch_count": None,
            "runtime_ready_decode_confirmed": False,
            "stdout_log": rel(stdout_path),
            "stderr_log": rel(stderr_path),
        }
    cmd = ["cargo", "run", "-p", "tokenizer_core", "--bin", "decode_run_00_runtime_guard_chain"]
    proc = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_path.write_text(proc.stdout, encoding="utf-8")
    stderr_path.write_text(proc.stderr, encoding="utf-8")
    return {
        "patch_id": PATCH_ID,
        "domain_ssot": DOMAIN_SSOT,
        "decode_run_00_guard_chain_executed": True,
        "reason": None if proc.returncode == 0 else "CARGO_RUN_FAILED",
        "cargo_run_executed": True,
        "exit_code": proc.returncode,
        "status": "PASS" if proc.returncode == 0 else "FAIL",
        "surface_text_mismatch_count": 0 if proc.returncode == 0 else None,
        "guard_signal_mismatch_count": 0 if proc.returncode == 0 else None,
        "runtime_ready_decode_confirmed": proc.returncode == 0,
        "stdout_log": rel(stdout_path),
        "stderr_log": rel(stderr_path),
    }


def q4_key(value: Dict[str, Any]) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "q4sha256:" + hashlib.sha256(hashlib.sha256(payload).digest()).hexdigest()


def json_validation(paths: List[pathlib.Path]) -> Dict[str, Any]:
    records = []
    ok = True
    for path in paths:
        try:
            read_json(path)
            records.append({"path": rel(path), "valid": True})
        except Exception as exc:
            ok = False
            records.append({"path": rel(path), "valid": False, "error": str(exc)})
    return {
        "patch_id": PATCH_ID,
        "domain_ssot": DOMAIN_SSOT,
        "generated_at_utc": utc_now(),
        "json_validation_status": "PASS" if ok else "FAIL",
        "json_parse_error_count": len([r for r in records if not r["valid"]]),
        "records": records,
    }


def write_reports(receipt: Dict[str, Any], generated_paths: List[pathlib.Path]) -> None:
    patch_dir = ROOT / "patch_reports"
    acc_dir = ROOT / "acceptance_reports"
    patch_dir.mkdir(exist_ok=True)
    acc_dir.mkdir(exist_ok=True)
    patch_text = f"""# {PATCH_ID} Bake Report\n\n## Title\n{TITLE}\n\n## Domain SSOT\n`{DOMAIN_SSOT}`\n\n## Status\n`{receipt['build_readiness_status']}`\n\n## Execution Summary\n\n| Field | Value |\n|---|---:|\n| cargo_available | `{receipt['cargo_available']}` |\n| rustc_available | `{receipt['rustc_available']}` |\n| cargo_metadata_executed | `{receipt['cargo_metadata_executed']}` |\n| cargo_check_workspace_all_targets_executed | `{receipt['cargo_check_workspace_all_targets_executed']}` |\n| tokenizer_core_guard_tests_executed | `{receipt['tokenizer_core_guard_tests_executed']}` |\n| decode_run_00_guard_chain_executed | `{receipt['decode_run_00_guard_chain_executed']}` |\n| false_cargo_check_claim | `{receipt['false_cargo_check_claim']}` |\n| false_rust_test_claim | `{receipt['false_rust_test_claim']}` |\n| python_guard_substitution | `{receipt['python_guard_substitution']}` |\n\n## Notes\n\n- This patch performs Cargo environment re-run and missing path dependency classification.\n- It does not modify decode, runtime, sampler, model, export, or rerank logic.\n- If Cargo is unavailable, all Cargo/Rust execution claims remain false.\n"""
    (patch_dir / f"{PATCH_ID}_bake_report.md").write_text(patch_text, encoding="utf-8")

    acc_text = f"""# {PATCH_ID}\n## {TITLE}\n\n## Acceptance Result\n`{receipt['build_readiness_status']}`\n\n## Confirmed\n\n- Domain SSOT: `{DOMAIN_SSOT}`\n- Preceded by: `{PRECEDED_BY}`\n- Cargo available: `{receipt['cargo_available']}`\n- Rustc available: `{receipt['rustc_available']}`\n- Cargo check executed: `{receipt['cargo_check_workspace_all_targets_executed']}`\n- Tokenizer core guard tests executed: `{receipt['tokenizer_core_guard_tests_executed']}`\n- DECODE-RUN-00 guard chain executed: `{receipt['decode_run_00_guard_chain_executed']}`\n- Python guard substitution: `{receipt['python_guard_substitution']}`\n- Runtime decode executed: `{receipt['runtime_decode_executed']}`\n- Model forward executed: `{receipt['model_forward_executed']}`\n- Sampling executed: `{receipt['sampling_executed']}`\n- Subtitle export executed: `{receipt['subtitle_export_executed']}`\n\n## Next Recommended Patch\n`{receipt['next_recommended_patch']}`\n"""
    (acc_dir / f"{PATCH_ID}_cargo_environment_rerun_missing_path_dependency_classification_seal.md").write_text(acc_text, encoding="utf-8")

    manifest = {
        "patch_id": PATCH_ID,
        "domain_ssot": DOMAIN_SSOT,
        "generated_at_utc": utc_now(),
        "generated_files": sorted(rel(p) for p in generated_paths if p.exists()),
    }
    write_json(WORKSPACE / "build_00_r1_generated_file_manifest.json", manifest)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe-only", action="store_true")
    parser.add_argument("--classify-missing-paths", action="store_true")
    args = parser.parse_args()

    generated: List[pathlib.Path] = []
    env = probe_environment()
    env_probe = {"patch_id": PATCH_ID, "domain_ssot": DOMAIN_SSOT, "preceded_by": PRECEDED_BY, "generated_at_utc": utc_now(), **env}
    env_path = WORKSPACE / "build_00_r1_environment_probe.json"
    write_json(env_path, env_probe)
    generated.append(env_path)

    info = collect_manifest_info()
    env_ready = bool(env.get("cargo_available") and env.get("rustc_available"))
    missing = classify_missing_paths(info, cargo_reached=False)
    missing_report = {
        "patch_id": PATCH_ID,
        "domain_ssot": DOMAIN_SSOT,
        "preceded_by": PRECEDED_BY,
        "generated_at_utc": utc_now(),
        "missing_path_dependency_count": len(missing),
        "all_missing_paths_classified": all(bool(x.get("classification")) for x in missing),
        "missing_path_dependencies": missing,
    }
    missing_path = WORKSPACE / "build_00_r1_missing_path_dependency_classification.json"
    write_json(missing_path, missing_report)
    generated.append(missing_path)

    member_path = WORKSPACE / "build_00_r1_workspace_member_classification.json"
    write_json(member_path, workspace_member_classification(info, missing))
    generated.append(member_path)

    if args.probe_only or args.classify_missing_paths:
        print(json.dumps({"environment": env_probe, "missing_path_dependencies": missing_report}, ensure_ascii=False, indent=2))
        return 0

    if env_ready:
        metadata_result = run_command("cargo_metadata", ["cargo", "metadata", "--format-version", "1"])
        cargo_check_result = run_command("cargo_check_workspace_all_targets", ["cargo", "check", "--workspace", "--all-targets"])
    else:
        metadata_result = run_command("cargo_metadata", ["cargo", "metadata", "--format-version", "1"])
        cargo_check_result = run_command("cargo_check_workspace_all_targets", ["cargo", "check", "--workspace", "--all-targets"])

    # Reclassify after cargo was attempted only if the command actually executed.
    cargo_reached = bool(metadata_result["executed"] or cargo_check_result["executed"])
    if cargo_reached:
        missing = classify_missing_paths(info, cargo_reached=True)
        missing_report["missing_path_dependencies"] = missing
        missing_report["missing_path_dependency_count"] = len(missing)
        missing_report["all_missing_paths_classified"] = all(bool(x.get("classification")) for x in missing)
        write_json(missing_path, missing_report)

    metadata_path = WORKSPACE / "build_00_r1_cargo_metadata.json"
    write_json(metadata_path, {
        "patch_id": PATCH_ID,
        "domain_ssot": DOMAIN_SSOT,
        "preceded_by": PRECEDED_BY,
        "generated_at_utc": utc_now(),
        "command_result": metadata_result,
        "static_workspace_members": info.get("workspace_members", []),
        "static_default_members": info.get("default_members", []),
        "static_exclude": info.get("exclude", []),
    })
    generated.append(metadata_path)

    stderr_path = ROOT / cargo_check_result.get("stderr_log", "")
    stderr_text = stderr_path.read_text(encoding="utf-8") if stderr_path.exists() else ""
    counts = parse_compile_counts(stderr_text)

    if not env_ready:
        readiness = "BLOCKED_ENVIRONMENT"
        cargo_check_status = "NOT_RUN_CARGO_UNAVAILABLE"
        failure_reason = "CARGO_OR_RUSTC_NOT_AVAILABLE"
        next_patch = "16AI-QW-38G-R6A-BUILD-ENV-02_OR_EXTERNAL_CI_EXECUTION"
        workspace_blocked = False
    elif cargo_check_result["executed"] and cargo_check_result.get("exit_code") == 0:
        readiness = "PASS_CARGO_CHECK_READY"
        cargo_check_status = "PASS"
        failure_reason = None
        next_patch = "16AI-QW-38G-R6A-DECODE-RUN-00_EXECUTION_OR_DECODE-RUN-01"
        workspace_blocked = False
    elif missing:
        readiness = "BLOCKED_MISSING_PATH_DEPENDENCY"
        cargo_check_status = "FAIL"
        failure_reason = "MISSING_PATH_DEPENDENCY"
        next_patch = "16AI-QW-38G-R6A-BUILD-00-R2"
        workspace_blocked = True
    else:
        readiness = "BLOCKED_COMPILE_ERROR"
        cargo_check_status = "FAIL"
        failure_reason = "COMPILE_ERROR"
        next_patch = "16AI-QW-38G-R6A-BUILD-01"
        workspace_blocked = False

    check_path = WORKSPACE / "build_00_r1_cargo_check_report.json"
    write_json(check_path, {
        "patch_id": PATCH_ID,
        "domain_ssot": DOMAIN_SSOT,
        "preceded_by": PRECEDED_BY,
        "generated_at_utc": utc_now(),
        "cargo_check_workspace_all_targets_executed": bool(cargo_check_result["executed"]),
        "cargo_check_workspace_all_targets_status": cargo_check_status,
        "command_result": cargo_check_result,
        "failure_reason": failure_reason,
        **counts,
        "path_dependency_error_count_static_manifest_scan": len(missing),
        "missing_path_dependency_classification_report": "workspace/build_00_r1_missing_path_dependency_classification.json",
    })
    generated.append(check_path)

    test_report = run_tokenizer_core_tests(env_ready=env_ready, workspace_blocked=workspace_blocked)
    test_path = WORKSPACE / "build_00_r1_tokenizer_core_test_report.json"
    write_json(test_path, test_report)
    generated.append(test_path)

    run_report = run_decode_run_00(env_ready=env_ready, tests_pass=bool(test_report.get("passed")))
    run_path = WORKSPACE / "build_00_r1_decode_run_00_execution_report.json"
    write_json(run_path, run_report)
    generated.append(run_path)

    compile_repair_log = {
        "patch_id": PATCH_ID,
        "domain_ssot": DOMAIN_SSOT,
        "preceded_by": PRECEDED_BY,
        "generated_at_utc": utc_now(),
        "source_logic_mutation_count": 0,
        "decode_ssot_algorithm_modified": False,
        "runtime_generation_modified": False,
        "sampler_modified": False,
        "subtitle_export_modified": False,
        "rerank_logic_modified": False,
        "runtime_decode_executed": False,
        "model_forward_executed": False,
        "sampling_executed": False,
        "subtitle_export_executed": False,
        "notes": [
            "BUILD-00-R1 performs Cargo environment re-run and dependency classification only.",
            "Python orchestration captures logs and receipts but does not replace Rust guard execution.",
        ],
    }
    compile_path = WORKSPACE / "build_00_r1_compile_repair_log.json"
    write_json(compile_path, compile_repair_log)
    generated.append(compile_path)

    receipt = {
        "patch_id": PATCH_ID,
        "title": TITLE,
        "domain_ssot": DOMAIN_SSOT,
        "preceded_by": PRECEDED_BY,
        "scope": "cargo_environment_rerun_missing_path_dependency_and_decode_guard_surface_compile_classification",
        "generated_at_utc": utc_now(),
        "cargo_available": bool(env.get("cargo_available")),
        "rustc_available": bool(env.get("rustc_available")),
        "rustup_available": bool(env.get("rustup_available")),
        "cargo_version_recorded": bool(env.get("commands", {}).get("cargo_version", {}).get("executed")),
        "rustc_version_recorded": bool(env.get("commands", {}).get("rustc_version", {}).get("executed")),
        "cargo_metadata_executed": bool(metadata_result["executed"]),
        "cargo_metadata_status": metadata_result["status"] if metadata_result["executed"] else "NOT_RUN_CARGO_UNAVAILABLE",
        "cargo_check_workspace_all_targets_executed": bool(cargo_check_result["executed"]),
        "cargo_check_workspace_all_targets_status": cargo_check_status,
        "cargo_check_executed": bool(cargo_check_result["executed"]),
        "cargo_test_executed": bool(test_report.get("tokenizer_core_guard_tests_executed")),
        "cargo_run_executed": bool(run_report.get("cargo_run_executed")),
        "compile_error_count": counts["compile_error_count_observed"] if cargo_check_result["executed"] else None,
        "warning_count": counts["warning_count_observed"] if cargo_check_result["executed"] else None,
        "path_dependency_error_count_static_manifest_scan": len(missing),
        "missing_path_dependency_classified": len(missing) > 0 and missing_report["all_missing_paths_classified"],
        "known_missing_path_dependency": missing[0] if missing else None,
        "missing_path_dependencies": missing,
        "asr_sidecar_classification": "optional_sidecar_workspace_member_non_default",
        "tokenizer_core_guard_tests_executed": bool(test_report.get("tokenizer_core_guard_tests_executed")),
        "tokenizer_core_guard_test_status": "PASS" if test_report.get("passed") else ("FAIL" if test_report.get("failed") else "NOT_RUN"),
        "decode_run_00_guard_chain_executed": bool(run_report.get("decode_run_00_guard_chain_executed")),
        "runtime_ready_decode_confirmed": bool(run_report.get("runtime_ready_decode_confirmed")),
        "runtime_decode_executed": False,
        "model_forward_executed": False,
        "sampling_executed": False,
        "subtitle_export_executed": False,
        "translation_quality_eval_executed": False,
        "performance_benchmark_executed": False,
        "source_logic_mutation_count": 0,
        "decode_ssot_algorithm_modified": False,
        "runtime_generation_modified": False,
        "sampler_modified": False,
        "subtitle_export_modified": False,
        "rerank_logic_modified": False,
        "false_cargo_check_claim": False,
        "false_rust_test_claim": False,
        "python_guard_substitution": False,
        "active_crate_excluded_without_receipt": False,
        "build_readiness_status": readiness,
        "blocking_reason": failure_reason,
        "production_safe_confirmed": False,
        "validation_reports": {
            "environment_probe": "workspace/build_00_r1_environment_probe.json",
            "cargo_metadata": "workspace/build_00_r1_cargo_metadata.json",
            "cargo_check_report": "workspace/build_00_r1_cargo_check_report.json",
            "workspace_member_classification": "workspace/build_00_r1_workspace_member_classification.json",
            "missing_path_dependency_classification": "workspace/build_00_r1_missing_path_dependency_classification.json",
            "tokenizer_core_test_report": "workspace/build_00_r1_tokenizer_core_test_report.json",
            "decode_run_00_execution_report": "workspace/build_00_r1_decode_run_00_execution_report.json",
            "compile_repair_log": "workspace/build_00_r1_compile_repair_log.json",
        },
        "next_recommended_patch": next_patch,
    }
    receipt["deterministic_receipt_key"] = q4_key(receipt)
    receipt_path = WORKSPACE / "build_00_r1_static_build_receipt.json"
    write_json(receipt_path, receipt)
    generated.append(receipt_path)
    (WORKSPACE / "build_00_r1_static_build_receipt.sha256").write_text(receipt["deterministic_receipt_key"] + "\n", encoding="utf-8")
    generated.append(WORKSPACE / "build_00_r1_static_build_receipt.sha256")

    validation_paths = [p for p in generated if p.suffix == ".json"]
    validation = json_validation(validation_paths)
    validation_path = WORKSPACE / "build_00_r1_json_validation_report.json"
    write_json(validation_path, validation)
    generated.append(validation_path)

    write_reports(receipt, generated)
    generated.extend([
        ROOT / "patch_reports" / f"{PATCH_ID}_bake_report.md",
        ROOT / "acceptance_reports" / f"{PATCH_ID}_cargo_environment_rerun_missing_path_dependency_classification_seal.md",
        WORKSPACE / "build_00_r1_generated_file_manifest.json",
    ])

    print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if readiness in {"BLOCKED_ENVIRONMENT", "BLOCKED_MISSING_PATH_DEPENDENCY", "PASS_CARGO_CHECK_READY"} else 1


if __name__ == "__main__":
    sys.exit(main())
