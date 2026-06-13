# ASH text-qwave scaffold

## SSOT
- tokenizer_core: hangul/jamo decomposition, morph heuristic nodes, structure tensor observation
- text_kernel: density gate, text-side delta-k summary, runtime hint projection
- runtime: optional `text_qwave_hints` bridge for prompt/backend/hot-cache biasing

## Stage-1 goal
Do not replace the main tokenizer.
Attach Korean structure-tensor observations as a side channel.

## Density gate mapping
The user-described BridgeKey density control is mapped to runtime-safe fields first:
- bridge_confidence
- cairo_risk_proxy
- ambiguity_mean

This keeps the name-space stable even when a first-class BridgeKey field does not yet exist in runtime SSOT.
