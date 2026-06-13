from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
checks = []

def check(name, cond):
    checks.append((name, bool(cond)))

kernel = ROOT / "crates/lora_train/src/lm_head_vocab_atlas_gpu_pass1_kernel.rs"
pass1 = ROOT / "crates/lora_train/src/lm_head_vocab_atlas_gpu_pass1.rs"
atlas = ROOT / "crates/lora_train/src/lm_head_vocab_atlas.rs"
lib = ROOT / "crates/lora_train/src/lib.rs"
accept = ROOT / "acceptance_reports/SFT-GPU-8H-C2_actual_pass1_gpu_projection_kernel.md"

kt = kernel.read_text(encoding="utf-8") if kernel.exists() else ""
pt = pass1.read_text(encoding="utf-8") if pass1.exists() else ""
at = atlas.read_text(encoding="utf-8") if atlas.exists() else ""
lt = lib.read_text(encoding="utf-8") if lib.exists() else ""

check("lm_head_vocab_atlas_gpu_pass1_kernel.rs exists", kernel.exists())
check("GpuPass1KernelConfig exists", "struct GpuPass1KernelConfig" in kt)
check("GpuPass1KernelDispatchReport exists", "struct GpuPass1KernelDispatchReport" in kt)
check("dispatch_pass1_projection_kernel exists", "fn dispatch_pass1_projection_kernel" in kt)
check("validate_pass1_kernel_policy exists", "fn validate_pass1_kernel_policy" in kt)
check("cpu_reference_pass1_group exists", "fn cpu_reference_pass1_group" in kt)
check("fixture parity exists", "run_pass1_kernel_fixture_parity" in kt and "fixture_max_abs_diff" in kt)
check("PASS_PASS1_GPU_KERNEL_SMOKE string exists", "PASS_PASS1_GPU_KERNEL_SMOKE" in kt + pt + at)
check("full logits false in report", "full_logits_buffer_created: false" in kt)
check("logits_readback false in report", "logits_readback: false" in kt)
check("group logits readback explicitly smoke-scoped", "group_logits_readback_for_smoke" in kt)
check("target capture fixture exists", "partial_target_seen[0] != 1" in kt and "partial_target_seen[1] != 0" in kt)
check("pass1 wrapper calls dispatch", "dispatch_pass1_projection_kernel" in pt)
check("atlas status updates to kernel smoke", "PASS_PASS1_GPU_KERNEL_SMOKE" in at)
check("lib exports kernel module", "pub mod lm_head_vocab_atlas_gpu_pass1_kernel;" in lt)
check("acceptance report exists", accept.exists())

failed = [name for name, ok in checks if not ok]
for name, ok in checks:
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
if failed:
    raise SystemExit(f"[FAIL_STATIC] SFT-GPU-8H-C2 static validation failed: {failed}")
print(f"[PASS_STATIC] SFT-GPU-8H-C2 actual pass1 GPU projection kernel seal ({len(checks)} checks)")
