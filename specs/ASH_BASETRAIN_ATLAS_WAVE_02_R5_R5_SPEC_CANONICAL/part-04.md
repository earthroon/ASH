The R5-R5 gate executes in this order.

## 16.1 Parent import

1. Read R5-R4 physical manifest.
2. Verify parent manifest digest.
3. Verify parent pass token.
4. Verify GQA geometry and production-block state.

## 16.2 External evidence import

5. Read checkpoint config snapshot bytes.
6. Verify expected config SHA-256 from CLI.
7. Parse JSON without injecting defaults.
8. Canonicalize the relevant RoPE fragment.
9. Read convention registry bytes.
10. Verify registry SHA-256.
11. Resolve exactly one registry record.
12. Read pinned source-evidence descriptor.
13. Verify source-evidence digest.

## 16.3 Authority construction

14. Build `ExternalRopeConventionAuthority`.
15. Seal convention digest.
16. Extend or build ModelSpec.
17. Build geometry authority.
18. Build sequence rope authority.
19. Derive backend RoPE params.
20. Verify full digest parity chain.

## 16.4 Known vector

21. Run CPU-f64 NeoX known vector.
22. Run CPU-f64 interleaved counterfactual.
23. Dispatch GPU NeoX known vector.
24. Dispatch GPU interleaved control pipeline.
25. Verify positive and negative expectations.
26. Run theta mutation control.

## 16.5 GQA physical execution

27. Acquire R5-R4 same-process resident weights.
28. Execute staged prefill with NeoX convention.
29. Read back compact Q/K RoPE surfaces.
30. Build CPU-f64 external-convention reference.
31. Compare all required stages.
32. Verify padding exact-zero.
33. Verify GQA quotient mapping remains active.
34. Verify live handoff convention digest.

## 16.6 Publication

35. Write receipts atomically.
36. Seal final manifest.
37. Emit PASS token only after all files are durable.

---

# 17. Required receipt set

Suggested runtime directory:

```text
workspace/runtime/basetrain/atlas_wave/02/r5/r5/
```

Required receipts:

```text
00_parent_r5_r4_import_receipt.json
01_checkpoint_config_source_receipt.json
02_checkpoint_config_rope_extract_receipt.json
03_rope_registry_source_receipt.json
04_rope_registry_resolution_receipt.json
05_external_source_evidence_receipt.json
06_external_rope_convention_authority.json
07_model_spec_rope_binding_receipt.json
08_geometry_rope_binding_receipt.json
09_sequence_rope_authority_receipt.json
10_backend_rope_params_receipt.json
11_pair_map_receipt.json
12_known_vector_fixture_receipt.json
13_known_vector_cpu_f64_neox_receipt.json
14_known_vector_cpu_f64_interleaved_receipt.json
15_known_vector_gpu_neox_receipt.json
16_known_vector_gpu_interleaved_receipt.json
17_known_vector_counterfactual_rejection_receipt.json
18_theta_mutation_control_receipt.json
19_q_unequal_head_domain_rope_receipt.json
20_k_unequal_head_domain_rope_receipt.json
21_q_rope_parity_receipt.json
22_k_rope_parity_receipt.json
23_context_parity_receipt.json
24_padding_exact_zero_receipt.json
25_live_handoff_rope_convention_receipt.json
26_negative_control_ledger.json
27_positive_proof_ledger.json
28_no_production_admission_receipt.json
29_proof_ledger_hold_receipt.json
30_r6_blocked_receipt.json
31_final_manifest.json
```

Each receipt contains:

```text
patch ID
build revision
parent digest
input digests
selected convention ID
convention digest
pass boolean
receipt digest
```

---

# 18. Positive proofs

Minimum required positive proofs:

## 18.1 Source and authority

```text
R5R5-POS-SRC-000 config bytes digest matches CLI expectation
R5R5-POS-SRC-001 config parses without default injection
R5R5-POS-SRC-002 theta source path recorded
R5R5-POS-SRC-003 registry bytes digest matches
R5R5-POS-SRC-004 exactly one convention record selected
R5R5-POS-SRC-005 external source revision pinned
R5R5-POS-SRC-006 external source evidence digest matches
```

## 18.2 Convention

```text
R5R5-POS-CONV-000 layout == NeoXHalfSplit
R5R5-POS-CONV-001 pair map for D=4 == [(0,2),(1,3)]
R5R5-POS-CONV-002 pair map digest recomputes
R5R5-POS-CONV-003 frequency formula ID exact
R5R5-POS-CONV-004 sign convention ID exact
R5R5-POS-CONV-005 Q=true K=true V=false
```

## 18.3 Theta

```text
R5R5-POS-THETA-000 config f64 theta bits preserved
R5R5-POS-THETA-001 geometry theta bits match
R5R5-POS-THETA-002 sequence authority theta bits match
R5R5-POS-THETA-003 GPU f32 conversion finite
R5R5-POS-THETA-004 GPU f32 conversion positive
R5R5-POS-THETA-005 theta mutation changes known vector
```

## 18.4 Known vector

```text
R5R5-POS-KNOWN-000 position zero identity exact
R5R5-POS-KNOWN-001 CPU-f64 NeoX expected values match
R5R5-POS-KNOWN-002 CPU-f64 interleaved expected values match
R5R5-POS-KNOWN-003 GPU NeoX matches NeoX expected
R5R5-POS-KNOWN-004 GPU interleaved matches interleaved expected
R5R5-POS-KNOWN-005 NeoX and interleaved outputs diverge
```

## 18.5 GQA physical execution

```text
R5R5-POS-GQA-000 Q head count 4
R5R5-POS-GQA-001 K head count 2
R5R5-POS-GQA-002 Q pair dispatch count exact
R5R5-POS-GQA-003 K pair dispatch count exact
R5R5-POS-GQA-004 Q RoPE CPU-f64 parity
R5R5-POS-GQA-005 K RoPE CPU-f64 parity
R5R5-POS-GQA-006 context CPU-f64 parity
R5R5-POS-GQA-007 quotient mapping retained
R5R5-POS-GQA-008 padding exact-zero retained
R5R5-POS-GQA-009 live handoff convention digest exact
```

---

# 19. Negative controls

Minimum required negative controls:

```text
NEG-SOURCE-CONFIG-MISSING
NEG-SOURCE-CONFIG-DIGEST
NEG-SOURCE-REGISTRY-MISSING
NEG-SOURCE-REGISTRY-DIGEST
NEG-SOURCE-EVIDENCE-DIGEST
NEG-SOURCE-UNPINNED-REVISION

NEG-CONFIG-THETA-MISSING
NEG-CONFIG-THETA-NAN
NEG-CONFIG-THETA-ZERO
NEG-CONFIG-THETA-ALIAS-CONFLICT
NEG-CONFIG-MODEL-TYPE-MISSING
NEG-CONFIG-ARCHITECTURE-AMBIGUOUS
NEG-CONFIG-SCALING-UNSUPPORTED

NEG-REGISTRY-ZERO-MATCH
NEG-REGISTRY-DUPLICATE-MATCH
NEG-REGISTRY-UNKNOWN-LAYOUT
NEG-REGISTRY-PAIR-MAP-DIGEST
NEG-REGISTRY-FREQUENCY-ID
NEG-REGISTRY-SIGN-ID

NEG-PAIR-NEOX-AS-INTERLEAVED
NEG-PAIR-INTERLEAVED-AS-NEOX
NEG-PAIR-LANE-OUT-OF-RANGE
NEG-PAIR-DUPLICATE-LANE
NEG-PAIR-ODD-ROTARY-DIM
NEG-PAIR-ZERO-ROTARY-DIM

NEG-THETA-HARDCODED-10000
NEG-THETA-RECEIPT-ONLY-MUTATION
NEG-THETA-GPU-CPU-SOURCE-DIVERGENCE

NEG-Q-USING-KV-HEAD-COUNT
NEG-K-USING-Q-HEAD-COUNT
