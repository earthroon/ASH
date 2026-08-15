# ASH-BASETRAIN-STORAGE-ROOT-AUTHORITY-R1

## Status

Implementation-aligned storage ownership specification inserted before the first N8 long-horizon physical run.

## Patch identity

```text
ASH-BASETRAIN-STORAGE-ROOT-AUTHORITY-R1
```

## Core contract

```text
Hot Runtime Root Authority /
Durable BaseTrain Storage Root Authority /
Runtime State != Durable State /
Explicit Cross-Volume Ownership /

--output-dir Hot Execution Authority /
--basetrain-storage-root Durable Authority /
Explicit Storage Publication Policy /

checkpoints / canonical_parents / receipts / archive Derived Roots /
No CWD-Owned Durable State /
No Repo-Relative Durable Fallback /
No Hidden Storage Fallback /

Windows Volume Identity Admission /
Storage Root Writable Preflight /
Free-Space Preflight /

Cross-Volume Copy-Verify-Publish /
No Cross-Volume Rename Atomicity Assumption /
Streaming Source Digest During Copy /
Destination Physical Rehash /
Same-Volume Final Rename /

N8 GEN13 Durable Checkpoint Publication /
N8 Receipt and R14 Durable Publication /
Training-State Directory Layout Preservation /
No Canonical Parent Promotion Before Resume-Cut /
No CURRENT_BASETRAIN_PARENT Pointer Update /

Existing GEN5 Parent Preservation /
No Automatic GEN5 Migration /
No Source Payload Rewrite /
No Runtime Training-State Rewrite /
No Silent Migration /
No Hidden Fallback
```

---

## 1. Authority split

`--output-dir` remains the hot runtime authority. It owns in-progress BaseTrain state, packed RUN_SLOT data, step receipts, and the physical N8 child state.

`--basetrain-storage-root` is a separate durable authority. For the current workstation this may be configured as `E:\ASH`, but no drive literal is hard-coded in core Rust.

The durable root deterministically derives:

```text
<storage-root>/checkpoints
<storage-root>/canonical_parents
<storage-root>/receipts
<storage-root>/archive
```

Missing or unavailable durable storage must fail closed. The runtime may not silently fall back to the repository, CWD, another drive, or a temp directory.

---

## 2. CLI contract

New options:

```text
--basetrain-storage-root <PATH>
--storage-publication-policy <POLICY>
```

R1 policies:

```text
none
receipts-only
checkpoint
canonical-parent
```

For N8, the admitted policies are:

```text
receipts-only
checkpoint
```

`canonical-parent` is explicitly rejected before Resume-Cut Exact Determinism is proven.

N8 requires an explicit storage root and an explicit admitted publication policy.

---

## 3. Existing GEN5 parent preservation

The promoted GEN5 physical parent remains at its already-bound D-drive run root.

This patch does not move, rewrite, copy-rebind, or synthesize GEN5.

N8 reads GEN5 as immutable source state and writes child runtime state to the N8 `--output-dir`.

Automatic cold migration of GEN5 is out of scope and requires a later explicit migration authority.

---

## 4. Storage preflight

Before N8 execution the storage layer:

1. creates the durable root and derived directories if absent;
2. verifies write access with a create, flush, sync, and delete probe;
3. resolves runtime and durable volume identities;
4. queries available bytes on Windows using `GetDiskFreeSpaceExW`;
5. estimates the durable checkpoint lower-bound from the promoted GEN5 packed payload sizes plus a bounded control reserve;
6. rejects an obviously insufficient target volume.

The preflight records whether runtime and durable roots occupy the same physical volume.

---

## 5. Cross-volume publication semantics

D-to-E publication is never treated as an atomic rename.

The required physical transaction is:

```text
source read
→ destination .partial write
→ source digest during streaming copy
→ destination sync
→ destination physical rehash
→ exact digest comparison
→ same durable volume final rename
```

The destination payload is not admitted merely because `copy` returned success.

For packed payloads, source length and SHA256 must match the authoritative packed-state manifest before publication.

---

## 6. N8 durable checkpoint layout

With publication policy `checkpoint`, a successful GEN13 candidate is published under:

```text
<storage-root>/checkpoints/
  gen000013_opt000013_cursor000083_<run-id>/
```

The durable checkpoint preserves BaseTrain run-state layout:

```text
training_state/
  active_training_state.json
  committed_training_state_step_000013.json
  <active-slot>/
    packed_state_manifest.json
    weights.r6pack
    adam_m.r6pack
    adam_v.r6pack
checkpoint_binding.json
```

This preserves exact RUN_SLOT path semantics without declaring the candidate a canonical parent.

Required identity:

```text
trainingGeneration = 13
optimizerStep = 13
cursorNextBatchOrdinal = 83
canonicalParentPromotion = false
```

---

## 7. Durable receipt publication

The N8 runtime receipts and ledgers are published under:

```text
<storage-root>/receipts/<run-id>/
```

This includes top-level BaseTrain receipt/ledger JSON files and the persistent `r14_long_horizon` step ledger.

The durable storage publication receipt is:

```text
basetrain_storage_publication_receipt.json
```

It records runtime/storage roots and volumes, publication policy, free-space preflight, copied and digest-verified payload accounting, durable receipt/checkpoint counts, source mutation, runtime rewrite, fallback counters, and durable checkpoint/receipt paths.

---

## 8. Publication ordering

Checkpoint and receipt content are first staged in `.partial` directories on the durable volume.

Checkpoint payload publication is finalized by a same-volume rename only after every copied payload has passed digest verification.

The durable receipt publication is finalized after its storage receipt is written.

If final receipt publication fails after the checkpoint rename, the implementation attempts to return the checkpoint to its `.partial` staging identity rather than treating it as committed authority.

No canonical parent pointer is updated in this patch.

---

## 9. N8 integration ordering

The N8 final sequence is:

```text
GEN13 physical state complete
→ N8 physical receipt finalized
→ GEN5 source-parent immutability reverified
→ durable storage publication
→ storage PASS
→ N8 PASS
→ expected Resume-Cut HOLD
```

N8 PASS is not emitted before durable publication succeeds when storage authority is bound.

---

## 10. No canonical promotion

For N8 R1:

```text
canonicalPointerUpdateCount = 0
canonicalParentPromotion = false
```

The directory `<storage-root>/canonical_parents` is reserved but unused for N8.

Only after a later `8 continuous == 4 + reload + 4` exact determinism closure may GEN13 be considered for canonical parent publication.

---

## 11. No double-authority rule

The durable checkpoint is a physical payload owner for the GEN13 candidate.

A later canonical-parent stage must not silently create a second full payload copy without an explicit retention/publication policy. It may instead adopt or reference the verified durable payload under a later authority.

---

## 12. Failure semantics

Any storage-root availability/writability failure, insufficient measured capacity, source size or digest drift, destination digest mismatch, source mutation during copy, publication collision, split-authority drift, hidden fallback, or N8 canonical-parent publication attempt rejects durable publication.

Failure does not synthesize missing state and does not rewrite the GEN5 parent.

---

## 13. PASS token

```text
PASS_ASH_BASETRAIN_STORAGE_ROOT_AUTHORITY_RUNTIME_DURABLE_SPLIT_R1
```

The existing N8 PASS remains separate and is emitted only after storage publication passes.

---

## 14. Expected N8 deployment

Recommended workstation deployment:

```text
Hot runtime:
D:\1111113232\DUST\1\ash_pass3\workspace\base_train_runs\...

Durable BaseTrain storage:
E:\ASH
```

Recommended N8 policy:

```text
--storage-publication-policy checkpoint
```

The N8 runtime remains on D while the verified GEN13 checkpoint and evidence are durably published to E.

---

## 15. Explicit non-goals

R1 does not perform existing GEN5 cold migration, canonical parent promotion, CURRENT_BASETRAIN_PARENT pointer update, archive retention policy, checkpoint dedup/reference counting, resume-cut determinism proof, or crash-recovery V2.
