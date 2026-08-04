AW02R5R3QueryProjectionDimensionOverflow
AW02R5R3KvProjectionDimensionOverflow
AW02R5R3QueryGeometryMismatch
AW02R5R3KvHeadCountExceedsQueryHeads
AW02R5R3GqaGroupingInvalid
AW02R5R3SelectedLayerOutOfRange
AW02R5R3RopeThetaConversionInvalid
AW02R5R3RmsEpsilonConversionInvalid
AW02R5R3AttentionScaleDerivationInvalid
AW02R5R3IndependentGeometryLiteralDetected
AW02R5R3FixtureSourceMultiplicity
AW02R5R3GqaPhysicalExecutionDeferredToR5R4
AW02R5R3RopePairingAuthorityUnbound
AW02R5R3ProductionAdmissionForbidden
```

Errors must be stable and machine-readable.

---

# 22. Physical gate

Binary:

```text
ash_basetrain_atlas_wave_02_r5_r3_geometry_authority_gate
```

The gate must:

```text
1. Validate R5-R2 lineage artifacts.
2. Build or load one fixture profile.
3. Generate ModelSpec bytes from that profile.
4. Generate checkpoint/header/plan from the same profile.
5. Build AW-00 transaction from the same ModelSpec bytes.
6. Parse checkpoint identity and header.
7. Reconcile header shapes with the ModelSpec.
8. Seal ModelGeometryAuthority.
9. Derive Params from geometry + batch + sequence authority.
10. Validate resident views against geometry.
11. Execute the existing R5 fixture path only after authority closure.
12. Publish geometry receipts.
13. Keep production, GQA physical and RoPE convention authority blocked.
```

The gate must not accept manually supplied geometry CLI fields.

CLI may supply paths, resource limits, epochs and output directories, but not:

```text
vocab size
hidden size
head counts
head dimension
RoPE theta
RMS epsilon
projection dimensions
```

---

# 23. Expected PASS token

```text
PASS_ASH_BASETRAIN_ATLAS_WAVE_02_R5_R3_CHECKPOINT_MODEL_GEOMETRY_AUTHORITY_HEADER_CONFIG_TO_MODELSPEC_BINDING_MODELSPEC_DERIVED_PARAMS_PROJECTION_SHAPE_DERIVATION_FIXTURE_PROFILE_EXPLICIT_ISOLATION_NO_INDEPENDENT_GEOMETRY_LITERAL_GQA_GEOMETRY_STATIC_ONLY_ROPE_PAIRING_UNBOUND_NO_PRODUCTION_ADMISSION_R6_BLOCKED_SEALED
```

The token intentionally does not contain:

```text
GQA_PHYSICAL_PASS
ROPE_CONVENTION_PASS
PRODUCTION_MODEL_PASS
NO_RECEIPT_OVERCLAIM
EVIDENCE_REQUALIFIED
```

---

# 24. Completion criteria

R5-R3 is complete only when all are true:

```text
zero-argument fixture_spec geometry declaration removed
one canonical fixture profile declaration remains
fixture checkpoint derived from fixture profile
fixture ModelSpec derived from fixture profile
fixture batch derived from fixture profile
atlas counts and byte lengths derived from tensor shapes
AW-00 and AW-02 consume byte-identical ModelSpec source
ModelSpec digest parity proven
Params created only through derive()
attention scale derived from head_dim
resident Q/K/V shapes checked independently
hidden == KV heads × head_dim removed from generic validation
GQA represented without physical-pass claim
RoPE pairing explicitly unbound
production admission explicitly false
prior artifacts immutable
```

---

# 25. Explicit non-goals

R5-R3 does not:

```text
execute a real GQA model
change Q-head to KV-head mapping
prove KV stride correctness
select split-half or interleaved RoPE
compare against Hugging Face or another external implementation
replace literal backend event counters
repair the proof-ledger failure-recording structure
expand the 128 negative-control matrix
repair repository-wide legacy WGSL
admit Headwise training authority
admit TensorCube Stage10
admit loss, backward or optimizer
```

---

# 26. Next patch

The next patch is:

```text
ASH-BASETRAIN-ATLAS-WAVE-02-R5-R4

GQA Physical Geometry Authority /
Unequal Query·KV Head Profile /
Distinct Q·K·V Projection Width /
KV Buffer Stride Closure /
Q-Head To KV-Head Mapping /
Resident K·V Shape Adoption /
CPU-f64 GQA Numerical Parity /
No Production Admission Seal
```

R5-R4 may begin only after R5-R3 proves that all geometry reaches the backend through one authority chain.

---

# 27. Final seal

```text
R5-R3 seals the direction of geometry authority.

Model geometry is authored once in the canonical ModelSpec source.
Checkpoint header shapes are physical witnesses, not substitute configuration.
Params are derived transport, not configuration authority.
Resident tensor shapes follow Q and KV projection dimensions independently.
Fixture literals are isolated to one explicit synthetic profile.
GQA is representable but not yet physically admitted.
RoPE parameters are bound, while pairing convention remains unbound.
Production model admission remains sealed.
```
