crates/burn_webgpu_backend/src/base_train_atlas_wave_02_r5_abi.rs
  add RopePairingLayout
  add dedicated RopeParams
  validate convention-derived params

crates/burn_webgpu_backend/src/base_train_atlas_wave_02_r5_staged_prefill.rs
  select exact RoPE pipeline from sealed authority
  preserve unequal Q/K dispatch domains

crates/burn_webgpu_backend/src/shaders/base_train_atlas_wave_02_r5_rope_neox_half_split.wgsl
  implement half-split pairing

crates/burn_webgpu_backend/src/shaders/base_train_atlas_wave_02_r5_rope_interleaved_adjacent.wgsl
  retain adjacent layout as explicit counterfactual/control

crates/orchestrator_local/src/base_train_atlas_wave_02_r5_cli_registry.rs
  register R5-R5 gate args

crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r5_physical_gate.rs
  add R5-R5 branch and receipt publication

crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r5_r5_external_rope_gate.rs
  dedicated executable wrapper

specs/fixtures/ash_basetrain_atlas_wave_02_r5_r5_checkpoint_config.json
specs/fixtures/ash_basetrain_atlas_wave_02_r5_r5_rope_convention_registry_v1.json
specs/fixtures/ash_basetrain_atlas_wave_02_r5_r5_external_source_evidence.json
specs/fixtures/ash_basetrain_atlas_wave_02_r5_r5_known_vector.json
specs/cli/ash_basetrain_atlas_wave_02_r5_r5.args
```

---

# 26. Static closure checks

The static validator requires at least:

```text
ModelSpec has pairing_layout field
ModelSpec has rotary_dim field
sequence authority transcript includes pairing layout
geometry digest includes convention digest
backend ABI has explicit pairing enum
NeoX WGSL uses lane_b = lane_a + rotary_dim/2
interleaved WGSL uses lane_a = 2*pair_index
both shaders derive exponent from pair index
Q and K width bases remain distinct
CPU reference has explicit exhaustive layout match
known-vector fixture contains position zero and one
known-vector expected NeoX and interleaved outputs differ
config theta is parsed from evidence bytes
CLI has no authoritative theta or pairing option
production admission remains deny
proof ledger remains HOLD
R6 remains BLOCKED
```

Static closure is necessary but not sufficient.

---

# 27. Physical admission matrix

| Surface | Required state |
|---|---|
| Parent R5-R4 GQA physical gate | PASS |
| External config byte binding | PASS |
| External registry resolution | PASS |
| `rope_theta` provenance | PASS |
| Pairing layout authority | PASS |
| NeoX half-split known vector CPU-f64 | PASS |
| NeoX half-split known vector GPU | PASS |
| Interleaved control CPU-f64 | PASS |
| Interleaved control GPU | PASS |
| NeoX/interleaved counterfactual separation | PASS |
| Theta mutation sensitivity | PASS |
| Q unequal head-domain rotation | PASS |
| K unequal head-domain rotation | PASS |
| Q RoPE CPU-f64 parity | PASS |
| K RoPE CPU-f64 parity | PASS |
| Context CPU-f64 parity | PASS |
| Padding exact-zero | PASS |
| Live handoff convention digest | PASS |
| Production checkpoint forward | NOT RUN |
| Production admission | BLOCKED |
| Proof ledger | HOLD |
| R6 | BLOCKED |

---

# 28. Final PASS token

The gate emits exactly:

```text
PASS_ASH_BASETRAIN_ATLAS_WAVE_02_R5_R5_EXTERNAL_ROPE_CONVENTION_AUTHORITY_CHECKPOINT_ROPE_THETA_BYTE_BINDING_ROTARY_PAIRING_LAYOUT_AUTHORITY_NEOX_HALF_SPLIT_INTERLEAVED_ADJACENT_EXPLICIT_SEPARATION_Q_K_UNEQUAL_HEAD_DOMAIN_ROTATION_CPU_F64_EXTERNAL_CONVENTION_PARITY_KNOWN_VECTOR_AND_THETA_MUTATION_COUNTERFACTUAL_REJECTION_LIVE_HANDOFF_CONVENTION_DIGEST_NO_PRODUCTION_ADMISSION_PROOF_LEDGER_HOLD_R6_BLOCKED_SEALED
```

The token is forbidden unless every required receipt is durable and the final manifest digest has been written.

---

# 29. Completion criteria

R5-R5 is complete only when all of the following are true:

```text
1. External config bytes are hashed and locally pinned.
2. `rope_theta` is parsed from those bytes without fallback.
3. Pairing layout is resolved by one versioned registry record.
4. The convention authority seals pair map, frequency formula and signs.
5. ModelSpec, geometry, sequence authority and backend params share one convention digest.
6. NeoX and interleaved layouts have explicit separate implementations.
7. The known vector discriminates the layouts on CPU-f64 and GPU.
8. Theta mutation changes physical output.
9. Q rotates four heads using Q width.
10. K rotates two heads using KV width.
11. Q/K RoPE and context match the external-convention CPU-f64 reference.
12. Padding remains exact zero.
13. The live handoff carries the convention digest without becoming its writer.
14. Production admission remains blocked.
15. Proof ledger remains HOLD.
16. R6 remains blocked.
```

---

# 30. Seal statement

```text
External configuration values are not conventions by themselves.
A matching theta does not prove a matching pair map.
GPU and CPU agreement does not prove checkpoint agreement when they share the same wrong layout.
R5-R5 therefore seals source bytes, family resolution, pair map, frequency schedule, sign convention, physical Q/K rotation, known-vector discrimination, and numerical parity as one lineage.
```
