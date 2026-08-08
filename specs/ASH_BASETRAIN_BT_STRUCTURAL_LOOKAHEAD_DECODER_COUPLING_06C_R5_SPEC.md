# ASH-BASETRAIN-BT-STRUCTURAL-LOOKAHEAD-DECODER-COUPLING-06C-R5

## Selected Decoder Gradient Admission / F32 First-Step Mutation Separation / Atlas-Wave Candidate Commit / Ambiguous Error Retirement Seal

Parent: `BT-STRUCTURAL-LOOKAHEAD-DECODER-COUPLING-06C-R4`

Observed physical blocker: `BTStructLookaheadSelectedDecoderGradientMissing` after R01-R06B and full 22-layer parent execution had already passed.

R4 reused the same error string for three distinct states:

1. selected decoder q-projection gradient absent from the backward graph;
2. gradient tensor present but all values zero;
3. gradient present/nonzero and Atlas-Wave candidate committed, but `lr=1e-6` produced no bitwise f32 q-weight change on the first step.

Those states are not semantically equivalent. R5 separates them.

### Required R5 distinctions

```text
BTStructLookaheadSelectedDecoderGradientAbsent
BTStructLookaheadSelectedDecoderGradientZero
BTStructLookaheadGateUpdateNoMutation
```

The selected decoder q gradient must still be present, finite, and nonzero. This is the physical proof that the selected decoder is not frozen.

The first-step q parameter digest is now observational:

```text
CHANGED
or
QUANTIZED_ZERO_FIRST_STEP
```

A `QUANTIZED_ZERO_FIRST_STEP` result does not mean the decoder was frozen. It means the nonzero Atlas-Wave update candidate did not cross the representable f32 parameter ULP for that lane at the current `1e-6` learning rate.

R5 does not synthesize a minimum one-ULP nudge, does not increase the learning rate silently, and does not change the R2 Atlas-Wave SGD formula.

```text
P_candidate = P_parent - learning_rate * dP
```

The structural gate still begins from exact zero and its first-step physical mutation remains required. This proves a live parameter update path while preserving zero-start coupling semantics.

### Receipt additions

```text
selectedDecoderGradientAdmission=true
selectedDecoderGradientPresent=true
selectedDecoderGradientNonzeroCount>0
selectedDecoderPhysicalMutation=<bool>
selectedDecoderMutationVerdict=CHANGED|QUANTIZED_ZERO_FIRST_STEP
```

### Scope

R5 changes exactly one code file:

```text
crates/orchestrator_local/src/base_train_structural_lookahead_decoder_coupling_06c.rs
```

No R01-R06B authority, TensorCube geometry, shared-KV authority, Atlas-Wave update map, DeltaK petrification policy, target causality, or LM-head HOLD boundary is modified.

Physical compile/runtime PASS remains operator-machine evidence.
