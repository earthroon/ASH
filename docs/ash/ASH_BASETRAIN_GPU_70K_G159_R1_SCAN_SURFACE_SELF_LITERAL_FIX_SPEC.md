# ASH-BASETRAIN-GPU-70K-G159-R1

## Scan Surface Self Literal Exclusion / Repeated Forward Plan Predicate Unblock / No Runtime Semantics Change

PatchId: `ASH-BASETRAIN-GPU-70K-G159-R1`  
SourcePatchId: `ASH-BASETRAIN-GPU-70K-G159`

## Problem

G159 received valid G158 evidence and valid CLI input, but stopped before repeated forward smoke planning.

The runtime receipt showed:

```text
previous_g158_accepted=true
smoke_mode=RepeatedDefaultRouteForwardSmoke
completion_mode=Hold
repeat_count=3
repeated_default_route_forward_smoke_plan_created=false
```

The issue was a local scan surface false positive. The module scanned its own pattern declaration area, so the mutation-clean predicate stayed closed even though the runtime input evidence was valid.

## Fix

G159-R1 keeps runtime semantics unchanged and adds a scan-surface sanitizer:

```text
strip_forbidden_pattern_table(content)
```

The scanner removes the local pattern declaration block from the scanned surface before evaluating runtime surface hits.

## Preserved Semantics

```text
RuntimePassTarget unchanged
repeat_count=3 requirement unchanged
completion_mode=Hold unchanged
repeated default route forward smoke semantics unchanged
completion claims remain blocked
checkpoint/safetensors/base weight mutation remains blocked
optimizer/backward/gradient mutation remains blocked
route pointer rewrite/reswitch remains blocked
```

## Acceptance

```text
pattern declaration block excluded from local scan surface
self-literal false positive removed
repeated forward plan predicate can open from valid G158 evidence
output artifact count remains 8
zip excludes artifacts, operator_approval directory, .ps1, .py, .sha256
```
