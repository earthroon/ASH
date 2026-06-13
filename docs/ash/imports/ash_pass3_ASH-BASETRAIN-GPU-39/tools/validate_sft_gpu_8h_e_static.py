from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
checks = []

def check(name, condition):
    if not condition:
        raise SystemExit(f"[FAIL] {name}")
    checks.append(name)
    print(f"[PASS] {name}")

pass2 = ROOT / "crates/lora_train/src/lm_head_vocab_atlas_gpu_pass2_grad.rs"
atlas = ROOT / "crates/lora_train/src/lm_head_vocab_atlas.rs"
lib = ROOT / "crates/lora_train/src/lib.rs"
acc = ROOT / "acceptance_reports/SFT-GPU-8H-E_pass2_gpu_gradient_kernel.md"

check("lm_head_vocab_atlas_gpu_pass2_grad.rs exists", pass2.exists())
text = pass2.read_text(encoding="utf-8")
atlas_text = atlas.read_text(encoding="utf-8")
lib_text = lib.read_text(encoding="utf-8")

for sym in [
    "GpuPass2GradConfig",
    "GpuPass2GradLayout",
    "GpuPass2GradBuffers",
    "GpuPass2GradReport",
    "validate_pass2_grad_policy",
    "build_gpu_pass2_grad_buffers",
    "dispatch_pass2_grad_kernel",
    "cpu_reference_pass2_grad_group",
    "run_pass2_grad_fixture_parity",
    "write_pass2_grad_report",
]:
    check(f"{sym} exists", sym in text)

check("module exported", "pub mod lm_head_vocab_atlas_gpu_pass2_grad;" in lib_text)
check("target_subtraction_applied report exists", "target_subtraction_applied" in text)
check("mean_loss_normalization report exists", "mean_loss_normalization" in text)
check("full_logits_buffer_created=false report exists", "full_logits_buffer_created: false" in text)
check("logits_readback=false report exists", "logits_readback: false" in text)
check("PASS_PASS2_GPU_GRAD_KERNEL_SMOKE exists", "PASS_PASS2_GPU_GRAD_KERNEL_SMOKE" in text and "PASS_PASS2_GPU_GRAD_KERNEL_SMOKE" in atlas_text)
check("8H-E entry connected", "dispatch_pass2_grad_kernel" in atlas_text and "write_pass2_grad_report" in atlas_text)
check("8H-D handoff replaced", "pass2 GPU gradient is scheduled for SFT-GPU-8H-E" not in atlas_text)
check("8H-F handoff exists", "SFT-GPU-8H-F partial gradient reduce + update kernel" in atlas_text)
check("acceptance report exists", acc.exists())

print(f"[PASS_STATIC] SFT-GPU-8H-E pass2 GPU gradient kernel ({len(checks)} checks)")
