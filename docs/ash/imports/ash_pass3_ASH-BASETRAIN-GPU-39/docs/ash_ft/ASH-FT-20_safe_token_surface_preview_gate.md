# ASH-FT-20 Safe Token Surface Preview Gate

## Purpose

ASH-FT-20 is the escaped-only preview gate after ASH-FT-19 classified selected_token_id 34196 as CONTROL / ESCAPED_PREVIEW_ONLY_CANDIDATE. It proves that an operator-approved preview can be created without leaking the raw token surface and without creating decoded text or mutating sequence state.

## Runtime behavior

1. Load ASH-FT-19 receipt, surface audit, safe preview policy, sequence guard, and no-generation guard.
2. Verify ASH-FT-19 PASS and selected_token_id parity.
3. Verify CONTROL / ESCAPED_PREVIEW_ONLY_CANDIDATE.
4. Require explicit operator approval with ESCAPED_PREVIEW_ONLY scope.
5. Read tokenizer vocab line for selected_token_id and verify checksum/byte length/char length against FT-19.
6. Create escaped representation internally.
7. Persist escaped preview metadata only: byte length, char length, checksum, mode, and guard booleans.
8. Persist raw preview, decoded text, sequence commit, and no-generation guards.

## Non-goals

- No raw token display.
- No decoded text output.
- No sequence append or commit.
- No model forward.
- No token selection, generation, or sampling.
- No checkpoint alias rebind or promotion.
