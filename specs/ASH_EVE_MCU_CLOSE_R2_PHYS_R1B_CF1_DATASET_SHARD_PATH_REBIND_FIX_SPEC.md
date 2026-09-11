# ASH-EVE-MCU-CLOSE-R2-PHYS-R1B-CF1-DATASET-SHARD-PATH-REBIND-FIX

## Physical dataset-path authority closure

### Problem

PHYS-R1 previously validated seed shards to canonical physical paths but left the original `DatasetShard.path` strings unchanged in the generated v5_48259 manifest.

The runtime `train_data` loader consumes `DatasetShard.path` directly and does not rebase relative paths against the generated manifest location. A projected manifest can therefore pass PHYS-R1 shard-byte validation and later fail in production with Windows `os error 3` when the raw relative path is no longer valid from the runtime working directory.

### Authority law

The generated PHYS-R1 dataset manifest shall publish, for every train/eval/test shard, the exact canonical `resolved_path` already admitted by PHYS-R1 shard evidence.

This is a path-authority correction only:

- shard payload bytes unchanged
- shard ordering unchanged
- split membership unchanged
- shard SHA-256 unchanged
- model lineage unchanged
- tokenizer lineage unchanged

### Historical evidence

The seed manifest remains unchanged and remains provenance evidence. `PhysR1ShardEvidence.manifest_path` retains the original seed path while `resolved_path` remains the physical authority used by the generated manifest.

### Source scope

`crates/base_train/src/eve_mcu_close_r2_physical_campaign_r1.rs`
SHA-256: `e3ff06468fa1bdca43c4658b51f12ef74c178be7129a9b8cff6bac15dd510293`

### Bake identity

Full ZIP SHA-256: `0c0f30782c3e799611766423a8fdcb1d1129216dc639c1e7b8457bede4ef00c0`
Overlay ZIP SHA-256: `22e11546e2015dca2f3c5fcb411f83fe946932717e013299f35971f8eb2bcb18`

### Required re-materialization

After applying this correction:

1. rebuild `base_train`
2. regenerate PHYS-R1 input genesis so the projected dataset manifest is republished with canonical shard paths
3. regenerate R1A fresh source because its cursor binds the dataset-manifest SHA
4. regenerate Native CF1 for the rebuilt binary
5. rerun R1B-CF1 preflight and full A/B/C

No old generated dataset manifest, R1A source receipt, or Native CF1 may be reused across this correction.
