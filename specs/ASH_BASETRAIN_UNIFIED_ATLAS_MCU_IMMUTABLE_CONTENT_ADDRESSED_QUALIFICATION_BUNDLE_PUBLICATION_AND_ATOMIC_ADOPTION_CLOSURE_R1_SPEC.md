# ASH-BASETRAIN-UNIFIED-ATLAS-MCU-IMMUTABLE-CONTENT-ADDRESSED-QUALIFICATION-BUNDLE-PUBLICATION-AND-ATOMIC-ADOPTION-CLOSURE-R1

## Immutable Content-Addressed Qualification Bundle / Atomic Current Pointer / Crash-Consistent Publication / Previous Authority Preservation / Digest-First Adoption / No Destructive Root Replacement / Exact Bundle Loader Resolution / Rollback-Ready Authority Chain

---

# 0. Revision identity

Revision:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-IMMUTABLE-CONTENT-ADDRESSED-QUALIFICATION-BUNDLE-PUBLICATION-AND-ATOMIC-ADOPTION-CLOSURE-R1`

Parent:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-PHYSICAL-QUALIFICATION-EVIDENCE-TRUTH-AND-BUNDLE-ADOPTION-CLOSURE-R2`

PASS token:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_IMMUTABLE_CONTENT_ADDRESSED_QUALIFICATION_BUNDLE_PUBLICATION_AND_ATOMIC_ADOPTION_CLOSURE_R1`

---

# 1. Purpose

Parent R2 establishes:

`physical execution -> typed evidence -> validated receipt -> validated bundle`.

R1 closes the remaining publication problem:

> How does a validated qualification bundle become the current production authority without deleting the previous valid authority, exposing partially written state, or allowing mutable bundle contents?

Canonical transition:

`Validated R2 Bundle -> Content Address -> Immutable Bundle Directory -> Independent Revalidation -> Atomic Current Pointer Switch -> Production Adoption`.

---

# 2. Center invariant

`Bundle identity = bundle semantic digest`.

`Published bundle = immutable`.

`Production adoption = atomic pointer transition`.

The following are not authority:

- an overwritten production directory;
- deletion of the old root followed by rename;
- a directory called `latest`, `prod`, or `current`;
- filesystem mtime;
- whichever bundle happens to be newest.

---

# 3. Core SSOT separation

Three states are distinct:

`Materialized Candidate Bundle != Published Immutable Bundle != Currently Adopted Bundle`.

Authority chain:

`R2 candidate root -> publication validation -> bundles/<bundle_digest>/ -> current.json -> production loader`.

The R2 candidate root may continue to be regenerated. It is not production-current authority.

---

# 4. Scope

R1 owns:

- content-addressed bundle identity;
- immutable bundle directory publication;
- atomic current-pointer adoption;
- previous-current preservation;
- crash-consistent adoption ordering;
- duplicate bundle idempotence;
- bundle reopen and digest validation;
- pointer schema and pointer digest;
- current-pointer loader resolution;
- stale/current mismatch rejection;
- partial publication rejection;
- rollback-ready previous-authority preservation;
- concurrent adoption serialization;
- publication/adoption receipts;
- one-current-bundle production receipt rebinding;
- legacy/bundle mixed-authority rejection.

---

# 5. Explicit non-goals

R1 does not:

- rerun R6/R7/R8/R8A qualification;
- change physical evidence predicates;
- change Muon arithmetic;
- change R8 policy or expert cost;
- enable production training Waves;
- enable ActiveAsync;
- retire exact waits;
- change Atlas lease identity;
- add remote/cloud artifact replication;
- implement automatic quality-regression rollback;
- garbage-collect valid historical bundles;
- add hardware Tensor Core expert execution.

---

# 6. Canonical qualification root

`<mcu-qualification-root>/`

Required layout:

```text
<mcu-qualification-root>/
  bundles/
    <bundle_digest_A>/
      qualification_bundle_manifest.json
      r6/
      r7/
      r8/
      r8a/
      publication_seal.json
    <bundle_digest_B>/
      ...
  current.json
  publication/
    adoption_receipts/
  .staging/
```

`.staging/` is never production-adoptable.

---

# 7. Bundle path authority

Final path:

`bundles/<bundle_digest>/`

where `<bundle_digest>` is the validated R2 semantic bundle digest.

The path is derived from content identity, not from run date or human label.

---

# 8. No arbitrary semantic final names

Forbidden as authority names:

- `latest/`
- `new/`
- `prod/`
- `pass/`
- `qualification_final/`
- timestamp-only directories.

Human-readable metadata may exist inside a bundle but does not define identity.

---

# 9. Bundle digest semantics

`bundle_digest` is the R2 semantic bundle digest.

It is not automatically:

- ZIP SHA-256;
- directory byte-order hash;
- filesystem metadata hash;
- timestamp hash.

---

# 10. Immutable final bundle

Once `bundles/<bundle_digest>/` is published, its semantic contents are immutable.

Forbidden:

- rewrite one receipt;
- replace one evidence file;
- patch manifest in place;
- change a semantic field while preserving directory name;
- overwrite the entire final bundle directory.

Any semantic change creates a new bundle digest.

---

# 11. Existing identical bundle

If `bundles/<bundle_digest>/` already exists:

1. reopen it;
2. validate the publication seal;
3. validate semantic inventory;
4. validate the complete R2 bundle;
5. require the path digest to match the bundle digest.

If valid, publication is idempotent: `IDEMPOTENT_EXISTING_BUNDLE`.

If invalid, fail with `E_MCU_BUNDLE_R1_EXISTING_CONTENT_ADDRESS_CORRUPT`.

No repair-in-place is permitted.

---

# 12. Content-address collision rule

Same digest plus different semantic content is fatal.

No overwrite, no newest-wins, no recovery by copying from another bundle.

---

# 13. Publication staging

A candidate is copied into:

`.staging/<publication_attempt_id>/`.

Only the exact R2 semantic file set is admitted. Unknown semantic files, symlinks, reparse-point redirects, device nodes, or unsupported filesystem entries are rejected.

---

# 14. Staging requirements

Before final immutable publication:

- all mandatory R2 files exist;
- optional E2 receipt/evidence cardinality is valid;
- every receipt/evidence pair validates;
- R2 bundle digest recomputes;
- semantic file hashes are computed;
- publication seal is created;
- staged bytes are reopened and revalidated.

---

# 15. No staging adoption

`current.json` must never point beneath `.staging/`.

The pointer schema only admits `bundles/<exact_digest>`.

---

# 16. Publication seal

`publication_seal.json` binds:

- publication schema/revision;
- R2 parent revision;
- exact bundle digest;
- Native CF1 authority digest;
- executable SHA-256;
- Cross-Release parent digest;
- device capability digest;
- fixture-plan digest;
- semantic file inventory digest;
- semantic file count;
- immutable-publication declaration;
- seal digest.

---

# 17. Semantic inventory

The inventory is constructed from the exact R2 generated semantic files present in the candidate.

Mandatory baseline:

- `qualification_bundle_manifest.json`
- R6 qualification receipt + R6 physical evidence
- R7 E1 qualification receipt + E1 physical evidence
- R8 qualification receipt + replay evidence + homogeneous physical evidence
- R8A qualification receipt + heterogeneous physical evidence.

Optional only as a valid pair:

- R7 E2 qualification receipt;
- R7 E2 physical evidence.

---

# 18. Unknown semantic injection

Unexpected files are not silently admitted into a production bundle.

The publication implementation compares the actual regular-file inventory to the exact expected R2 set plus `publication_seal.json` after sealing.

---

# 19. Publication sequence

Canonical order:

1. load and validate R2 candidate bundle;
2. validate current binary compatibility;
3. validate current device capability for adoption;
4. derive `bundles/<bundle_digest>/`;
5. reuse only if an existing target fully validates;
6. copy exact semantic files into root-local staging;
7. reopen and validate staged R2 content;
8. construct and write publication seal;
9. reopen and validate staging + seal;
10. rename staging directory into `bundles/<bundle_digest>/`;
11. reopen the published immutable bundle;
12. revalidate it;
13. construct candidate current pointer;
14. atomically replace `current.json`;
15. reopen current pointer;
16. resolve exact bundle;
17. revalidate adopted bundle;
18. emit adoption receipt.

---

# 20. Critical ordering

Immutable bundle publication must precede pointer switch.

A pointer may never reference a future or absent target.

---

# 21. Previous-current preservation

Before the pointer switch, current production authority is untouched.

If new publication fails, the previous current pointer remains current.

---

# 22. No destructive production root replacement

Forbidden production topology:

`delete current/final root -> rename new staging into its place`.

R1 production authority is `current.json`, not a mutable final directory.

The parent R2 candidate-output directory may remain an ephemeral candidate materialization surface and is not treated as production current authority.

---

# 23. Crash case A

Crash before immutable publication:

- current pointer unchanged;
- staging remains non-adoptable;
- no production authority changed.

---

# 24. Crash case B

Crash after immutable publication but before pointer switch:

- old current remains current;
- new bundle exists but is unadopted;
- no corruption is inferred.

---

# 25. Crash case C

Crash during pointer replacement must leave either:

- the old complete pointer; or
- the new complete pointer.

Partially rewritten `current.json` is forbidden.

---

# 26. Atomic current pointer

`current.json` is never modified in place.

Write protocol:

`create_new temporary file -> write -> sync -> atomic replace/rename -> reopen`.

Windows uses `MoveFileExW(MOVEFILE_REPLACE_EXISTING | MOVEFILE_WRITE_THROUGH)`.

Non-Windows uses same-directory atomic rename semantics.

---

# 27. Pointer schema

`McuQualificationCurrentPointerR1` contains:

- schema version;
- publication revision;
- bundle digest;
- `bundles/<digest>` relative path;
- publication seal digest;
- Native CF1 authority digest;
- executable SHA-256;
- device capability digest;
- previous bundle digest;
- monotonic pointer generation;
- pointer digest.

---

# 28. Relative-path rule

Only a normalized relative path exactly matching:

`bundles/<bundle_digest>`

is accepted.

Absolute paths, `..`, prefix escape, and arbitrary child paths are rejected.

---

# 29. Pointer digest

Semantic pointer digest excludes:

- mtime;
- temporary filename;
- absolute root path;
- host PID.

It includes all semantic authority fields.

---

# 30. Pointer generation

Every actual current transition increments `pointer_generation` monotonically.

Genesis adoption begins at generation 1.

---

# 31. Generation is not bundle identity

A historical immutable bundle may be explicitly re-adopted at a later pointer generation without changing its bundle digest.

---

# 32. Previous bundle binding

Every non-genesis current pointer records the previously current bundle digest.

This creates explicit adoption lineage.

---

# 33. Previous digest is not automatic rollback

Recording previous authority never causes automatic rollback.

R1 remains fail-closed.

---

# 34. First adoption

No previous pointer is valid genesis state.

`previous_bundle_digest = None`.

---

# 35. Current pointer validation

Loader validates:

- pointer schema;
- pointer revision;
- pointer digest;
- digest syntax;
- exact relative path;
- path containment below `bundles/`;
- target existence;
- publication seal;
- R2 bundle;
- current binary/device constraints supplied by caller.

---

# 36. Pointer/path mismatch

`bundle_digest=AAA` with `bundle_relative_path=bundles/BBB` is rejected by `E_MCU_BUNDLE_R1_CURRENT_POINTER_PATH_DIGEST_MISMATCH`.

---

# 37. Missing bundle

A valid-looking pointer whose target is absent fails with `E_MCU_BUNDLE_R1_CURRENT_BUNDLE_MISSING`.

No filesystem scan fallback is allowed.

---

# 38. Corrupt current bundle

A pointer target that exists but fails seal/R2/inventory validation is `E_MCU_BUNDLE_R1_CURRENT_BUNDLE_CORRUPT`.

No silent previous-bundle fallback.

---

# 39. Why silent rollback is forbidden

Silent fallback would make requested/adopted authority differ from actual authority without an explicit authority transition.

---

# 40. Explicit rollback readiness

Because historical bundles are immutable and retained, rollback is an explicit new pointer generation targeting a previously validated digest.

---

# 41. Publication attempt identity

A publication attempt uses a non-semantic attempt ID derived from bundle digest plus process/time nonce material.

Attempt identity never changes bundle semantic identity.

---

# 42. Attempt nonce semantics

Attempt identity only separates retries/concurrency. It is not a PASS predicate and does not enter the R2 bundle digest.

---

# 43. Publication/adoption locking

One qualification root admits one current-pointer adoption transaction at a time.

A create-new lock file is fail-closed when another publisher owns the transaction boundary.

---

# 44. Lock scope

The lock protects:

- current generation read;
- publication/adoption decision;
- pointer generation increment;
- atomic pointer transition.

It does not redefine GPU qualification scheduling.

---

# 45. Concurrent new bundles

Different immutable bundles may coexist. Current adoption remains serialized.

---

# 46. Lost-update prevention

An optional expected pointer generation can be supplied.

If actual generation differs, reject with `E_MCU_BUNDLE_R1_CURRENT_POINTER_GENERATION_CONFLICT`.

No hidden overwrite.

---

# 47. Retry after conflict

Caller may reopen current authority and explicitly retry using the new generation.

---

# 48. Same-bundle re-adoption

If current already points to the requested bundle, return `NOOP_ALREADY_CURRENT` without incrementing pointer generation.

---

# 49. Idempotent publication

Repeated publication of one valid digest creates only one immutable `bundles/<digest>/` object.

---

# 50. Adoption receipt

`McuQualificationBundleAdoptionReceiptR1` records:

- status (`ADOPTED` or `NOOP_ALREADY_CURRENT`);
- bundle/seal digests;
- pointer generation before/after;
- previous bundle digest;
- whether immutable publication occurred or an existing bundle was reused;
- final-bundle revalidation;
- atomic pointer switch observation;
- pointer reopen validation;
- adopted-bundle reopen validation;
- destructive replacement count;
- training/optimizer/checkpoint/N2 mutation counts;
- receipt digest.

---

# 51. Adoption receipt is a consequence

An `ADOPTED` receipt is emitted only after current pointer replacement and post-switch resolution/revalidation.

---

# 52. No precomputed PASS receipt

The adoption receipt may not be finalized before pointer transition.

---

# 53. Adoption receipt storage

Recommended runtime path:

`publication/adoption_receipts/<receipt_digest>.json`.

The file is audit history, not current SSOT.

---

# 54. Adoption history is not current authority

Current authority remains `current.json`.

Historical receipts explain transitions only.

---

# 55. Loader API

Canonical API:

`load_current_mcu_qualification_bundle_r1(root, expected_binary, expected_device, require_e2)`.

Return type is `ValidatedCurrentMcuQualificationBundleR1` containing pointer, publication seal and validated R2 bundle.

---

# 56. Loader sequence

`read current -> validate pointer -> canonicalize target -> enforce bundles-root containment -> validate publication seal -> validate R2 bundle -> validate optional binary/device authority -> return typed object`.

---

# 57. No directory scanning fallback

Forbidden:

- scan `bundles/` and choose newest;
- choose lexically highest digest;
- choose highest mtime;
- choose first bundle that validates.

---

# 58. Current executable binding

When production/adoption requires exact binary identity, adopted bundle `base_train_binary_sha256` must match the current executable.

Failure: `E_MCU_BUNDLE_R1_CURRENT_BINARY_AUTHORITY_MISMATCH`.

---

# 59. Device binding

Publication/adoption checks the current qualified subgroup32 + SHADER_F16 capability digest against the R2 bundle.

Production R7 still binds its actual active Device capability before low-precision execution.

---

# 60. Expert qualification preservation

P1 does not modify R7 expert qualification, R8 policy or R8A physical execution evidence.

It selects one immutable transaction containing them.

---

# 61. No receipt copying into mutable current directory

Forbidden:

```text
current/
  r6_receipt.json
  r7_receipt.json
```

`current.json` is a pointer, not a copy of child evidence.

---

# 62. One-bundle SSOT

All production child qualification paths in bundle mode resolve from one current pointer and one immutable bundle.

---

# 63. Cross-bundle child mixing forbidden

Production may not combine R6 from bundle A, R7 from bundle B, R8 from bundle C, or manually supplied paths with bundle-current paths.

---

# 64. Historical retention

R1 does not automatically delete superseded valid bundles.

---

# 65. Retention purpose

Historical immutable bundles support audit, explicit rollback, regression comparison and authority lineage.

---

# 66. Garbage collection

Automatic GC is outside R1.

A later GC must never delete current or explicitly retained rollback authorities.

---

# 67. Orphan staging

Staging is non-adoptable. Cleanup may be implemented separately without changing qualification truth.

---

# 68. Published but unadopted bundles

A valid immutable bundle may exist without being current. This is a legitimate state.

---

# 69. Filesystem durability boundary

R1 writes and syncs semantic files/pointers where supported and uses namespace transition only after completed writes.

It does not claim stronger physical disk durability than the host filesystem actually provides.

---

# 70. Windows compatibility

Atomic pointer replacement must not assume POSIX rename-over-existing behavior.

Windows uses `MoveFileExW` with replace-existing and write-through flags.

---

# 71. Same-volume publication

P1 staging resides below the qualification root itself, while final bundles reside below the same root. Atomic directory publication is therefore same-root/same-volume by construction.

---

# 72. Path traversal rejection

Pointer authority rejects parent traversal, absolute paths, drive/UNC escape and paths not exactly equal to the digest-derived bundle path.

---

# 73. Symlink/reparse-point policy

Semantic bundle roots and files are not allowed to redirect through symlink/reparse-point authority in R1.

---

# 74. Immutable meaning

Immutability is enforced semantically by refusal to overwrite an existing content-addressed bundle.

Filesystem ACL hardening may be added independently.

---

# 75. Tamper detection

External mutation of a published file invalidates either semantic inventory digest, publication seal, child receipt/evidence digest, or R2 bundle validation.

---

# 76. No self-healing mutation

Loader does not repair tampered content from staging, caches or another bundle.

---

# 77. Pointer tamper detection

Pointer field changes require a valid pointer digest and still trigger full target revalidation.

---

# 78. No timestamp freshness authority

Currentness comes only from the validated current pointer.

---

# 79. Adoption CLI

Explicit existing-bundle adoption:

`--adopt-unified-atlas-mcu-qualification-bundle-r1 <bundle_digest>`

with:

`--mcu-qualification-root <path>`.

---

# 80. Combined publish-and-adopt CLI

Combined orchestration:

`--publish-and-adopt-unified-atlas-mcu-qualification-bundle-r1`

requires:

- `--mcu-qualification-candidate-bundle-root <R2 candidate>`;
- `--mcu-qualification-root <production qualification root>`.

Optional conflict guard:

`--mcu-qualification-expected-pointer-generation <n>`.

Typed publication and adoption states remain separate internally.

---

# 81. Separate authority boundary

Internal functions remain separate:

- `publish_mcu_qualification_bundle_r1`;
- `adopt_existing_mcu_qualification_bundle_r1` / adoption transaction;
- `load_current_mcu_qualification_bundle_r1`.

---

# 82. Publication state semantics

Logical progression:

`Staging -> Validated -> PublishedImmutable -> RevalidatedPublished -> AdoptionPending -> Adopted`.

A staging candidate may never jump directly to adopted authority.

---

# 83. No illegal transition

No pointer switch is allowed before final immutable bundle validation.

---

# 84. Failure after immutable publication

If immutable publication succeeds but pointer adoption fails, the new bundle remains valid but unadopted and current authority remains unchanged.

---

# 85. Failure after pointer switch

If the pointer switches but post-switch validation or adoption receipt persistence fails, report a hard error. Do not silently roll back the pointer.

---

# 86. Post-switch validation

Atomic pointer replacement proves namespace transition only. It does not prove target validity. Reopen and resolve are mandatory.

---

# 87. Typed current authority

`ValidatedCurrentMcuQualificationBundleR1` is the canonical loaded authority object.

---

# 88. No arbitrary downstream child selection in bundle mode

Bundle mode first resolves the current bundle. Child receipt paths are derived from that exact bundle only.

---

# 89. Production runtime SSOT transition

Bundle-mode environment:

`ASH_UNIFIED_ATLAS_MCU_QUALIFICATION_ROOT_R1=<root>`.

At Production Muon runtime construction, P1 resolves and validates `current.json`, then derives the exact R6/R7/R8/R8A receipt paths from that bundle before those authorities are constructed.

---

# 90. Compatibility bridge

Existing child authority implementations currently consume individual receipt-path environment variables.

R1 may bridge the validated current bundle into those existing loaders only from one centralized binding point.

This bridge does not permit user-supplied child-path mixing.

---

# 91. Mixed authority rejection

If bundle mode is requested while a caller already supplies non-bundle individual qualification receipt paths, fail with:

`E_MCU_BUNDLE_R1_MIXED_QUALIFICATION_AUTHORITY`.

If bundle mode was already centrally bound in the same process, existing child variables must exactly equal the current bundle-derived paths.

---

# 92. Authority mode declaration

Central bundle binding sets:

`ASH_UNIFIED_ATLAS_MCU_QUALIFICATION_AUTHORITY_MODE=IMMUTABLE_CURRENT_BUNDLE_R1`.

This identifies the compatibility bridge as bundle-owned rather than caller-owned legacy path selection.

---

# 93. Publication telemetry minimum

Required semantic facts include:

- immutable bundle published or valid existing bundle reused;
- final bundle revalidated;
- current pointer switched or already-current no-op;
- pointer reopened/validated;
- adopted bundle reopened/validated;
- destructive root replacement count = 0;
- training/optimizer/checkpoint/Physical-N2 mutation counts = 0.

---

# 94. Mandatory invariant

`destructive_root_replacement_count = 0`.

An actual adoption requires `atomic_pointer_switch_completed=true`; `NOOP_ALREADY_CURRENT` is the only no-switch success state.

---

# 95. Static validation

Static gate proves at least:

- content-addressed `bundles/<digest>` path;
- no final-bundle overwrite/delete path;
- current pointer schema;
- Windows atomic replacement helper;
- pointer generation conflict detection;
- final published bundle reopen validation;
- post-switch current reopen validation;
- mixed-authority rejection;
- production callsite bundle binding before R6/R7/R8/R8A construction;
- no directory-scan fallback;
- no silent rollback;
- parent R2 candidate materialization semantics remain isolated rather than silently rewritten.

---

# 96. Required Rust tests

Minimum categories:

Content addressing:

- digest-derived path;
- valid existing digest reuse;
- corrupt existing target reject.

Immutability:

- published bundle never overwritten;
- semantic change requires new digest.

Pointer:

- genesis generation 1;
- next adoption increments generation;
- already-current is idempotent;
- path/digest mismatch reject;
- missing target reject.

Concurrency:

- stale expected generation reject;
- adoption serialized.

Path safety:

- `..` reject;
- absolute path reject;
- bundle-root escape reject.

Authority:

- child receipts do not mix across bundles;
- bundle and legacy user authority do not mix;
- current bundle validates before runtime admission.

---

# 97. Failure-injection matrix

Minimum future physical/runtime matrix:

1. fail before staging validation;
2. fail after staging validation;
3. fail before immutable rename;
4. fail after immutable rename;
5. fail before pointer write;
6. fail before pointer replace;
7. pointer generation conflict;
8. corrupt existing content-addressed bundle;
9. corrupt pointer;
10. missing target;
11. tampered R6 evidence;
12. tampered publication seal;
13. cross-bundle child substitution;
14. path traversal;
15. same-bundle republication.

---

# 98. Runtime-generated artifacts

R1 runtime may generate:

- `publication_seal.json`;
- `current.json`;
- adoption receipt JSON;
- immutable R2 bundle copies.

These runtime outputs are not pre-baked implementation artifacts.

---

# 99. Packaging policy

Implementation source ZIP must exclude generated and documentation artifacts, including:

- this specification;
- `specs/` content;
- patch-note Markdown;
- bake manifests;
- generated qualification receipts;
- physical evidence JSON;
- generated qualification bundle manifests;
- generated `publication_seal.json`;
- generated `current.json`;
- generated adoption receipts;
- static-validation output logs/review reports.

Executable source code that implements manifest/artifact concepts remains source and is not removed merely because its Rust filename contains `manifest` or `artifact`.

---

# 100. GitHub publication

GitHub publication for this revision is spec-only unless implementation publication is explicitly requested.

---

# 101. State-mutation exclusion

Publication/adoption must not:

- advance training generation;
- commit optimizer state;
- commit checkpoint;
- write Physical N2;
- mutate R6/R7/R8/R8A evidence;
- modify an immutable published bundle.

---

# 102. PASS semantics

The PASS token means a complete R2-qualified evidence bundle was assigned its semantic content address, published below an immutable digest-derived path, reopened and validated, and adopted only through one atomic current-pointer transition.

It also means:

- previous current authority was preserved until the new target was ready;
- no production bundle was overwritten in place;
- no current authority was inferred from timestamps or directory names;
- no child receipt was mixed across bundles;
- the final pointer was reopened and resolved;
- the adopted target passed complete validation;
- the production Muon receipt compatibility bridge, when bundle mode is selected, derives all child receipt paths from that one current bundle.

---

# 103. PASS does not mean

R1 PASS does not mean:

- new Muon arithmetic qualified;
- production training Wave qualified;
- performance improved;
- automatic rollback enabled;
- GC qualified;
- remote replication qualified;
- ActiveAsync enabled;
- Atlas leases changed;
- R8 policy changed.

---

# 104. Final authority declaration

Before R1:

> A complete R2 evidence bundle can be validated, but production publication still needs a durable distinction between a candidate directory, a published immutable evidence object, and the one currently adopted authority.

After R1:

> Every validated qualification bundle has one immutable content address. Publishing a new bundle never destroys an older valid bundle. A bundle can exist without being current. Current production authority is expressed by one small digest-bound generation-bound pointer. That pointer changes only after the complete immutable target has been independently revalidated. A failed candidate publication cannot erase previous authority. A published-but-unadopted bundle cannot silently become current. A stale concurrent publisher cannot overwrite a newer adoption. In bundle mode, all R6/R7/R8/R8A receipt paths originate from that exact current bundle, and caller-provided mixed child authority is rejected.

---

# 105. Center sentence

> **P0가 “이 PASS는 어느 물리 증거에서 나왔는가”를 봉인했다면, P1은 “그 증거 묶음을 어떻게 현재 권위로 바꾸면서도 이전 권위를 죽이지 않을 것인가”를 봉인한다. 번들은 돌이고, `current.json`만 움직인다.**