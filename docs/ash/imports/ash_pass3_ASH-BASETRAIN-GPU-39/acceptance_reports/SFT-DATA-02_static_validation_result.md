# SFT-DATA-02 Static Validation Result

- [x] module exists
- [x] test exists
- [x] lib exists
- [x] report exists
- [x] module bracket balance
- [x] test bracket balance
- [x] lib bracket balance
- [x] lib pub mod added
- [x] lib pub use added
- [x] module contains AshSftDatasetPackFilesystemLayout
- [x] module contains AshSftAtlasCheckpointSafetensorsRef
- [x] module contains AshSftAtlasCheckpointLock
- [x] module contains AshSftDatasetPackWriterConfig
- [x] module contains AshSftDatasetPackWriterInput
- [x] module contains AshSftDatasetPackWritePlan
- [x] module contains AshSftDatasetPackWriterReport
- [x] module contains build_sft_dataset_pack_writer_plan
- [x] module contains allow_dataset_pack_filesystem_write
- [x] module contains allow_atlas_checkpoint_safetensors_write
- [x] module contains allow_atlas_checkpoint_manifest_as_ssot
- [x] module contains allow_native_dump_execution
- [x] module contains allow_sft_training_execution
- [x] module contains safetensors_path.ends_with(".safetensors")
- [x] module contains manifest_is_metadata_only
- [x] module contains is_atlas_checkpoint_ssot
- [x] test contains sft_data_02_builds_dataset_pack_writer_plan_without_writing_files
- [x] test contains sft_data_02_binds_safetensors_as_atlas_checkpoint_ssot
- [x] test contains sft_data_02_rejects_manifest_as_checkpoint_ssot
- [x] test contains sft_data_02_rejects_non_safetensors_checkpoint_path
- [x] test contains sft_data_02_rejects_filesystem_write_flag
- [x] test contains sft_data_02_rejects_safetensors_write_and_native_dump_flags
- [x] test contains sft_data_02_rejects_path_traversal_dataset_root
- [x] test contains sft_data_02_deterministic_writer_plan_and_checkpoint_lock
- [x] report contains PASS_CANONICAL_DATASET_PACK_WRITER_FILESYSTEM_LAYOUT_SEAL
- [x] report contains Atlas checkpoint SSOT must be `.safetensors`
- [x] report contains Does not write dataset files
- [x] report contains Does not write safetensors checkpoints
- [x] report contains native_dump_execution_allowed = false

## Status
PASS_SFT_DATA_02_STATIC_VALIDATION

## Note
cargo/rustc are unavailable in this environment; this is a static file/export/seal validation only.
