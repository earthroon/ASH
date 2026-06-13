# 16AI-QW-38G-R6A-R12A-R1A Static Validation

- status: STATIC_HOTFIX_BAKED_COMPILE_NOT_EXECUTED_IN_CONTAINER
- fixed surface: PowerShell runner only
- reason: native stderr through Tee-Object produced NativeCommandError wrapping cargo progress output
- model mutation: false
