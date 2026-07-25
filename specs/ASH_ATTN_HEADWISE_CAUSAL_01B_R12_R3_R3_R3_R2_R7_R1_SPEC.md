# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R1

## Component-Scoped ABI Revision Ownership /

## Backend·Model-Core Bundle Identity /

## Duplicate and Unknown CLI Argument Rejection /

## Canonical Run Contract Parse Seal

---

## 0. 목적

R7-R1은 kernel 구현이나 성능 정책을 변경하지 않는다.

이번 패치의 목적은 다음 두 가지다.

```text
1. backend와 model_core의 ABI revision 소유권을 분리한다.
2. 실행 인자를 registry 기반으로 엄격하게 파싱한다.
```

R7 실행에서 확인된 상태:

```text
backend ABI
= ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7

model_core ABI
= ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R6-R1
```

R7은 backend kernel과 route policy를 변경했지만 model_core public ABI는 변경하지 않았다.

따라서 두 컴포넌트에 동일한 revision을 요구하는 것은 잘못된 ABI 귀속이다.

실행 명령에서도 다음 결함이 관찰됐다.

```text
R7 옵션 블록 중복
unknown option 무시
last-write-wins
옵션 이름 접착
```

관찰된 접착 토큰:

```text
--gqa2-query-heads-per-workrequire-softmax-numerical-parity
```

---

# 1. Patch identity

```text
patch_id=
ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R1

parent_patch_id=
ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7

runtime_schema=
ash.attn.headwise.causal.01b.r12.r3.r3.r3.r2.r7.r1.runtime_artifact.v1

local_manifest_schema=
ash.attn.headwise.causal.01b.r12.r3.r3.r3.r2.r7.r1.local_manifest.v1

build_revision=
ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R1

backend_public_abi_revision=
ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7

model_core_public_abi_revision=
ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R6-R1

kernel_revision=
ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7

route_policy_revision=
ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7

cli_contract_revision=
ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R1

promotion_scope=
incremental_decode_only
```

변경하지 않는 항목:

```text
attention equations
kernel WGSL
GQA2 tile geometry
candidate registry
cost decomposition
traffic accounting
route LUT
non-inferiority policy
guard math
scratch usage
rollback policy
```

---

# 2. Component-scoped ABI SSOT

필수 component taxonomy:

```rust
pub enum HeadwiseAbiComponent {
    Backend,
    ModelCore,
    KernelSet,
    GuardRuntime,
    RoutePolicy,
    ManifestBuilder,
    InputDigestPolicy,
    CliContract,
}
```

필수 expectation 구조:

```rust
pub struct HeadwiseAbiExpectation {
    pub component: HeadwiseAbiComponent,

    pub expected_revision: &'static str,
    pub observed_revision: &'static str,

    pub source_symbol: &'static str,

    pub compatibility_policy:
        HeadwiseAbiCompatibilityPolicy,

    pub required: bool,
}
```

compatibility policy:

```rust
pub enum HeadwiseAbiCompatibilityPolicy {
    Exact,
    ExplicitAllowList,
}
```

R7-R1 기본값:

```text
Exact
```

금지:

```text
prefix match
revision substring match
semantic-version 추론
다른 component PASS로 누락 component 대체
```

---

# 3. Canonical ABI ownership

## Backend

```text
expected=
ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7

observed=
HEADWISE_ATLAS_01B_PUBLIC_ABI_REVISION
```

## ModelCore

```text
expected=
ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R6-R1

observed=
HEADWISE_ATTENTION_01B_PUBLIC_ABI_REVISION
```

## KernelSet

```text
expected=
ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7
```

## RoutePolicy

```text
expected=
ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7
```

## CliContract

```text
expected=
ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R1
```

---

# 4. Shared revision 제거

금지되는 기존 구조:

```rust
const EXPECTED_PUBLIC_ABI_REVISION: &str =
    "ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7";

ensure!(
    backend_revision == EXPECTED_PUBLIC_ABI_REVISION
);

ensure!(
    model_core_revision == EXPECTED_PUBLIC_ABI_REVISION
);
```

필수 구조:

```rust
const EXPECTED_BACKEND_PUBLIC_ABI_REVISION: &str =
    "ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7";

const EXPECTED_MODEL_CORE_PUBLIC_ABI_REVISION: &str =
    "ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R6-R1";
```

검증:

```rust
ensure!(
    HEADWISE_ATLAS_01B_PUBLIC_ABI_REVISION
        == EXPECTED_BACKEND_PUBLIC_ABI_REVISION,
    "BackendAbiRevisionMismatch: expected={} actual={}",
    EXPECTED_BACKEND_PUBLIC_ABI_REVISION,
    HEADWISE_ATLAS_01B_PUBLIC_ABI_REVISION,
);

ensure!(
    HEADWISE_ATTENTION_01B_PUBLIC_ABI_REVISION
        == EXPECTED_MODEL_CORE_PUBLIC_ABI_REVISION,
    "ModelCoreAbiRevisionMismatch: expected={} actual={}",
    EXPECTED_MODEL_CORE_PUBLIC_ABI_REVISION,
    HEADWISE_ATTENTION_01B_PUBLIC_ABI_REVISION,
);
```

필수 정적 조건:

```text
shared_cross_component_expected_revision_check_count=0
```

---

# 5. Component ABI receipt

```rust
pub struct HeadwiseComponentAbiReceipt {
    pub component: HeadwiseAbiComponent,

    pub expected_revision: String,
    pub observed_revision: String,

    pub source_symbol: String,
    pub compatibility_policy: String,

    pub exact_match: bool,
    pub allow_list_match: bool,

    pub pass: bool,
}
```

필수 조건:

```text
component_receipt_count
=
required_component_count

component_abi_fail_count=0
```

---

# 6. ABI bundle identity

component revision은 서로 달라도 된다.

대신 실제 결합 상태를 하나의 bundle digest로 봉인한다.

```rust
pub struct HeadwiseAbiBundleIdentity {
    pub backend_public_abi_revision: String,
    pub model_core_public_abi_revision: String,
    pub kernel_revision: String,
    pub guard_runtime_revision: String,
    pub route_policy_revision: String,
    pub manifest_builder_revision: String,
    pub input_digest_policy_revision: String,
    pub cli_contract_revision: String,

    pub canonical_serialization: String,
    pub bundle_digest: String,

    pub all_components_pass: bool,
}
```

canonical order:

```text
backend_public_abi_revision
model_core_public_abi_revision
kernel_revision
guard_runtime_revision
route_policy_revision
manifest_builder_revision
input_digest_policy_revision
cli_contract_revision
```

serialization:

```text
field=value\n
```

digest:

```text
SHA-256(canonical serialization)
```

필수 조건:

```text
bundle_member_count=8
bundle_missing_member_count=0
bundle_duplicate_member_count=0
bundle_cross_component_equality_requirement=false
```

---

# 7. Runtime artifact ABI fields

필수:

```text
backend_public_abi_revision
model_core_public_abi_revision
kernel_revision
guard_runtime_revision
route_policy_revision
manifest_builder_revision
input_digest_policy_revision
cli_contract_revision
abi_bundle_digest
```

금지되는 authority field:

```text
production_abi_revision
```

호환 목적으로 유지한다면:

```text
authority=false
deprecated=true
```

를 명시한다.

---

# 8. CLI registry SSOT

모든 인자는 하나의 registry에 귀속한다.

```rust
pub struct HeadwiseCliOptionSpec {
    pub key: &'static str,

    pub value_type:
        HeadwiseCliValueType,

    pub required: bool,

    pub repeat_policy:
        HeadwiseCliRepeatPolicy,

    pub default_value:
        Option<&'static str>,

    pub semantic_group:
        HeadwiseCliSemanticGroup,
}
```

value type:

```rust
pub enum HeadwiseCliValueType {
    Boolean,
    UnsignedInteger,
    SignedInteger,
    Float,
    String,
    CsvUnsignedInteger,
    CsvString,
    Enum(&'static [&'static str]),
    Path,
}
```

repeat policy:

```rust
pub enum HeadwiseCliRepeatPolicy {
    Forbid,
    AllowExactDuplicate,
    Collect,
}
```

R7-R1의 모든 기존 옵션:

```text
repeat_policy=Forbid
```

---

# 9. CLI parsing phases

```rust
pub enum HeadwiseCliParsePhase {
    RawTokenCapture,
    TokenShapeValidation,
    KeyLookup,
    DuplicateDetection,
    ValuePresenceValidation,
    TypeParsing,
    SemanticValidation,
    CanonicalNormalization,
    ContractDigest,
}
```

필수 실행 순서:

```text
raw argv capture
→ token shape validation
→ registry lookup
→ duplicate detection
→ value presence validation
→ typed parse
→ semantic validation
→ canonical normalization
→ contract digest
```

---

# 10. Duplicate argument rejection

금지:

```rust
values.insert(key, value);
```

를 이용한 last-write-wins.

필수:

```rust
if let Some(first) = seen.get(key) {
    return Err(
        DuplicateCliArgument {
            key,
            first_index: first.index,
            duplicate_index: current_index,
            first_value: first.value,
            duplicate_value: value,
        }
    );
}
```

동일 값이 반복돼도 실패한다.

```text
DuplicateCliArgument:
key=--cost-profile-buckets
first_index=<n>
duplicate_index=<m>
```

필수:

```text
duplicate_cli_key_count=0
```

---

# 11. Unknown argument rejection

모든 `--key`는 registry에 존재해야 한다.

```text
UnknownCliArgument:
key=--gqa2-query-heads-per-workrequire-softmax-numerical-parity
token_index=<n>
```

금지:

```text
unknown key 저장 후 무시
unknown key 로그만 출력하고 계속 실행
unknown key를 HashMap에 삽입
```

필수:

```text
unknown_cli_key_count=0
```

---

# 12. Token adhesion detection

탐지 대상:

```text
known key 뒤에 다른 key 이름이 접착됨
token 내부에 추가 "--"가 존재함
값 위치에 option 형태 토큰이 존재함
known key prefix 뒤에 known key suffix가 이어짐
```

예:

```text
--gqa2-query-heads-per-workrequire-softmax-numerical-parity
```

진단:

```text
CliTokenAdhesionDetected:
raw=<token>
probable_left=--gqa2-query-heads-per-workgroup
probable_right=--require-softmax-numerical-parity
token_index=<n>
```

추정 split이 불가능해도 unknown-key rejection은 반드시 실행한다.

---

# 13. Missing value rejection

모든 value option은 다음 조건을 만족해야 한다.

```text
next token exists
next token is not another --key
next token satisfies registered type
```

실패:

```text
MissingCliArgumentValue:
key=<key>
token_index=<n>
```

boolean도 반드시 명시한다.

```text
true
false
```

암묵적 flag boolean은 허용하지 않는다.

---

# 14. Unexpected positional rejection

`--` 이후 registry에 귀속되지 않는 positional token은 실패한다.

```text
UnexpectedCliPositionalArgument:
raw=<value>
token_index=<n>
```

이 검사는 PowerShell continuation 누락으로 분리된 토큰을 포착한다.

---

# 15. Strict type parsing

## Boolean

```text
true
false
```

만 허용한다.

## Unsigned integer

```text
ASCII digit only
negative sign forbidden
overflow rejection
```

## Float

```text
finite only
NaN rejected
Inf rejected
```

## CSV

```text
empty element forbidden
whitespace-only element forbidden
per-element typed parse
duplicate rejection where uniqueness is required
```

## Enum

```text
exact registered value only
```

---

# 16. Semantic CLI groups

```rust
pub enum HeadwiseCliSemanticGroup {
    Repository,
    ParentBinding,
    PromotionScope,
    RoutePolicy,
    ProbeMeasurement,
    Timestamping,
    GuardRuntime,
    ScratchAndAlias,
    PerformanceSurface,
    StatisticalPolicy,
    ResourceValidation,
    CostDecomposition,
    CandidateSearch,
    CrossoverRouting,
    CanaryRollback,
    ArtifactOutput,
}
```

모든 option은 정확히 하나의 group을 소유한다.

필수:

```text
unowned_semantic_group_key_count=0
duplicate_registry_key_count=0
```

---

# 17. Semantic validation

필수 관계:

```text
probe_pairs
=
probe_rounds * probe_pairs_per_round

query_atlas_queries_per_round
=
query_atlas_pairs_per_round
* query_atlas_timestamps_per_pair

candidate_full_pairs
=
candidate_full_rounds
* candidate_full_pairs_per_round

expected_negative_controls
=
1260
```

출력 경로:

```text
workspace/runtime/attention
```

하위만 허용한다.

parent artifact와 manifest는 존재하고 승인된 parent에 결속돼야 한다.

---

# 18. Canonical run contract

```rust
pub struct HeadwiseCanonicalRunContract {
    pub ordered_entries:
        Vec<HeadwiseCanonicalCliEntry>,

    pub semantic_group_counts:
        BTreeMap<String, usize>,

    pub normalized_text: String,
    pub contract_digest: String,
}
```

entry:

```rust
pub struct HeadwiseCanonicalCliEntry {
    pub key: String,
    pub normalized_value: String,
    pub value_type: String,
    pub semantic_group: String,
}
```

canonical order:

```text
semantic group ordinal
→ registry ordinal
```

금지:

```text
HashMap iteration order
raw input order
단순 알파벳 정렬
```

serialization:

```text
--key=value\n
```

digest:

```text
SHA-256(normalized_text)
```

---

# 19. Parse receipt

```rust
pub struct HeadwiseCliParseReceipt {
    pub raw_token_count: usize,
    pub parsed_key_count: usize,

    pub required_key_count: usize,
    pub missing_required_key_count: usize,

    pub duplicate_key_count: usize,
    pub unknown_key_count: usize,
    pub malformed_token_count: usize,
    pub token_adhesion_count: usize,
    pub missing_value_count: usize,
    pub unexpected_positional_count: usize,
    pub type_parse_failure_count: usize,
    pub semantic_failure_count: usize,

    pub original_token_digest: String,
    pub canonical_contract_digest: String,

    pub pass: bool,
}
```

PASS:

```text
모든 failure counter=0
pass=true
```

---

# 20. Boot authority order

필수:

```text
raw CLI capture
→ strict CLI parse seal
→ canonical contract digest
→ parent binding
→ component ABI receipts
→ ABI bundle digest
→ static truth
→ GPU adapter/device initialization
→ kernel execution
→ artifact emission
```

금지:

```text
CLI seal 전에 GPU 초기화
CLI seal 전에 artifact 작성
ABI bundle PASS 전에 kernel 실행
```

필수 counters:

```text
gpu_initialization_before_parse_pass_count=0
artifact_write_before_parse_pass_count=0
kernel_execution_before_abi_bundle_pass_count=0
```

---

# 21. Parent binding

R7-R1의 component composition:

```text
parent patch=R2-R7
backend revision=R2-R7
model_core revision=R2-R6-R1
kernel revision=R2-R7
route policy revision=R2-R7
CLI contract revision=R2-R7-R1
```

이는 model_core downgrade가 아니다.

```text
실제로 변경되지 않은 component의
기존 public ABI를 유지하는 것
```

이다.

---

# 22. Failure taxonomy

```rust
pub enum Headwise01bR12R3R3R3R2R7R1FailureCode {
    BackendAbiRevisionMismatch,
    ModelCoreAbiRevisionMismatch,
    KernelRevisionMismatch,
    GuardRuntimeRevisionMismatch,
    RoutePolicyRevisionMismatch,
    ManifestBuilderRevisionMismatch,
    InputDigestPolicyRevisionMismatch,
    CliContractRevisionMismatch,

    AbiComponentReceiptMissing,
    AbiBundleMemberMissing,
    AbiBundleMemberDuplicate,
    AbiBundleDigestMismatch,
    CrossComponentAbiEqualityRequirementObserved,

    DuplicateCliArgument,
    UnknownCliArgument,
    CliTokenAdhesionDetected,
    MissingCliArgumentValue,
    UnexpectedCliPositionalArgument,
    MalformedCliOptionToken,

    BooleanParseFailure,
    UnsignedIntegerParseFailure,
    SignedIntegerParseFailure,
    FloatParseFailure,
    CsvParseFailure,
    EnumParseFailure,
    PathParseFailure,

    DuplicateCsvElement,
    CliSemanticConstraintFailure,
    MissingRequiredCliArgument,

    CanonicalCliOrderMismatch,
    CanonicalCliDigestMismatch,
    OriginalCliTokenDigestMismatch,

    GpuInitializationBeforeCliSeal,
    ArtifactWriteBeforeCliSeal,
    KernelExecutionBeforeAbiBundleSeal,

    StaticTruthFailure,
    NegativeControlFailure,
    ArtifactDigestFailure,
}
```

---

# 23. Runtime artifacts

```text
workspace/runtime/attention/

ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r1_runtime_artifact.json
ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r1_local_manifest.json

ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r1_parent_binding_receipt.json

ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r1_component_abi_expectations.json
ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r1_component_abi_receipts.json
ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r1_abi_bundle_identity.json

ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r1_cli_option_registry.json
ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r1_raw_cli_tokens.json
ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r1_cli_parse_receipt.json
ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r1_cli_semantic_group_receipts.json

ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r1_canonical_run_contract.json
ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r1_canonical_run_command.ps1

ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r1_negative_control_registry.json
ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r1_negative_control_outcomes.json
ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r1_negative_control_summary.json

ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r1_static_checks.json
ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r1_claim_boundary_receipt.json
ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r1_verdict.json
```

---

# 24. Manifest groups

```text
binding
abi_identity
cli_contract
kernel_evidence
routing
verification
```

필수:

```text
artifact_group_count=6
duplicate_artifact_key_count=0
manifest_deep_json_macro_count=0
```

---

# 25. Primary artifact fields

```text
schema
patch_id
parent_patch_id
build_revision

backend_public_abi_revision
model_core_public_abi_revision
kernel_revision
guard_runtime_revision
route_policy_revision
cli_contract_revision

abi_bundle_member_count
abi_bundle_digest

component_abi_pass_count
component_abi_fail_count

raw_cli_token_count
parsed_cli_key_count
registered_cli_key_count
required_cli_key_count

duplicate_cli_key_count
unknown_cli_key_count
malformed_cli_token_count
cli_token_adhesion_count
missing_cli_value_count
unexpected_cli_positional_count
cli_type_parse_failure_count
cli_semantic_failure_count

original_cli_token_digest
canonical_run_contract_digest

gpu_initialization_before_parse_pass_count
artifact_write_before_parse_pass_count
kernel_execution_before_abi_bundle_pass_count

component_scoped_abi_ownership_proven
abi_bundle_identity_proven
duplicate_unknown_cli_rejection_proven
canonical_run_contract_parse_proven

failed_components
```

---

# 26. Negative controls

R7 inherited controls:

```text
1220
```

R7-R1 additions:

```text
component ABI=10
duplicate and unknown CLI=10
token and type parsing=10
canonical contract=10
```

Final:

```text
negative_control_count=1260
```

## Component ABI controls

```text
ABI01 BackendUsesModelCoreExpectation
ABI02 ModelCoreUsesBackendExpectation
ABI03 SharedExpectedRevisionRestored
ABI04 BackendMismatchAccepted
ABI05 ModelCoreMismatchAccepted
ABI06 KernelRevisionMissing
ABI07 RoutePolicyRevisionMissing
ABI08 BundleMemberMissing
ABI09 BundleMemberDuplicate
ABI10 BundleDigestOrderChanged
```

## CLI controls

```text
CLI01 DuplicateKeySameValue
CLI02 DuplicateKeyDifferentValue
CLI03 UnknownKeyStoredSilently
CLI04 UnknownKeyIgnored
CLI05 LastWriteWinsObserved
CLI06 RegistryDuplicateKey
CLI07 MissingRequiredKey
CLI08 UnexpectedPositionalAccepted
CLI09 OptionWithoutValueAccepted
CLI10 BooleanImplicitDefaultAccepted
```

## Token controls

```text
TOK01 AdhesiveOptionNames
TOK02 EmbeddedDoubleDash
TOK03 InvalidBoolean
TOK04 NegativeUnsignedInteger
TOK05 IntegerOverflow
TOK06 NaNFloat
TOK07 InfiniteFloat
TOK08 EmptyCsvElement
TOK09 DuplicateCsvElement
TOK10 UnknownEnumValue
```

## Canonical controls

```text
CAN01 HashMapOrderUsed
CAN02 RawInputOrderUsedAsCanonical
CAN03 MissingFinalLf
CAN04 DuplicateCanonicalEntry
CAN05 OriginalTokenDigestMissing
CAN06 CanonicalDigestMismatch
CAN07 GpuInitializedBeforeParsePass
CAN08 ArtifactWrittenBeforeParsePass
CAN09 GeneratedPowerShellDuplicateKey
CAN10 GeneratedPowerShellTrailingContinuation
```

필수 aggregate:

```text
negative_control_count=1260
negative_control_executed_count=1260
negative_control_skipped_count=0
negative_control_fail_count=0
```

---

# 27. Required CLI additions

```text
--cli-contract-policy registry-strict-v1

--require-duplicate-cli-key-zero true
--require-unknown-cli-key-zero true
--require-cli-token-adhesion-zero true
--require-missing-cli-value-zero true
--require-unexpected-positional-zero true
--require-cli-type-parse-failure-zero true
--require-cli-semantic-failure-zero true

--canonical-cli-order registry-group-order-v1
--require-original-cli-token-digest true
--require-canonical-run-contract-digest true
--emit-canonical-powershell-command true

--abi-ownership-policy component-scoped-exact-v1
--require-backend-abi-exact true
--require-model-core-abi-exact true
--require-kernel-revision-exact true
--require-route-policy-revision-exact true
--require-cli-contract-revision-exact true
--require-abi-bundle-digest true
--forbid-cross-component-revision-equality-requirement true

--require-cli-seal-before-gpu-init true
--require-cli-seal-before-artifact-write true

--expected-negative-controls 1260
```

---

# 28. Canonical command correction

R7 option block은 정확히 한 번만 존재해야 한다.

정상:

```text
--gqa2-query-heads-per-workgroup 1,2
--gqa2-value-chunks 16,32,64
--maximum-kernel-candidates 36
--softmax-strategies existing,online-single,online-two-level,subgroup-fused
--require-softmax-numerical-parity true
```

금지:

```text
--gqa2-query-heads-per-workrequire-softmax-numerical-parity
```

필수:

```text
duplicate_R7_option_block_count=0
```

---

# 29. PASS formula

```text
PASS =
  exact R7 parent binding

  && backend ABI exact R7
  && model-core ABI exact R6-R1
  && kernel revision exact R7
  && route policy revision exact R7
  && CLI contract revision exact R7-R1

  && all required component receipts pass
  && ABI bundle member count exact
  && ABI bundle digest passes
  && cross-component equality requirement absent

  && CLI registry passes
  && duplicate CLI key count=0
  && unknown CLI key count=0
  && malformed token count=0
  && adhesion count=0
  && missing value count=0
  && unexpected positional count=0
  && type parse failure count=0
  && semantic failure count=0

  && original token digest passes
  && canonical contract digest passes

  && GPU initialization before CLI seal count=0
  && artifact write before CLI seal count=0
  && kernel execution before ABI bundle seal count=0

  && inherited R7 kernel evidence executes
  && guard passes
  && canary passes
  && rollback passes

  && negative control count=1260
  && negative control fail count=0

  && static truth passes
  && artifact digest truth passes
  && model-quality claim count=0
```

---

# 30. PASS proves

```text
backend와 model_core revision이
각 component에 정확히 귀속된다.

서로 다른 component revision을 가진
정상 bundle을 결정적으로 식별할 수 있다.

duplicate CLI가 기존 값을 덮어쓰지 못한다.

unknown 또는 접착된 option이
조용히 무시되지 않는다.

실행 인자 전체가 하나의
canonical normalized contract를 가진다.

CLI와 ABI seal 전에
GPU 및 artifact 작업이 시작되지 않는다.
```

---

# 31. PASS does not prove

```text
GQA2 tile-32가 Reference를 이긴다.

R7 kernel candidate가 production에 승격된다.

cost decomposition이 완전히 닫힌다.

production crossover가 확정된다.

full-prefill이 승격된다.

chunked decode가 승격된다.

모델 품질이 개선된다.
```

---

# 32. HOLD tokens

ABI HOLD:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R1_COMPONENT_ABI_OR_BUNDLE_IDENTITY_INCOMPLETE
```

CLI HOLD:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R1_CANONICAL_RUN_CONTRACT_PARSE_INCOMPLETE
```

성능 HOLD:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R1_ABI_AND_CLI_TRUTH_ESTABLISHED_ATLAS_REFERENCE_NON_INFERIORITY_INCOMPLETE
```

---

# 33. PASS token

```text
PASS_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R1_COMPONENT_SCOPED_ABI_REVISION_OWNERSHIP_BACKEND_MODEL_CORE_BUNDLE_IDENTITY_DUPLICATE_UNKNOWN_CLI_ARGUMENT_REJECTION_CANONICAL_RUN_CONTRACT_PARSE_INCREMENTAL_ONLY_NO_MODEL_QUALITY_OVERCLAIM
```

---

# 34. Required source changes

```text
crates/orchestrator_local/src/bin/
  ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r1_gate.rs
```

권장 분리:

```text
crates/orchestrator_local/src/
  headwise_abi_bundle.rs
  headwise_cli_registry.rs
  headwise_cli_parser.rs
  headwise_cli_contract.rs
```

Cargo:

```text
crates/orchestrator_local/Cargo.toml
```

Spec:

```text
specs/
  ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R1_SPEC.md
```

---

# 35. Canonical build

```powershell
cargo fmt --all -- --check

cargo check --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r1_gate
```

---

# 36. Final authority boundary

```text
Backend revision
  → backend authority

Model-core revision
  → model-core authority

Kernel revision
  → kernel implementation authority

Route revision
  → route policy authority

ABI bundle digest
  → 실제 component 조합 authority
  → revision equality 요구 없음

CLI registry
  → accepted option SSOT

Raw argv
  → 입력 증거

Canonical run contract
  → 실행 계약 SSOT

duplicate·unknown·adhesion
  → 즉시 fail-closed

CLI seal
  → GPU 초기화 전 필수

ABI bundle seal
  → kernel 실행 전 필수

Promotion
  → ABI truth
  + CLI truth
  + R7 kernel evidence
  + matched E2E
  + guard
  + canary
  + rollback
  + 1260-control PASS
```
