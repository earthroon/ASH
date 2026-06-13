# ASH-FT-09-R1 Integrity Type Rebind Fix

The FT-09 build failed because it referenced `AshFt08DeltaPacketIntegrityReceipt`, while FT-08 defines `AshFt08IntegrityReceipt`.

R1 rebinds FT-09 to the actual FT-08 type name and preserves all No Runtime Default Apply guards.
