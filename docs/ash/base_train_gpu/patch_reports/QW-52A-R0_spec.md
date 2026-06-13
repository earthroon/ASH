# QW-52A-R0 Spec

Cheonjiin Structural Probe Library Lift / No Logic Rewrite Seal.

The existing `af16ai6b_cheonjiin_structural_probe.rs` logic is lifted into `model_core::cheonjiin_structural_probe` for reuse by QW-52A-R1/QW-52B without rewriting Cheonjiin or QWave math. The original binary remains as a Rust wrapper. Python is not used for trace, validation, receipt, or state judgment.
