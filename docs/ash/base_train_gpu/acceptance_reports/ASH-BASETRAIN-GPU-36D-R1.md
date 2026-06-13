# ASH-BASETRAIN-GPU-36D-R1 Acceptance

## Patch

ASH-BASETRAIN-GPU-36D-R1  
Adjacent Window Block Constant Name Buildfix /  
Out Of Range Symbol Rebind No Logic Change Seal

## Verdict

STATIC_BAKE_COMPLETE

## Scope

This patch only rebinds the unresolved Rust constant reference in the 36D adjacent window plan path.

## Fixed Symbol

Replaced:

```txt
BLOCK_ADJ_WINDOW_PLAN_OUTSIDE_READ_RANGE
```

With the existing defined constant:

```txt
BLOCK_ADJ_WINDOW_OUTSIDE_READ_RANGE
```

The status string remains unchanged:

```txt
BLOCKED_ADJACENT_WINDOW_PLAN_OUTSIDE_READ_RANGE
```

## Guard

- No read policy change
- No continuity logic change
- No receipt schema change
- No Cargo dependency added
- No GPU upload
- No full tensor load
- No safetensors mutation
