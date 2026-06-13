#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAILURES: list[str] = []
PASSES: list[str] = []


def check(cond: bool, label: str) -> None:
    if cond:
        PASSES.append(label)
    else:
        FAILURES.append(label)


def read(rel: str) -> str:
    path = ROOT / rel
    if not path.exists():
        FAILURES.append(f"missing file: {rel}")
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


sft = read("crates/lora_train/src/sft_feature_store.rs")
provider = read("crates/lora_train/src/a_sft_batched_hidden_provider.rs")
config = read("crates/lora_train/src/config.rs")
native = read("crates/model_core/src/native_wgpu.rs")
lib = read("crates/lora_train/src/lib.rs")
config_json_path = ROOT / "configs/ash_ko_short_sft_lm_head_lora_v1b_native_dump.json"

check("teacher.forward_hidden_ids(&item.example.full_ids)" not in sft,
      "hot path per-example teacher.forward_hidden_ids loop removed from sft_feature_store.rs")
check("build_a_sft_padded_hidden_input" in sft and "slice_hidden_for_example" in sft,
      "A-SFT padded batch builder and seq_len slice helpers present")
check("hidden_provider.forward_group(batch_input)" in sft,
      "native_dump uses ASftBatchedHiddenProvider::forward_group")
check("compute_level_batched_hidden" in sft and "per_example_forward_loop_removed" in sft,
      "progress report records compute-level batched seal fields")
check("pub mod a_sft_batched_hidden_provider;" in lib,
      "a_sft_batched_hidden_provider module exported")
check("pub struct ASftBatchedHiddenInput" in provider and "pub struct ASftBatchedHiddenOutput" in provider,
      "batched hidden input/output structs present")
check("NativeWgpuBatched" in provider and "ReferencePerExampleFallback" in provider,
      "provider has native and explicit fallback variants")
check("native.forward_hidden_padded_batch" in provider,
      "native provider calls NativeWgpuModel::forward_hidden_padded_batch")
check("pub fn forward_hidden_padded_batch" in native,
      "NativeWgpuModel::forward_hidden_padded_batch API present")
check("hidden_provider: Option<String>" in config,
      "ASftDumpBatchingConfig.hidden_provider present")
check("require_compute_batched_hidden" in config,
      "ASftDumpBatchingConfig.require_compute_batched_hidden present")
check("forbid_per_example_forward" in config,
      "ASftDumpBatchingConfig.forbid_per_example_forward present")

if config_json_path.exists():
    try:
        cfg = json.loads(config_json_path.read_text(encoding="utf-8"))
        dump = cfg["a_sft_native_contract"]["dump_batching"]
        check(dump.get("hidden_provider") == "native_wgpu_padded_hidden",
              "native_dump config hidden_provider=native_wgpu_padded_hidden")
        check(dump.get("require_compute_batched_hidden") is True,
              "native_dump config require_compute_batched_hidden=true")
        check(dump.get("forbid_per_example_forward") is True,
              "native_dump config forbid_per_example_forward=true")
    except Exception as exc:
        FAILURES.append(f"config json parse/contract failed: {exc}")
else:
    FAILURES.append("missing native dump config json")

print("SFT-GPU-8F static validation")
print(f"PASS count: {len(PASSES)}")
for item in PASSES:
    print(f"[PASS] {item}")
if FAILURES:
    print(f"FAIL count: {len(FAILURES)}")
    for item in FAILURES:
        print(f"[FAIL] {item}")
    sys.exit(1)
print("[PASS_STATIC] SFT-GPU-8F compute-level batched hidden provider seal")
