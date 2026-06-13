# 16AI-QW-38G-R6A-BUILD-ENV-01 Bake Report

## Rust Toolchain Local/CI Provision Follow-up Seal

### Summary

This bake updates the Rust toolchain local/CI provision layer after `DECODE-QA-01~12`, `DECODE-RUN-00`, and the latest `BUILD-00-R1` re-entry. It does not modify decode, runtime generation, sampler, model forward, rerank, or subtitle export logic.

### Added / Updated Files

```text
rust-toolchain.toml
tools/provision_rust_toolchain.py
ci_templates/ash_build_env_01_github_actions.yml
workspace/build_env_01_toolchain_config_report.json
workspace/build_env_01_local_toolchain_probe.json
workspace/build_env_01_path_probe.json
workspace/build_env_01_local_environment_receipt.json
workspace/build_env_01_installation_instructions.md
workspace/build_env_01_recheck_commands.md
workspace/build_env_01_next_rerun_handoff.md
workspace/build_env_01_ci_template_surface_check.json
workspace/build_env_01_forbidden_python_runner_scan.json
workspace/build_env_01_json_validation_report.json
workspace/build_env_01_generated_file_manifest.json
acceptance_reports/16AI-QW-38G-R6A-BUILD-ENV-01_rust_toolchain_local_ci_provision_follow_up_seal.md
patch_reports/16AI-QW-38G-R6A-BUILD-ENV-01_bake_report.md
```

### Execution Result

```text
local_cargo_available = false
local_rustc_available = false
local_rustup_available = false
ci_template_generated = true
ci_template_includes_decode_guard_tests = true
ci_template_includes_decode_run_00 = true
cargo_check_executed = false
cargo_test_executed = false
cargo_run_executed = false
python_guard_substitution = false
forbidden_python_runner_count = 0
environment_status = LOCAL_BLOCKED_CI_TEMPLATE_READY
```

### Boundary

Python remains an environment/provision/orchestration receipt helper only. It does not replace Rust decode guard execution.

### Next Commands

```bash
python3 tools/provision_rust_toolchain.py --verify --emit-receipt
python3 tools/provision_rust_toolchain.py --local-provision-check
python3 tools/run_build_00_r1_cargo_environment_rerun.py
```

If Cargo is available:

```bash
cargo test -p tokenizer_core --test decode_run_00_runtime_guard_chain
cargo run -p tokenizer_core --bin decode_run_00_runtime_guard_chain
```
