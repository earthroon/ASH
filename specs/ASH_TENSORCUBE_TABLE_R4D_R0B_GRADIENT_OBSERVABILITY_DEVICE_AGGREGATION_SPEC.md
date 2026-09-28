# TENSORCUBE-TABLE-R4D-R0B

## GRADIENT OBSERVABILITY DEVICE AGGREGATION

```text
TENSORCUBE-TABLE-R4D-R0B

GRADIENT OBSERVABILITY DEVICE AGGREGATION

+ R0A PIPELINE RESIDENCY PRESERVATION
+ DEVICE-RESIDENT PER-OBSERVATION SLOT LEDGER
+ R27 EXACT DEVICE RESULT RETENTION
+ R2D EXACT SUM-SQUARE RESULT RETENTION
+ STEP-BARRIER COMPACT READBACK
+ NONFINITE / NONZERO / MAX-ABS / SUM-SQUARE PRESERVATION
+ FIRST-FAILURE SLOT / LABEL IDENTITY
+ STEP-BARRIER-OBSERVABLE CLASSIFICATION
+ PER-GRADIENT HOST READBACK ELIMINATION
+ PER-GRADIENT POLL-WAIT ELIMINATION
+ GENERATION / OPTIMIZER-STEP BINDING
+ COVERAGE / DUPLICATE FAIL-CLOSED SEAL
+ OBSERVE PARENT-PARITY QUALIFICATION
+ NO RAW GRADIENT D2H
+ NO NEW GRADIENT-MATH WGSL
+ NO THRESHOLD RELAXATION
```

---

# 1. Purpose

R0B removes the CPU synchronization point attached to every migrated gradient observation while preserving the exact parent R27/R2D numerical reductions and the R0A persistent-pipeline authority.

Parent:

```text
TENSORCUBE-TABLE-R4D-R0A
HOT-PATH PIPELINE RESIDENCY
```

R0A already prevents repeated creation of the R27 gradient-observer and R2D sum-square pipelines, but the parent observation path still performs tiny device-result readback and blocking host wait for each observation.

R0B changes the canonical R6 wave-resident production path from:

```text
gradient
    -> R27 / R2D GPU reduction
    -> tiny readback
    -> map_async
    -> Poll(Wait)
    -> host receipt
    -> next gradient
```

to:

```text
gradient 0 -> exact R27/R2D device result slot -\
gradient 1 -> exact R27/R2D device result slot --+--> retained device slots
gradient N -> exact R27/R2D device result slot -/
                                                   |
                                                   v
                                         optimizer-step barrier
                                                   |
                                                   v
                                   one compact copy / map / Poll(Wait)
                                                   |
                                                   v
                                      host receipt materialization
```

The observation evidence moves across the host boundary once at the step barrier. It is not deleted or approximated.

---

# 2. Implementation Resolution

The planning specification allowed a single GPU atomic/reduction ledger.

The baked implementation intentionally uses a **bounded device-resident per-observation slot ledger** instead of introducing new aggregation arithmetic WGSL.

Reason:

```text
existing R27 shader
    already produces exact 20-byte observation result

existing R2D shader
    already produces exact 4-byte sum-square result
```

R0B retains those exact device buffers until the semantic barrier and copies them into one compact readback buffer.

This preserves the parent numerical algorithms and still removes the target bottleneck:

```text
per-gradient map/poll/host synchronization
```

without simultaneously changing reduction math.

This revision therefore optimizes **synchronization transaction cardinality**, not the compact evidence byte count itself.

---

# 3. Compact Slot Geometry

Each R0B observation slot reserves:

```text
R27 result      20 bytes
R2D sum-square  4 bytes optional
-------------------------
slot ceiling    24 bytes
```

Constants:

```text
R4D_R0B_MAX_OBSERVATIONS_PER_STEP = 16,384
R4D_R0B_COMPACT_SLOT_BYTES        = 24
```

Maximum compact barrier readback at the configured ceiling:

```text
16,384 * 24 = 393,216 bytes
```

This is bounded independently of raw gradient tensor byte size.

No raw gradient payload participates in this readback.

---

# 4. Runtime Mode

Environment:

```text
ASH_TENSORCUBE_TABLE_R4D_R0B_MODE
```

Accepted values:

```text
OFF / DISABLED / 0
OBSERVE / OBSERVE_ONLY
ACTIVE / ACTIVE_VERIFIED / 1
```

Default:

```text
OFF
```

Semantics:

```text
OFF
    parent immediate R27/R2D observation path remains authoritative

OBSERVE
    device slots are queued
    parent immediate host observations are also executed
    barrier result must exactly match parent evidence
    no performance claim

ACTIVE
    migrated observations use device slots only
    immediate parent host readbacks are retired
    receipts are materialized after the single step barrier readback
```

---

# 5. R0A Dependency

R0B requires R0A pipeline residency.

If R0B is enabled without the R0A persistent runtime:

```text
R4D_R0B_REQUIRES_R4D_R0A_PIPELINE_RESIDENCY
```

is fail-closed.

R0B obtains the existing persistent:

```text
R27R1GradientObserverPipelineRuntime
R2DGradientSumSquaresPipelineRuntime
```

from `R4dR0aHotPathPipelineResidency`.

R0A pipeline creation accounting remains unchanged; R0B only adds dispatch accounting through the same authority.

---

# 6. R27 Pending Device Result

Backend addition:

```text
R27R1PendingGradientObservation
```

Canonical enqueue:

```text
enqueue_r27r1_gradient_surface_with_pipeline_runtime(...)
```

The enqueue path:

```text
preserves the existing micro-atlas plan
preserves the existing R27 dispatch math
preserves the existing per-page submission semantics
returns the device stats buffer
```

and performs no:

```text
map_async
get_mapped_range
device.poll
```

The legacy immediate R27 wrapper remains available and is rebuilt on top of the enqueue function for OFF/OBSERVE compatibility.

---

# 7. R2D Pending Device Result

Backend addition:

```text
R2DPendingGradientSumSquares
```

Canonical enqueue:

```text
enqueue_r2d_gradient_sum_squares_with_pipeline_runtime(...)
```

It preserves the parent partial/reduce pipelines and returns the exact device total buffer without immediate host readback.

The legacy immediate R2D compact function remains available and uses the same enqueue result followed by its parent readback path.

---

# 8. Observation Classification

R0B explicitly represents:

```text
ImmediateSafetyCritical
StepBarrierObservable
```

The observation surfaces migrated by this bake are explicitly classified:

```text
StepBarrierObservable
```

because their values are consumed as gradient-health / receipt / optimizer-step admission evidence after the R6 wave-resident backward/accumulation work, not as buffer-use legality decisions between individual gradient dispatches.

`ImmediateSafetyCritical` remains represented for future source-audited exceptions, but this bake does not silently classify unrelated safety-critical readbacks into R0B.

Readbacks outside the migrated R27/R2D production surface remain unchanged.

---

# 9. Step Identity

One active R0B step binds:

```text
source_generation
target_generation
source_optimizer_step
target_optimizer_step
```

Required exactness:

```text
target_generation        = source_generation + 1
target_optimizer_step    = source_optimizer_step + 1
```

Only one active step is admitted per runtime authority.

Partial or stale ledgers cannot be rebound to another generation/step.

---

# 10. Bounded Observation Ledger

The host orchestration ledger retains only bounded metadata and device-buffer handles:

```text
slot
label
R27 pending device result
optional R2D pending device result
optional OBSERVE parent reference
observation class
```

It does **not** retain raw gradient bytes.

Capacity is fail-closed at 16,384 observation slots.

Duplicate slot identity is fail-closed.

---

# 11. ACTIVE Deferred Receipt Law

In ACTIVE mode the backward path cannot build final logical/layer gradient receipts from immediate host values, because no per-gradient readback exists.

Therefore ACTIVE returns deferred structural placeholders carrying exact:

```text
element coverage
R0B slot identity
```

After the barrier readback the escaping backward receipts are materialized with the exact device results.

The deferred placeholder itself never becomes commit evidence.

---

# 12. Wave Ordering

Canonical R6 wave-resident ordering is:

```text
begin R0B step

forward / backward observations queued

R6 accumulator end-wave
R6 accumulator finalize

final accumulated gradients queued into same R0B ledger

ONE r4d_r0b_seal_step(...)

materialize lane logical/layer receipts
materialize accumulated-gradient receipt

compute final backward receipt digests / summaries
```

Thus one barrier covers both migrated per-gradient diagnostics and final accumulated-gradient observations.

---

# 13. Single Barrier Readback

At seal:

```text
slot_count * 24-byte compact readback buffer
```

is created.

One encoder copies:

```text
R27 stats  -> slot + 0
R2D sumsq  -> slot + 20 when present
```

Then R0B performs exactly one source-level sequence in the canonical barrier implementation:

```text
queue.submit
map_async
PollType::Wait
get_mapped_range
```

for the entire step ledger.

R0B does not claim to eliminate existing observer AT¥ÍÁÑ¡Ì½ÍÕµ¥ÍÍ¥½¹Ì¸%Ð±¥µ¥¹ÑÌµ¥ÉÑ¨©¡½ÍÐÉ¬½Ý¥ÐÑÉ¹ÍÑ¥½¹Ì¨¨¸((´´´((ÄÐ¸áÐIÍÕ±ÐAÉÍ¥¹()Q¡HÈÜ½µÁÐÉÍÕ±ÐÁÉÍÉÙÌÁÉ¹Ð¥±Ìè()ÑáÐ)Á½Í¥Ñ¥Ù}½Õ¹Ð)¹Ñ¥Ù}½Õ¹Ð)éÉ½}½Õ¹Ð)¹½¹¥¹¥Ñ}½Õ¹Ð)µá}Ì)()IÅÕ¥ÉÁÉÑ¥Ñ¥½¸è()ÑáÐ)Á½Í¥Ñ¥Ù¬¹Ñ¥Ù¬éÉ¼¬¹½¹¥¹¥Ñôô±µ¹Ñ}½Õ¹Ð)()HÉÍÕ´µÍÅÕÉµÕÍÐÉµ¥¸¥¹¥Ñ¸()±½°É¥ÁÐÉÑ¥½¸É¥ÙÌè()ÑáÐ)¹½¹¥¹¥Ñ}½Õ¹Ð)¹½¹éÉ½}½Õ¹Ð)µá}Ì)ÍÕµ}ÍÄ)½ÍÉÙÉ¥¹Ð½Õ¹Ð)½ÍÉÙ±µ¹Ð½Õ¹Ð)()É½´Ñ¡áÐÁÉÍÍ±½ÐÉÍÕ±ÑÌ¸((´´´((ÄÔ¸¥ÉÍÐ¥±ÕÉ%¹Ñ¥Ñä()HÁÁÉÍÉÙÌ½Õ¹¥±ÕÉÑÑÉ¥ÕÑ¥½¸¸()=¸¥ÉÍÐÁÉÍ¹½¹¥¹¥ÑÉÍÕ±Ð°Ñ¡ÑÉµ¥¹°É¥ÁÐÉ½ÉÌ¸¥¹Ñ¥Ñä½Ñ¡½É´è()ÑáÐ)Í±½ÐèñÍ±½Ðøé±°èñ¹½¹¥°½ÍÉÙÑ¥½¸±°ø)()Q¡¥ÌÙ½¥ÌÕ±°µÉ¥¹ÐÉ Ý¡¥±ÁÉÍÉÙ¥¹Ñ¡¥ÉÍÐ¥±¥¹µ¥ÉÑ½ÍÉÙÑ¥½¸¥¹Ñ¥Ñä¸((´´´((ÄØ¸=	MIYAÉ¥Ñä()=	MIYµ½±¥ÉÑ±äÁÉ½ÉµÌ½Ñ ÁÑ¡Ìè()ÑáÐ)¹ÜÙ¥µÍ±½ÐÉÍÕ±Ð(¬)ÁÉ¹Ð¥µµ¥ÑHÈÜ½HÉ¡½ÍÐÉÍÕ±Ð)()ÐÉÉ¥ÈÑ¡äµÕÍÐµÑ áÑ±äÕ¹ÈÑ¡ÁÉ¹ÐÉÁÉÍ¹ÑÑ¥½¸½¹ÑÉÐ¸()AÉ¥Ñä¥±ÕÉ¥¹Éµ¹ÑÌè()ÑáÐ)½ÍÉÙ}ÁÉ¥Ñå}¥±ÕÉ}½Õ¹Ð)()¹¥±Ìè()ÑáÐ)%1}HÑ}HÁ	}=	MIY}AI%Qd)()=	MIY)¥ÌÅÕ±¥¥Ñ¥½¸µ½¹±ä¹¥Ì¹½ÐÁÉ½Éµ¹¥áÑÕÉ¸((´´´((ÄÜ¸Q%Y!½ÍÐMå¹¡É½¹¥éÑ¥½¸±½ÍÕÉ()Q%YÉÅÕ¥ÉÌè()ÑáÐ)Ù¥}±É}ÕÁÑ}½Õ¹ÐøÀ)½ÙÉáÐ)ÁÉ}É¥¹Ñ}É­}½Õ¹ÐôÀ)ÁÉ}É¥¹Ñ}±½­¥¹}Ý¥Ñ}½Õ¹ÐôÀ)ÍÑÁ}ÉÉ¥É}É­}½Õ¹ÐôôÍÑÁ}Í±}½Õ¹ÐôôÍÑÁ}¥¹}½Õ¹Ð)ÉÝ}É¥¹Ñ}É¡}åÑÌôÀ)¹½¹¥¹¥Ñ}½Õ¹ÐôÀ)()¥±ÕÉ±ÍÍÌ¥¹±Õè()ÑáÐ)%1}HÑ}HÁ	}1I}9=Q}aI%M)%1}HÑ}HÁ	}I%9Q}=YI}@)%1}HÑ}HÁ	}AI}I%9Q}I	-}MUIY%Y)%1}HÑ}HÁ	}AI}I%9Q}]%Q}MUIY%Y)%1}HÑ}HÁ	}MQA}I	-}=U9P)%1}HÑ}HÁ	}I]}I%9Q}É )%1}HÑ}HÁ	}9=9%9%Q}I%9P)((´´´((Äà¸½ÙÉÕÑ¡½É¥Ñä()QÉµ¥¹°½ÙÉÉÅÕ¥ÉÌè()ÑáÐ)áÁÑ}É¥¹Ñ}½Õ¹Ðôô½ÍÉÙ}É¥¹Ñ}½Õ¹Ð)áÁÑ}±µ¹Ñ}½Õ¹Ðôô½ÍÉÙ}±µ¹Ñ}½Õ¹Ð)ÕÁ±¥Ñ}É¥¹Ñ}½Õ¹ÐôÀ)½ÙÉ}Á}½Õ¹ÐôÀ)()Q¡­¥µÁ±µ¹ÑÑ¥½¸ÌáÁÑ½½ÍÉÙÉ¥¹Ð½Õ¹Ð¥ÌÑ¡¹½¹¥°ÅÕÕ¨©½ÍÉÙÑ¥½¸µÍ±½Ð¨¨É¥¹±¥Ñä½ÈÑ¡µ¥ÉÑHØÝÙÁÑ ¸MÑÑ¥±°µÉÁ ±½ÍÕÉ¹ÍÕÉÌ±°Í±Ñµ¥ÉÑÍÕÉÌÉ½ÕÑÑ¡É½Õ HÁìÉÕ¹Ñ¥µÉ¥ÁÐÙÉ¥¥ÌÙÉäÅÕÕÍ±½Ð¥ÌÉ½ÙÉáÑ±ä¸()HÁ½Ì¹½Ð±¥´¸¥¹Á¹¹Ðµ½°µÝ¥É¥¹Ðµ¹¥ÍÐå½¹Ñ¡Ð¹½¹¥°µ¥ÉÑ½ÍÉÙÑ¥½¸ÍÐ¸((´´´((Ää¸ÕµÕ±ÑÉ¥¹Ð=ÍÉÙÑ¥½¸()Q¡¥¹°HØÕµÕ±ÑµÉ¥¹Ð½ÍÉÙÑ¥½¸¥Ì±Í¼ÅÕÕÑ¡É½Õ HÁÕÍ¥¹½Õ¹ÉÜ±ÍÍ±¥Ì¸()%ÐÕÍÌÑ¡ÍµÄØ5¥¡Õ¹­¥¹ÕÑ¡½É¥ÑäÌÑ¡ÁÉ¹Ð½ÍÉÙÈÁÑ Ý¡ÉÉÅÕ¥É¸()9¼¡½ÍÐÉ¥¹ÐÁå±½¥ÌµÑÉ¥±¥é¸()ÑÈÑ¡½¹ÉÉ¥È°Ñ¡á¥ÍÑ¥¹ÕµÕ±ÑµÉ¥¹ÐÉ¥ÁÐÍ¡Á¥ÌÉ½¹ÍÑÉÕÑÉ½´HÁÍ±½ÐÉÍÕ±ÑÌ¸()=µ½ÉÑ¥¹ÌÑ¡ÁÉ¹Ð½ÍÉÙ}ÕµÕ±Ñ}É¥¹ÑÌ ¸¸¸¥±±¬¸((´´´((ÈÀ¸9¼IÜÉ¥¹ÐÉ ()HÁÉ¬½¹Ñ¥¹Ì½¹±ä½µÁÐHÈÜ½HÉÉÍÕ±ÑÌ¸()½É¥¸è()ÑáÐ)Õ±°É¥¹ÐÑ¹Í½ÈÉ¬)¡½ÍÐYñÌÈøÉ¥¹ÐµÑÉ¥±¥éÑ¥½¸)ÉÜÉ¥¹ÐÕµÀ½ÈÁÉ¥Ñä)()I¥ÁÐ¥±è()ÑáÐ)ÉÝ}É¥¹Ñ}É¡}åÑÌ)()µÕÍÐÉµ¥¸éÉ¼½ÈQ%Yµ¥ÍÍ¥½¸¸((´´´((ÈÄ¸9¼Q¡ÉÍ¡½±I±áÑ¥½¸()HÁ¡¹ÌÙ¥¹ÑÉ¹ÍÁ½ÉÐ¹Íå¹¡É½¹¥éÑ¥½¸Ñ¥µ¥¹½¹±ä¸()%Ð½Ì¹½Ð±ÑÈè()ÑáÐ)¥¹¥Ñ¥¹¥Ñ¥½¸)¹½¹éÉ¼¥¹¥Ñ¥½¸)µàµÌÉ¥Ñ¡µÑ¥)ÍÕ´µÍÅÕÉÉ¥Ñ¡µÑ¥)É¥¹ÐáÁ±½Í¥½¸Á½±¥ä)±½°¹½É´Á½±¥ä)±¥ÁÁ¥¹Ñ¡ÉÍ¡½±)½ÁÑ¥µ¥éÈ½ÉµÕ±)()I¥ÁÐáÁ±¥¥Ñ±äÍ±Ìè()ÑáÐ)¹½}Ñ¡ÉÍ¡½±}É±áÑ¥½¸ôÑÉÕ)((´´´((ÈÈ¸AÉ¹Ð	ÕIÁ¥È()ÕÉ¥¹HÁµ¥ÉÑ¥½¸°½¹HÙµHÈ½ÕÑÁÕÐµ­ÝÉÍ½ÕÉ±±Í¥Ñ¥¸Ñ±Í}ÉÕ¹Ñ¥µ}É±}±½ÍÍ}­ÝÉ¹ÉÍÝÌ½Õ¹±±¥¹Ñ¡É½ÕÑµÍ¡±ÁÈÝ¥Ñ ½Í½±ÑÙ¥°ÅÕÕ￾&wVÖVçG2à ¤B26÷'&V7FVBFò72FR6æöæ6Â&÷WFR6öçFWC  ¦FW@¦ö'6W'fU÷6ævÆR&÷WFRÂfGræGrÂâââ¦  ¥F22âæ6FVçFÂ6ö×ÆR×6R&W"&WV&VB'FR&VçBVÇW"6væGW&RâBFöW2æ÷B6ævRw&FVçBÖF÷"#"ö'6W'fFöâ6VÖçF72à ¢ÒÒÐ ¢2#2âFW&ÖæÂ&V6V@ ¤fÆS  ¦FW@§FVç6÷&7V&U÷F&ÆU÷#FE÷#%öw&FVçEöö'6W'f&ÆGöFWf6Uövw&VvFöå÷&V6VBæ§6öà¦  ¤6ö×7BÆös  ¦FW@¥´4ÕDTå4õ$5T$RÕD$ÄRÕ#DBÕ#%Õ¶w&FVçBÖö'6W'f&ÆGÖFWf6RÖvw&VvFöåÐ¦  ¥72Fö¶Vã  ¦FW@¥55õDTå4õ$5T$UõD$ÄUõ#DEõ#%ôu$DTåEôô%4U%d$ÄEôDUd4Uôtu$TtDôà¦  ¥66Â÷W&f÷&Öæ6RöÆC  ¦FW@¤ôÄEõDTå4õ$5T$UõD$ÄUõ#DEõ#%õ44ÅõU$dõ$Ôä4UõTådU$dT@¦  ¢ÒÒÐ ¢2#Bâ&V6VB6÷VçFW'0 ¥FRFW&ÖæÂ&V6VB&W÷'G2BÖæ×VÓ  ¦FW@§7FWö&Vvåö6÷Vç@§7FW÷6VÅö6÷Vç@¦FWf6UöÆVFvW%÷WFFUö6÷Vç@¦WV7FVEöw&FVçEö6÷Vç@¦ö'6W'fVEöw&FVçEö6÷Vç@¦WV7FVEöVÆVÖVçEö6÷Vç@¦ö'6W'fVEöVÆVÖVçEö6÷Vç@¦æöæfæFUö6÷Vç@¦æöç¦W&õö6÷Vç@¦Öö'0§7VÕ÷7¦GWÆ6FUöw&FVçEö6÷Vç@¦6÷fW&vUövö6÷Vç@§W%öw&FVçE÷&VF&6µö6÷Vç@§W%öw&FVçE÷&VF&6µö'FW0§W%öw&FVçEö&Æö6¶æu÷vEö6÷Vç@§7FWö&'&W%÷&VF&6µö6÷Vç@§7FWö&'&W%÷&VF&6µö'FW0¦ÖÖVFFU÷6fWG÷&VF&6µö6÷Vç@§&uöw&FVçEöC&ö'FW0¦ö'6W'fU÷&GöfÇW&Uö6÷Vç@¦f'7EöfÇW&UöFVçFG¦Öw&FVEöö'6W'fFöåö6Æ70¦  ¢ÒÒÐ ¢2#RâWÆ6BæöâÔvöÇ0 ¥#"FöW2æ÷BWB6ævS  ¦FW@¦f÷'v&BfæFRÖwV&B&VF&6·0¥#Bõ#Rôs#DBæöâÖw&FVçB7FGW2÷&VF&6²öÆ7¤FÕrW"×6VvÖVçB7FGW2&VF&6°§vVvB$B&W6FVæ7§&W6FVçB4öfæFRfÆFFöâ66ç0¦GW&&ÆR&ö¦V7Föâ÷7B6÷W0¦fÆW77FVÒGW&&ÆG&'&W'0¦  ¥FW6R&VÖâ6W&FVÇGG&'WF&ÆR&öFÖFV×2à ¢ÒÒÐ ¢2#bâæòæWrG&æærtu4À ¥#"FG2æòæWrw&FVçB&FÖWF2tu4ÂfÆRà ¤B&WW6W2FRW7BW7Fær##rõ#$BFWf6R&VGV7Föç2æB6ævW2öæÇ&W7VÇBÆfWFÖRò&VF&6²66VGVÆærà ¦utu4Â6÷W&6Rw&×W7B&VÖâ'FRÖFVçF6ÂFò#&VçBà ¢ÒÒÐ ¢2#râ7GVÂ6öFRFVÇF ¦FW@¤ÔôB¤DB ¤DTÂ ¦  ¤ÖöFfVC  ¦FW@¦7&FW2ö&6U÷G&â÷7&2öFÆ5÷'VçFÖU÷&VÅöÆ÷75ö&6·v&Bç'0¦7&FW2ö&6U÷G&â÷7&2öÆ"ç'0¦CsS33cv6&&CSsS3#f#c#fCV&C6ss&&CFCc#c&3CcC6R7&FW2ö&6U÷G&â÷7&2÷6¶VE÷'VçFÖUöæFfUö&ö÷G7G&ö67V×VÆFöå÷vfU÷&W6FVæ7ç'0£Vf3VSV6cSC#csVS&&VfSv##Sc63s#3S36V6SCFf#s#b7&FW2ö&6U÷G&â÷7&2÷&öGV7Föåö×VÇF7FWöÆö÷ö67V×VÆFöã÷66VGVÆW"ç'0¦#VCf&S#sC6&##&6VSC##svfCC#ccc6#scV#33CF3Cc3&27&FW2ö&6U÷G&â÷7&2÷FVç6÷&7V&U÷F&ÆU÷#FE÷#ö÷E÷F÷VÆæU÷&W6FVæ7ç'0£3##3C#FCFFVCvCsCf6cvCcSV3Cf&Ffc3cC#SvSV6f#vCR7&FW2ö&6U÷G&â÷7&2÷FVç6÷&7V&U÷F&ÆU÷#FE÷#%öw&FVçEöö'6W'f&ÆGöFWf6Uövw&VvFöâç'0¦SFc3&3CSCcf#F3CCSSfsfcSf#sf&ccVVSS#cVS6&7&FW2ö'W&å÷vV&wUö&6¶VæB÷7&2ö&6U÷G&å÷##w#öw&FVçEöö'6W'f&ÆGç'0£CcF3cCCCC33sS36CcccSvCsFScS#&cV3c3#S3cfVSvFfS7&FW2ö'W&å÷vV&wUö&6¶VæB÷7&2ö&6U÷G&å÷#&Eöw&FVçE÷7G&VÒç'0¦Ff36V63sfFS6S##VS#vC#CVF##663sSSCcs#fcCscCFööÇ2÷fÆFFUö6÷FVç6÷&7V&U÷F&ÆU÷#FE÷#ö÷E÷F÷VÆæU÷&W6FVæ7÷7FF2ç£#F&V#C33&66V3CS3csFcSScscsC63s3c&ccSS&#FööÇ2÷fÆFFUö6÷FVç6÷&7V&U÷F&ÆU÷#FE÷#%öw&FVçEöö'6W'f&ÆGöFWf6Uövw&VvFöå÷7FF2ç¦  ¢ÒÒÐ ¢23"â'Ff7B6VÇ0 ¦FW@¤÷fW&Æ6öFRÖöæÇ¤ ¥4Ó#Sb&S#vCcffCvsV&fSc3VS3FC&6vfVFCV#S3SF#ffCf&V#S&Sv60¦fÆW3Ó ¤5$3Õ50 ¤gVÆÂ6öFRÖöæÇ¤ ¥4Ó#SbCsV#VF#FcFC6cCcv3sfC#cSc3ss#CcC633&fSssc&#3p¦fÆW3ÓS# ¤5$3Õ50¦  ¢ÒÒÐ ¢232âÆö6Â6ö×ÆR66WFæ6P ¥&WV&VBöâFRWF÷&FFfRvæF÷w26÷W&6RG&VS  ¦÷vW'6VÆÀ¦6&vò6V6² ¢×'W&å÷vV&wUö&6¶VæB ¢ÒÖÆ" ¢Ò×&VÆV6R ¢ÒÖÆö6¶VB ¢Ö¢ ¦6&vò6V6² ¢×&6U÷G&â ¢ÒÖÆ" ¢Ò×&VÆV6R ¢ÒÖÆö6¶VB ¢Ö¢ ¦6&vò'VÆB ¢×&6U÷G&â ¢ÒÖ&â&6U÷G&â ¢Ò×&VÆV6R ¢ÒÖÆö6¶VB ¢Ö¢¦  ¤6ö×ÆR52×W7Bæ÷B&RæfW'&VBVçFÂFW6RWV7WFR7V66W76gVÆÇà ¢ÒÒÐ ¢23Bâ'VçFÖRVÆf6Föâ÷&FW  ¤f'7BVÆf6Föã  ¦FW@¤4õDTå4õ$5T$UõD$ÄUõ#DEõ#ôÔôDSÔ5DdP¤4õDTå4õ$5T$UõD$ÄUõ#DEõ#%ôÔôDSÔô%4U%dP¦  ¥&WV&VB&Vf÷&R5DdR&öÖ÷Föã  ¦FW@¦FWf6R6Æ÷BFWW&66V@¤ô%4U%dR&VçB&GW7@¦6÷fW&vRW7@¦vVæW&Föâö÷FÖ¦W"×7FWFVçFGW7@¦  ¥FVâ5DdS  ¦FW@¤4õDTå4õ$5T$UõD$ÄUõ#DEõ#ôÔôDSÔ5DdP¤4õDTå4õ$5T$UõD$ÄUõ#DEõ#%ôÔôDSÔ5DdP¦  ¢ÒÒÐ ¢23Râ5DdR66Â66WFæ6P ¥&WV&VC  ¦FW@¦FWf6UöÆVFvW%÷WFFUö6÷VçBâ ¦WV7FVEöw&FVçEö6÷VçBÓÒö'6W'fVEöw&FVçEö6÷Vç@¦WV7FVEöVÆVÖVçEö6÷VçBÓÒö'6W'fVEöVÆVÖVçEö6÷Vç@¦GWÆ6FUöw&FVçEö6÷VçBÒ ¦6÷fW&vUövö6÷VçBÒ §W%öw&FVçE÷&VF&6µö6÷VçBÒ §W%öw&FVçEö&Æö6¶æu÷vEö6÷VçBÒ §7FWö&'&W%÷&VF&6µö6÷VçBÓÒ7FW÷6VÅö6÷VçBÓÒ7FWö&Vvåö6÷Vç@§&uöw&FVçEöC&ö'FW2Ò ¦æöæfæFUö6÷VçBÒ ¦f'7BÖfÇW&RFVçFG&VÖç2&÷VæFVBvVâfÇW&RfGW&R2WW&66V@¥#VÆæR&W6FVæ7&VÖç2FÖGFV@¦  ¥FR66Â'Vâ×W7BÇ6òFVÖöç7G&FRæò&Vw&W76öââ#bô4cvVæW&Föâ6Æ÷7W&Rà ¢ÒÒÐ ¢23bâW&f÷&Öæ6R66WFæ6P ¥6ÖR×6÷W&6Rô#  ¦FW@¥#&Vç@§g0¥#²#"5DdP¦  ¤ÖV7W&RBÖæ×VÓ  ¦FW@¦Öö7æ26÷Vç@¥öÆÂvB6÷Vç@¦6ö×7B&VF&6²G&ç67Föâ6÷Vç@¦6ö×7B&VF&6²'FW0¤5R&ö6W72FÖP¦&6·v&BvÆÂFÖP¦÷FÖ¦W"×7FWvÆÂFÖP¦vVæW&FöâvÆÂFÖP¦  ¥#"FöW2æ÷B6ÆÒVÆÖæFöâöbÆÂuR7V&ÖG2÷"ÆÂ÷7BvG2âG&æærâB6Æ×2VÆÖæFöâöbFRÖw&FVB¢§W"Öw&FVçB##rõ#$BÖÖVFFR÷7B&VF&6²÷vB6â¢¢à ¤æòW7B7VVGW6ÆÒ2W&ÖGFVB&Vf÷&R66Âô"WfFVæ6Rà ¢ÒÒÐ ¢23râ7V66W76÷  ¤gFW"#"6ö×ÆR²ô%4U%dR&G²5DdR66Â6Æ÷7W&S  ¦FW@¥DTå4õ$5T$RÕD$ÄRÕ#D2Ô4cp¥%DÂe$ÒõBÕtTtBdõ%t$Bò$4µt$B$UU4P¦  ¥#"FöW2æ÷B&VvâvVvB×&W6FVæ7÷FÖ¦FöâG6VÆbà ¢ÒÒÐ ¢23â6ö×ÆWFöâÆp ¥#"ÖVÖC  ¦FW@¥55õDTå4õ$5T$UõD$ÄUõ#DEõ#%ôu$DTåEôô%4U%d$ÄEôDUd4Uôtu$TtDôà¦  ¦266Â&öÖ÷FöâöæÇvVã  ¦FW@¥4õU$4P¢W7B##rõ#$BFWf6R&W7VÇG2&WFæVBFò&'&W ¢æò&rw&FVçB÷7BÖFW&Æ¦Föà ¥5DD0¢#"sós50¢&WV&VB&VçB&Vw&W76öç250 ¤4ôÕÄP¢&6¶VæB&VÆV6R50¢&6U÷G&âÆ"&VÆV6R50¢&6U÷G&â&æ'50 ¥%TåDÔRô%4U%dP¢&VçBöFWf6R&GW7@ ¥44Â5DdP¢Öw&FVBW"Öw&FVçB&VF&6·2Ò ¢Öw&FVBW"Öw&FVçB&Æö6¶ærvG2Ò ¢öæR&÷VæFVB&'&W"&VF&6²W"÷VæVB7FW ¢6÷fW&vRW7@¢&rw&FVçBC$Ò ¢F÷vç7G&VÒw&FVçB&V6VG2ÖFW&Æ¦VB&Vf÷&R6öÖÖBWF÷&G ¥U$dõ$Ôä4P¢6W&FVÇÖV7W&V@¦  ¢ÒÒÐ ¢23âfæÂÆp £â¢¥#"FöW2æ÷BvV¶Vâw&FVçBö'6W'f&ÆGâB6ævW2vVâW7BFWf6RWfFVæ6R7&÷76W2FR÷7B&÷VæF'â¢  £â¢¥FRW7Fær##ræB#$B&VGV7Föç2&VÖâFRçVÖW&6ÂWF÷&GâFV"6ö×7BFWf6R&W7VÇG2&VÖâ&W6FVçB7&÷72FR7FWæB&R&VBöæ6RBFR6VÖçF2&'&W"â¢  £â¢¥W"Öw&FVçBÖ÷öÆÂ7æ6&öæ¦Föâ2&VÖ÷fVBf÷"FRÖw&FVB#bvfR×&W6FVçB&öGV7FöâF²&rw&FVçG2æWfW"&V6öÖR÷7BÆöBâ¢ ￿