# ASH-FT-11-R1 Export Surface Direct Bin Import Fix

The FT-11 bin target now imports directly from the FT-11 module path while `lib.rs` also keeps the root export surface. This reduces repeated failures caused by stale or incomplete root re-export surfaces.
