# 16AI-6H-R1 Acceptance

Status: PENDING_RUNTIME

## Scope

- Compile fix only
- generation=false
- token_ids_mutated=false
- committed_prompt_ids=baseline
- vocab_augmented=false
- new_token_ids_created=false

## Acceptance Criteria

- AC-16AI-6H-R1-1: `quality_by_case` declares `BTreeMap<String, QualityPair>` explicitly.
- AC-16AI-6H-R1-2: `pair` declares `QualityPair` explicitly.
- AC-16AI-6H-R1-3: 16AI-6H compiles without E0282.
- AC-16AI-6H-R1-4: Existing 6H policy contracts remain unchanged.

## 판단불가

Runtime pass is pending local cargo execution.
