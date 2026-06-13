# QW-50-R0X-A-R1
## Greedy Repeat Attractor Observation Wrapper UTF-8 Bytes Capture / No Runtime Mutation Seal

## SSOT
- base_patch: QW-50-R0X-A
- scope: wrapper I/O capture only
- runtime/model/token/logit/sampler mutation: false

## Prior Failure
- Python subprocess text-mode capture used the Windows default CP949 decoder.
- UTF-8 Rust stdout/stderr triggered UnicodeDecodeError in reader threads.
- proc.stdout became None and wrapper summary was not written.

## Repair
- Capture stdout/stderr as raw bytes.
- Persist raw `.bin` files.
- Decode text copies with UTF-8 and errors=replace.
- Extract JSON from decoded stdout text.

## Forbidden State
- No token ban.
- No logit penalty.
- No sampler mutation.
- No runtime behavior mutation.
- No model weight mutation.

## Validation
- `python -m py_compile scripts/run_qw50_r0x_a_vulkan_infer_wrapper.py` passes in bake environment.
