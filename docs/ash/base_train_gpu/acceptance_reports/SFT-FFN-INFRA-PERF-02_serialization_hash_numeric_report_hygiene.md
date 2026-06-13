# SFT-FFN-INFRA-PERF-02 Acceptance

## Status

PASS_STATIC / PENDING_LOCAL_RUST_TEST

## Scope

Serialization, hash unification, numeric norm stability, markdown report rendering, and clone allocation hygiene.

## SSOT

- serde_json render digest
- manual JSON render removal digest
- hash unification digest
- legacy hash behavior digest
- stable L2 norm digest
- markdown renderer boundary digest
- clone allocation audit digest

## Confirmed Static Gates

- capability audit JSON uses serde_json rendering.
- manual JSON escaping is removed from capability audit rendering.
- duplicated stable_hash implementations in the targeted files are routed through infra_hash.
- legacy hash behavior is preserved through stable_hash64_legacy / stable_hash_fmt_v2 compatibility.
- stable L2 norm utility is provided.
- finite norm guard utility is provided.
- markdown report rendering boundary is introduced.
- report schema remains preserved.
- clone allocation audit evidence type is recorded.
- public API remains preserved.
- seal id semantics remain preserved.
- runtime attach remains closed.
- promotion apply remains closed.
- current pointer update remains closed.

## Opened

- serde_json audit JSON renderer
- manual JSON escape removal
- hash centralization
- legacy hash behavior fixture
- stable_l2_norm_f32
- stable_l2_norm_f32_checked
- stable_l2_norm_delta_f32
- markdown report renderer boundary
- snapshot/evidence clone audit evidence

## Closed

- capability audit schema semantic change
- legacy digest rewrite
- hash algorithm replacement
- report schema rewrite
- template engine dependency
- runtime attach
- promotion apply
- current pointer update
- slot ready mark
- ASH binding

## Runtime Acceptance Pending

Requires local Rust toolchain execution for cargo test.
