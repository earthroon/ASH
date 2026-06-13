# Same-device raw logits bridge priority-2 patch

## What this patch adds
- `NativeWgpuModel::can_same_device_raw_logits_bridge(&LastLogitsGpu)`
- `NativeWgpuModel::try_bridge_last_logits_raw_lease(&LastLogitsGpu, &mut BridgeStats)`
- `supports_same_device_raw_bridge(&WgpuDevice)` export in `burn_webgpu_backend`

## What it means
This patch upgrades the seam from **runtime handle access** to an actual **last-logits raw lease bridge entrypoint**.

The bridge still depends on the priority-1 runtime handle extraction seam. If the local/vendor fork still returns `None`, this patch will gracefully return `None` too.

## Current limitation
This patch does not yet run GPU sampling. It only makes it possible for later patches to take a `LastLogitsGpu` and obtain a same-device `RawWgpuBufferLease` when local raw access is available.
