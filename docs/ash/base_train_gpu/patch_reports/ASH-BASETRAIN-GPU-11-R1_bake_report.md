# ASH-BASETRAIN-GPU-11-R1 Bake Report

## 확정

- Fix target: WGPU validation error in `Device::create_bind_group_layout`.
- Root cause: compute stage had 5 storage buffers while adapter requested limit allowed 4.
- Fix: binding 0 token input moved from storage buffer to uniform buffer.
- Storage buffers after fix: embed, q_proj, lm_head, logits_output = 4.
- Uniform buffers after fix: token_input = 1.

## 추정

This should clear the exact validation panic reported by the operator. Any later shader/runtime issue must be treated as a new local SSOT log.

## 판단불가

Local cargo build/run was not executed in this environment.
