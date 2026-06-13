# 16AF-G Native FFN Generation Candidate Gate

- commit: 16AF-G
- candidate_wire_present: true
- generation_connected_default: false
- candidate_runtime_enabled: true
- fallback_cpu_reference: true
- parity_pass_required: true
- parity_passed: true
- attention_native: false
- kv_cache_native: false
- pass: true

```json
{
  "attention_native": false,
  "build_gate": "pass_by_user_reported_local_cargo_check",
  "cache": {
    "cached_layers": 14,
    "preupload": true,
    "preupload_ms": 569.0450999999999,
    "total_bytes": 1937768448
  },
  "candidate_runtime_enabled": true,
  "candidate_wire_present": true,
  "commit": "16AF-G",
  "enable_candidate_requested": true,
  "error": null,
  "fallback_cpu_reference": true,
  "generation_connected_default": false,
  "generation_probe": {
    "elapsed_ms": 57776.2077,
    "executed": true,
    "max_new_tokens": 8,
    "output_ids": [
      1,
      2,
      3,
      171,
      246,
      136,
      143,
      175,
      242,
      131,
      132
    ],
    "prompt_ids": [
      1,
      2,
      3
    ],
    "vocab_limit": 256
  },
  "kv_cache_native": false,
  "parity_pass_required": true,
  "parity_passed": true,
  "runtime_gate": "safe_generation_native_ffn_candidate_default_false",
  "summary": {
    "cpu_reference_fallback_preserved": true,
    "default_false_preserved": true,
    "generation_default_connected": false,
    "pass": true
  }
}
```
