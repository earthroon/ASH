# SFT-GPU-8C Static Validation Result

- [x] ASftPhase exists
- [x] ASftHiddenSourceDecision exists
- [x] decide_a_sft_hidden_source exists
- [x] guard_a_sft_full_checkpoint_teacher exists
- [x] target check avoids slice PartialEq risk
- [x] lib exports hidden source module
- [x] training imports hidden source guard
- [x] direct loop guard before load_full_checkpoint_weights
- [x] direct loop guard before ReferenceModel::from_full_checkpoints
- [x] direct loop refuses full checkpoint fallback for atlas not wired
- [x] smoke phase direct_train
- [x] train_200 phase direct_train
- [x] smoke forbids full teacher in train
- [x] train_200 forbids full teacher in train
- [x] native dump phase native_dump
- [x] native dump allows teacher only in dump
- [x] train_from_features requires manifest

PASS_STATIC 17 / 17
