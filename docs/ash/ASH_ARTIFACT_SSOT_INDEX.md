# ASH Artifact SSOT Index

## BaseTrain GPU

Current imported local source:

$src

## Imported sections

- docs/ash/base_train_gpu/specs
- docs/ash/base_train_gpu/patch_reports
- docs/ash/base_train_gpu/acceptance_reports
- docs/ash/base_train_gpu/artifacts

## ZIP Policy

Future ASH baked ZIPs should include only:

- crates/
- specs/
- sidecars/
- vendor_fork_scaffold/
- apps/
- Cargo.toml / Cargo.lock / rust-toolchain
- selected JSON/debug artifacts required for execution

All other accumulated markdown reports, manifests, reviews, handoff documents, and acceptance evidence should be stored in this GitHub repository.
