# ASH-BASETRAIN-BT-STRUCTURAL-MEDUSA-HEADS-06B-R3

## Full Response Authority Deconfliction / R01 Canonical Token Authority Preservation / Legacy R6 Fixture Token Flags Retirement / R06A Runtime Sequence Override Single Bridge Seal

> Parent code: `BT-STRUCTURAL-MEDUSA-HEADS-06B-R2`
>
> Failure evidence: `BTKoreanIngressDualTokenAuthority`
>
> Repair class: response-file authority closure only
>
> Code algorithm/WGPU/head math change: none
>
> Proof ledger: `HOLD`

## 1. Root cause

`ash_basetrain_structural_medusa_heads_06b_full.args` combined two incompatible token-authority surfaces in one flattened invocation:

```text
R01 canonical Korean source -> tokenizer authority
+
legacy generic R6 fixture flags:
  --token-ids 1..32
  --row-valid-lengths 32
  --position-ids 0..31
```

R01 correctly rejects any generic `--token-ids` while `korean_text_tokenizer_v1` is canonical and raises `BTKoreanIngressDualTokenAuthority`.

The generic R6 fixture fields are unnecessary in 06B because R6R6 already supports the exact runtime sequence override generated from R06A ancestry:

```text
--r6-r6-runtime-sequence-override-file
workspace/runtime/basetrain/structural_medusa_heads/06b/r06a_runtime_sequence_override.json

--require-r6-r6-runtime-sequence-override
true
```

When the override is present, R6R6 does not consume the generic fixture token/valid-length/position fields.

## 2. Repair

Remove only these key/value pairs from the 06B merged full response file:

```text
--token-ids
1,2,3,...,32

--row-valid-lengths
32

--position-ids
0,1,2,...,31
```

Do not weaken or bypass:

```text
BTKoreanIngressDualTokenAuthority
BTKoreanIngressFixtureAuthorityLeak
```

Do not add a second namespaced fixture authority.

## 3. Single sequence authority flow

After R3:

```text
Korean source file
  -> tokenizer_core normalization/encode
  -> R01 BaseTrainRuntimeInputSequenceAuthority
  -> R02/R03/R04/R05/R06A
  -> R06B writes r06a_runtime_sequence_override.json
  -> R6R6 consumes exact token_ids + row_valid_lengths + position_ids from override
  -> 22-layer decoder
  -> final RMSNorm hidden
  -> structural Medusa heads
```

There is one semantic token authority. The R6R6 override is a bridge of that same authority, not a second authority.

## 4. Required static gates

```text
06b_full generic --token-ids count = 0
06b_full generic --row-valid-lengths count = 0
06b_full generic --position-ids count = 0

r6-r6 runtime override file key count = 1
require r6-r6 runtime override = true

R01 source-file authority remains required = true
R01 fixture-authority separation remains required = true
R01 allow token-id override remains false

06B head/WGPU source files unchanged from R2
R06A target authority source unchanged from R2
```

## 5. Expected physical evidence

R01 must now pass instead of stopping at dual authority:

```text
[bt-korean-ingress-01]
fixture_token_authority_used=0
normalization_owner=tokenizer_core
encode_owner=tokenizer_core
valid_token_count=8
...
PASS_ASH_BASETRAIN_BT_KOREAN_INGRESS_01_...
```

Later R06B must report:

```text
runtime_sequence_override_used=1
runtime_input_sequence_authority_match=1
source_hidden_seq=32
source runtime valid length = 8
```

The legacy synthetic `1..32 / valid=32` fixture must not become the R06B hidden authority.

## 6. Scope seal

R3 changes only:

```text
specs/cli/ash_basetrain_structural_medusa_heads_06b_full.args
```

No Rust source, Q-wave math, structural targets, hidden tap, WGPU GEMM, head initialization, prediction geometry, masks, or training boundary is changed.

## 7. Run

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_structural_medusa_heads_06b_gate `
  -- "@specs/cli/ash_basetrain_structural_medusa_heads_06b_full.args"
```
