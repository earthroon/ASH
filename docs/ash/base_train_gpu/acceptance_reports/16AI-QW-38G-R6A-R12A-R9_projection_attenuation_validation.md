# 16AI-QW-38G-R6A-R12A-R9 Acceptance — Projection Attenuation Validation

## Acceptance Criteria
- R8A source receipt is loaded and PASS.
- Safe projection candidate exists and profile is `HEAD2_TARGET_DIRECTION_ORTHOGONAL_ONLY`.
- Primary repeat validation matrix is written.
- Repeat margin-drop stats are written.
- Output stability validation is written.
- Prompt variant and negative control statuses are written, including explicit SKIPPED states when no sets are supplied.
- Validation decision is written.
- Runtime default apply remains false.

## Local Command
```powershell
.\scriptsun_16AI_QW_38G_R6A_R12A_R9_projection_attenuation_validation.ps1 -Build
```
