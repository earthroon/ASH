# QW38G R6A R12B-R1 Static Validation

- status: `STATIC_PATCHED_COMPILE_NOT_EXECUTED_IN_CONTAINER`
- failing site: R12B summary `serde_json::json!` macro
- fix: split large JSON macro into `serde_json::Map` inserts
- mutation performed: `false`
- safetensors modified: `false`
- tokenizer modified: `false`
