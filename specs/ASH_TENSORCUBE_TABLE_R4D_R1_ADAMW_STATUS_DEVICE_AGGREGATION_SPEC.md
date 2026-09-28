# TENSORCUBE-TABLE-R4D-R1

## ADAMW STATUS DEVICE AGGREGATION

```text
TENSORCUBE-TABLE-R4D-R1

ADAMW STATUS DEVICE AGGREGATION

+ CF8 / CF7 / R0B / R0A PRESERVATION
+ EXISTING PER-SEGMENT ADAMW STATUS SEMANTICS PRESERVATION
+ PER-SEGMENT DEVICE STATUS RETENTION
+ STEP-SCOPED STATUS COMPACTION
+ DEDICATED STATUS-ONLY REDUCER WGSL
+ TOTAL STATUS FAILURE COUNT
+ FIRST-FAILED SEGMENT SLOT
+ FAILURE-BIT SUMMARY
+ GPU-COVERED SEGMENT COUNT
+ PER-SEGMENT 4B READBACK ELIMINATION IN ACTIVE
+ PER-SEGMENT MAP_ASYNC ELIMINATION IN ACTIVE
+ ONE 16-BYTE STEP SUMMARY READBACK
+ OBSERVE LEGACY / DEVICE PARITY
+ STATUS ADMISSION BEFORE GENERATION PROMOTION
+ B06 STATUS-ADMISSION CONSUMPTION
+ CANDIDATE WEIGHT / M / V RESIDENCY PRESERVATION
+ NO ADAM NUMERICAL MATH CHANGE
```

## 1. Purpose

The parent AdamW path produces one exact 4-byte device status counter per segment, copies it to a per-segment MAP_READ buffer, requests `map_async`, and lets the pending-generation scheduler collect it through nonblocking polling.

R4D-R1 collapses the **host transaction cardinality** without changing AdamW numerical math or the existing per-segment status producer.

ACTIVE becomes:

```text
segment 0 status --\
segment 1 status ---+--> retained device status slots
...                ---+--> one compact device array
segment N status --/          |
                              v
                       reducer WGSL
                              |
                              v
                       16-byte summary
                              |
                              v
                      one map/readback
                              |
                              v
                       status admission
                              |
                              v
                    generation promotion
```

## 2. Source-Truth Boundary

The parent status collection is not one blocking `PollType::Wait` per segment. It uses nonblocking submission completion / map callback polling.

Therefore the R1 target is specifically:

```text
per-segment status COPY_SRC -> MAP_READ
per-segment map_async
per-segment mapped host read
status-specific polling transaction multiplicity
```

Submission-completion polling required for resource lifetime is a separate authority and is preserved.

## 3. Implementation Resolution

The planning draft allowed changing the AdamW shader to write a shared ledger directly. The baked implementation intentionally chooses a narrower authority:

```text
existing AdamW shader
    -> exact 4-byte per-segment device status remains unchanged

R1 barrier
    -> copies retained 4-byte status values into compact device buffer
    -> NEW reducer WGSL computes one 16-byte summary
    -> one summary readback
```

Reason: this preserves the exact parent AdamW status semantics and avoids introducing shared-write/lease coupling into the candidate kernel.

Thus:

```text
parent AdamW WGSL changed = 0
new status-only reducer WGSL = 1
Adam numerical math changed = 0
```

## 4. Runtime Mode

Environment:

```text
ASH_TENSORCUBE_TABLE_R4D_R1_MODE
```

Accepted:

```text
OFF / DISABLED / 0
OBSERVE / OBSERVE_ONLY
ACTIVE / ACTIVE_VERIFIED / 1
```

Default is `OFF`.

R1 OBSERVE/ACTIVE requires:

```text
R4D-R0A = ACTIVE
R4D-R0B = ACTIVE
```

## 5. OFF

OFF preserves the parent per-segment status readback/map path.

It is the physical A/B baseline.

## 6. OBSERVE

OBSERVE preserves each parent 4-byte status readback and additionally retains the exact device status buffer for the R1 barrier.

At the barrier the compact device status values are copied into the R1 readback after the 16-byte summary and compared against the already-observed parent status values.

Required successful-path parity:

```text
parent segment status == compact device segment status
for every exercised segment
```

OBSERVE intentionally retains parent cost and is qualification-only.

## 7. ACTIVE

ACTIVE changes the AdamW producer status transport:

```text
status_readback = None
per-segment status copy-to-MAP_READ = absent
per-segment map_async = absent
```

The original 4-byte status storage buffer remains device-resident until the optimizer-step status barrier.

Per-segment candidate weight/M/V production is unchanged.

## 8. Deferred Device Status Slot

Backend materializes:

```text
AdamWDeferredStatusDeviceSlotR4DR1
```

binding:

```text
source_generation
target_generation
canonical_parameter_index
element_start
element_count
submission_epoch
status device buffer
status physical allocation
tracked submission / arena retirement authority
```

The slot retains no candidate weight/M/V host payload.

## 9. Submission Completion vs Status Admission

After an AdamW segment submission is physically complete:

```text
source/params/gradient leases may retire
candidate weight/M/V may become provisional device candidate state
status buffer remains retained for the R1 barrier
```

Physical segment completion does **not** imply status admission or generation promotion.

## 10. Deterministic Segment Order

The pending-generation scheduler already owns canonical submitted segment keys in a `BTreeSet`.

R1 drains status slots in that deterministic order.

The resulting compact array index is the canonical R1 status slot ordinal.

Required:

```text
status slot count == submitted segment count
no duplicate slot
no missing slot
```

## 11. Status Reducer

Added WGSL:

```text
crates/base_train/src/shaders/tensorcube_table_r4d_r1_adamw_status_reduce.wgsl
```

It consumes the compact array of exact parent `u32` status counts and produces four atomic words:

```text
word 0  total_status_failure_count
word 1  first_failed_segment_slot, U32_MAX when none
word 2  failure_bits
word 3  gpu_covered_segment_count
```

The reducer does not read or modify weight, M, V, or gradients.

Current failure-bit schema is intentionally bounded to:

```text
FAILURE_ANY
```

because the unchanged parent 4-byte status producer exposes a count, not a categorized failure code.

## 12. Summary Size

Canonical ACTIVE summary:

```text
4 x u32 = 16 bytes
```

Constants:

```text
R4D_R1_SUMMARY_BYTES = 16
R4D_R1_STATUS_BYTES_PER_SEGMENT = 4
R4D_R1_MAX_STATUS_SEGMENTS = 1,048,576
```

## 13. One Step Readback

At the status barrier R1 performs one tracked submission containing:

```text
N x copy 4-byte retained status -> compact device array
one reducer dispatch
copy 16-byte summary -> readback
```

OBSERVE additionally copies the compact array into the same readback for parity.

ACTIVE performs exactly one summary `map_async` request.

The completion loop uses existing nonblocking poll/submission-completion authority; R1 adds no `PollType::Wait`.

## 14. ACTIVE D2H Geometry

For `N` AdamW segments:

Parent-equivalent status D2H:

```text
4N bytes
N status readback transactions
N map requests
```

R1 ACTIVE success path:

```text
16 bytes
1 status summary readback transaction
1 map request
```

For very small N, R1 may not reduce status bytes. The primary structural target is host transaction cardinality.

## 15. Exact Status Semantics Preservation

The parent AdamW shader remains byte-identical.

Therefore all existing parent status increments remain authoritative, including current nonfinite/invalid-value and subgroup-contract failure behavior.

R1 sums those exact status counts; it does not reinterpret Adam values on host or in the reducer.

## 16. Adam Numerical Preservation

The parent candidate shader equations and writes remain unchanged, including:

```text
m = beta1*m_prev + (1-beta1)*g
v = beta2*v_prev + (1-beta2)*g*g
bias correction
new weight calculation
candidate_weight write
candidate_m write
candidate_v write
```

No Adam hyperparameter, finite predicate, dispatch geometry, or candidate write equation changes in R1.

## 17. Candidate Residency Preservation

R1 status aggregation adds no candidate:

```text
weight D2H
M D2HV D2H
host Vec materialization
```

The producer's existing active-device candidate backing remains authoritative.

R1 reads only status buffers.

## 18. Step Status Admission Receipt

Materialize:

```text
AdamWStepStatusAdmissionReceiptR4DR1
```

binding at minimum:

```text
source generation
target generation
optimizer step
expected segment count
gpu-covered segment count
total status failure count
first failed segment slot
first failed parameter/range identity
failure bits
parent-equivalent status D2H bytes
actual status D2H bytes
status D2H￿ñåÑÌÙ½¥)ÁÈµÍµ¹ÐÉ¬½µÀ½Õ¹ÑÌ)ÍÑÀÉ¬½µÀ½Õ¹ÑÌ)=	MIYÁÉ¥Ñä¥±ÕÉÌ)µ¥ÑÑ)É¥ÁÐ¥ÍÐ)((Ää¸MÕÍÌµ¥ÍÍ¥½¸()MÕÍÌÉÅÕ¥ÉÌè()ÑáÐ)áÁÑ}Íµ¹Ñ}½Õ¹ÐøÀ)ÁÕ}½ÙÉ}Íµ¹Ñ}½Õ¹ÐôôáÁÑ}Íµ¹Ñ}½Õ¹Ð)Ñ½Ñ±}ÍÑÑÕÍ}¥±ÕÉ}½Õ¹ÐôôÀ)¥ÉÍÑ}¥±}Íµ¹Ñ}Í±½Ðô¹½¹)¥±ÕÉ}¥ÑÌôôÀ)=	MIYÁÉ¥Ñä¥±ÕÉÌôôÀ)()Q%Y¥Ñ¥½¹±±äÉÅÕ¥ÉÌè()ÑáÐ)ÁÉ}Íµ¹Ñ}ÍÑÑÕÍ}É­}½Õ¹ÐôÀ)ÁÉ}Íµ¹Ñ}ÍÑÑÕÍ}µÁ}Íå¹}½Õ¹ÐôÀ)ÍÑÁ}ÍÑÑÕÍ}É­}½Õ¹ÐôÄ)ÍÑÁ}ÍÑÑÕÍ}µÁ}Íå¹}½Õ¹ÐôÄ)ÑÕ±}ÍÑÑÕÍ}É¡}åÑÌôôÄØ)((ÈÀ¸¥ÉÍÐµ¥±ÕÉÑÑÉ¥ÕÑ¥½¸()IÕÈÉ½ÉÌÑ¡±½ÝÍÐ¥±½µÁÐÍ±½ÐÑ¡É½Õ Ñ½µ¥µµ¥¸Íµ¹Ñ¥Ì¸()Q¡ÑÉµ¥¹¥ÍÑ¥Í¡Õ±ÈÍ±½Ð½ÉÈµÁÌÑ¡ÐÍ±½Ð¬Ñ¼è()ÑáÐ)¹½¹¥±}ÁÉµÑÉ}¥¹à)±µ¹Ñ}ÍÑÉÐ)±µ¹Ñ}½Õ¹Ð)()9¼ÉÜ¹¥Ñ½É¥¹ÐÉ ¥ÌÉÅÕ¥É¸((ÈÄ¸¹ÉÑ¥½¸AÉ½µ½Ñ¥½¸Ñ()]¡¸HÄ¥Ì¹±è()ÑáÐ)µ]Ñ¥ÙÙ¥A¹¥¹¹ÉÑ¥½¹M¡Õ±ÉHÄèéÑ­}¹ÉÑ¥½¸ ¤)()ÉÅÕ¥ÉÌ¸µ¥ÑÑHÄÍÑÑÕÌÉ¥ÁÐ¸()¥±ÕÉè()ÑáÐ)%1}HÑ}HÅ}9%Q}AI=5=Q}	=I}MQQUL)()Q¡¥ÌÁÉÙ¹ÑÌÁ¡åÍ¥±±ä½µÁ±Ñ¹¥Ñ¹ÉÑ¥½¸É½´½µ¥¹ÁÉ½µ½Ñ¥½¸µ±¥¥±½ÉÍÑÑÕÌ½ÍÉÙÑ¥½¸¸((ÈÈ¸ÀØ½¹ÍÕµÁÑ¥½¸()Q¡ÁÉ½ÕÑ¥½¸ÀØÍÑ¥¹±±Í¥ÑáÁ±¥¥Ñ±äÉÅÕ¥ÉÌè()ÑáÐ)ÈÑ}ÈÅ}ÍÑÑÕÍ}µ¥ÑÑôÑÉÕ)ÈÑ}ÈÅ}ÍÑÑÕÍ}µ¥ÍÍ¥½¹}¥ÍÐÁÉÍ¹Ð)()½É½¹ÍÕµ¥¹½Ñ­¥¹Ñ¡¹¥Ñ¹ÉÑ¥½¸Ý¡¸HÄ¥Ì¹±¸()HÄÍÑÑÕÌÙ¥¹Ñ¡É½ÉÁÉÑ¥¥ÁÑÌ¥¸Ñ¡¹ÉÑ¥½¸½µµ¥Ð¡¥¸ÉÑ¡ÈÑ¡¸Éµ¥¹¥¹¥¹½ÍÑ¥µ½¹±ä¸((ÈÌ¸MÑÑÕÌM±½Ð1¥Ñ¥µ()AÈµÍµ¹ÐÍÑÑÕÌÁ¡åÍ¥°±±½Ñ¥½¸¼É¹±ÍÉµ¥¹Ì±¥ÙÑÈÍµ¹ÐÍÕµ¥ÍÍ¥½¸½µÁ±Ñ¥½¸¹¥ÌÉ±Í½¹±äÑÈÑ¡HÄÉÉ¥È¡Ì½Á¥¹ÉÕ¥Ð¸()ÑÈÉÉ¥Èè()ÑáÐ)ÑÉ­ÍÑÑÕÌ±ÍÉ±Í)É¹ÍÑÑÕÌ±ÍÉ±¥µ°½È½Ý¹±±½Ñ¥½¸ÉÑ¥É)()9¼ÍÑÑÕÌÙ¥±±½Ñ¥½¸¥Ì¥¹Ñ¹Ñ¥½¹±±äÉÑ¥¹É½ÍÌÍÑÁÌ¸((ÈÐ¸9¼±½°Ù¥1È()Q¡ÉÕÈÉÕ¹Ñ¥µ¥ÌÁÉÍ¥ÍÑ¹Ð½ÈÑ¡Í¡Õ±È±¥Ñ¥µ°ÕÐÍÑÑÕÌÍ±½ÑÌ¹ÍÕµµÉäÉÍÑÀµÍ½Á¸()9¼ÁÉ½ÍÌµ±½°µÕÑ±ATÍÑÑÕÌ±È¥Ì¥¹ÑÉ½Õ¸((ÈÔ¸A½±°ÑÑÉ¥ÕÑ¥½¸	½Õ¹Éä()HÄ¥ÍÑ¥¹Õ¥Í¡Ìè()ÑáÐ)ÍÕµ¥ÍÍ¥½¸µ½µÁ±Ñ¥½¸Á½±±¥¹)ÍÑÑÕÌµÀ½É¬ÑÉ¹ÍÑ¥½¹Ì)()HÄ½Ì¨©¹½Ð¨¨±¥´Éµ½Ù°½ÍÕµ¥ÍÍ¥½¸µ½µÁ±Ñ¥½¸Á½±±¥¹¹½È¹¥Ñ½ÉÍ½ÕÉ±¥Ñ¥µ¸()%Ð±¥µÌÉµ½Ù°½µ¥ÉÑÁÈµÍµ¹ÐÍÑÑÕÌµÀ½É¬ÑÉ¹ÍÑ¥½¹Ì¥¸Q%Y¸((ÈØ¸ÑÕ°½±Ñ()ÑáÐ)5=Ð)Ì)0À)()5½¥¥è()ÑáÐ)ÉÑÌ½Í}ÑÉ¥¸½ÍÉ½±¥¹ÉÌ)ÉÑÌ½Í}ÑÉ¥¸½ÍÉ½Ñ¹Í½ÉÕ}±½±}µÕ½¹}ÁÉ½ÕÑ¥½¹}±±Í¥Ñ}½ÁÑ¥½¸¹ÉÌ)ÉÑÌ½Í}ÑÉ¥¸½ÍÉ½Õ¹¥¥}Ñ±Í}µÕ}µÝ}Ñ¥Ù}Ù¥}Á¹¥¹}¹ÉÑ¥½¹}Í¡Õ±É}ÈÄ¹ÉÌ)ÉÑÌ½ÕÉ¹}ÝÁÕ}­¹½ÍÉ½µÝ}Ñ¥Ù}Ù¥}¹¥Ñ}ÈÄ¹ÉÌ)()è()ÑáÐ)ÉÑÌ½Í}ÑÉ¥¸½ÍÉ½Í¡ÉÌ½Ñ¹Í½ÉÕ}Ñ±}ÈÑ}ÈÅ}µÝ}ÍÑÑÕÍ}ÉÕ¹ÝÍ°)ÉÑÌ½Í}ÑÉ¥¸½ÍÉ½Ñ¹Í½ÉÕ}Ñ±}ÈÑ}ÈÅ}µÝ}ÍÑÑÕÍ}Ù¥}ÉÑ¥½¸¹ÉÌ)Ñ½½±Ì½Ù±¥Ñ}Í¡}Ñ¹Í½ÉÕ}Ñ±}ÈÑ}ÈÅ}µÝ}ÍÑÑÕÍ}Ù¥}ÉÑ¥½¹}ÍÑÑ¥¹Áä)()9¼ÁÉ¹ÐÙ±¥Ñ½ÈÍ½ÕÉÉÅÕ¥ÉÍÕÍÍ½Èµ½¥¥Ñ¥½¸¸((ÈÜ¸	Õ¥±ÉÁ ¼]M0AÉÍÉÙÑ¥½¸()ÑáÐ)É¼¹Ñ½µ°åÑµ¥¹Ñ¥°)É¼¹±½¬åÑµ¥¹Ñ¥°)ÁÉ¹Ð]M0¥±ÌôÌÈÀ)ÁÉ¹Ð]M0¡¹ôÀ)¹Ü]M0¥±ÌôÄ)Ý½É¬]M0Ñ½Ñ°ôÌÈÄ)()Q¡Í½±]M0¥Ñ¥½¸¥ÌÑ¡HÄÍÑÑÕÌÉÕÈ¸((Èà¸MÑÑ¥ÁÑ¹()áÕÑ¥¸Ñ¡­¹Ù¥É½¹µ¹Ðè()ÑáÐ)AMM}Q9M=IU	}Q	1}HÑ}HÅ}5]}MQQUM}Y%}IQ%=9}MQQ%¡­ÌôÄÐÔ)AMM}Q9M=IU	}Q	1}HÑ}á}IM%9Q}Y1%Q%=9}I%AQ}!}MQQ%¡­ÌôÄÌØ)AMM}Q9M=IU	}Q	1}HÑ}Ý}AIQ%1}YI5}!=Q}]%!Q}IUM}MQQ%¡­ÌôÄÔÄ)AMM}Q9M=IU	}Q	1}HÑ}HÁ	}I%9Q}=	MIY	%1%Qe}Y%}IQ%=9}MQQ%¡­ÌôÄÜà)AMM}Q9M=IU	}Q	1}HÑ}HÁ}!=Q}AQ!}A%A1%9}IM%9e}MQQ%¡­ÌôÄÀÐ)AMM}Q9M=IU	}Q	1}HÑ}Ù}%IQ}	=U9}]%!Q}UA1=}MQQ%¡­ÌôÄÌÔ)AMM}Q9M=IU	}Q	1}HÑ}Õ}!=MQ}=Ae}=11AM}MQQ%¡­ÌôÄÈÜ)AMM}Q9M=IU	}Q	1}HÑ}Ñ}!=MQ}Y%}%=}I=U9QI%A}QQI%	UQ%=9}MQQ%¡­ÌôØÜ)AMM}Q9M=IU	}Q	1}HÑ}Í}M1=Q}1%e1}MQQ%¡­ÌôÜÜ)AMM}Q9M=IU	}Q	1}HÑ	}Í}U11}I=UQ}!=MQ}1I}=5AQ%=9}MQQ%¡­ÌôÄÈÜ)AMM}Q9M=IU	}Q	1}HÅ}Å}%55UE	1}	eQ}=U9Q%9}MQQ%)MM}Y}5U}1=M}HÉ}A!eM}9Ie}HÅ}Å}MQQ%¡­ÌôØÌ)AMM}Y}5U}HÍ!}ÄÅ}A}=]}9%Q}]%!Q}MUMM=I}MQQ%¡­ÌôØÐ)((Èä¸M½ÕÉM±Ì()ÑáÐ(ÍÝÔÌàÐÐÕÌÀÜÐäÝÈÈÌÈÔÀÜÉÜÄÍäÜÝáäÝÁäÝÀäÀÜØÄÉÑÌ½Í}ÑÉ¥¸½ÍÉ½±¥¹ÉÌ(ÜáÙåÐÑÜÙÍÈÔÄÀÜÈÉØÙÔÅÙÌØåäÉÌÈÉÍàÍÀÙåÀÍÑÉÑÌ½Í}ÑÉ¥¸½ÍÉ½Ñ¹Í½ÉÕ}±½±}µÕ½¹}ÁÉ½ÕÑ¥½¹}±±Í¥Ñ}½ÁÑ¥½¸¹ÉÌ)ÝàÈÌÀÉØÐÈäàØÕÜÑÅÑÐÀÉàÐåäÐÍÅÄÑÕÌÈÐÈÙÑÔáàäØäÕÉÑÌ½Í}ÑÉ¥¸½ÍÉ½Õ¹¥¥}Ñ±Í}µÕ}µÝ}Ñ¥Ù}Ù¥}Á¹¥¹}¹ÉÑ¥½¹}Í¡Õ±É}ÈÄ¹ÉÌ￿óCC##c#cv#3F&f#f3cfc##VVcSc6#cV6C3SF#&6#s&f3c7&FW2ö'W&å÷vV&wUö&6¶VæB÷7&2öF×uö7FfUöFWf6Uö6æFFFU÷#ç'0£6CFCFS3VC3CV3VVf&C&6vcF3F#63cSCFCF#C3SV"7&FW2ö&6U÷G&â÷7&2÷6FW'2÷FVç6÷&7V&U÷F&ÆU÷#FE÷#öF×u÷7FGW5÷&VGV6Rçvw6À¦6Css3C3&SVF#63s#3Scs&6CVc6f&S&V#&&cvSffSR7&FW2ö&6U÷G&â÷7&2÷FVç6÷&7V&U÷F&ÆU÷#FE÷#öF×u÷7FGW5öFWf6Uövw&VvFöâç'0£sfVCSCS&Sv&CCFV3&c36fC6FcV3#&cs&V6cvFc#VFööÇ2÷fÆFFUö6÷FVç6÷&7V&U÷F&ÆU÷#FE÷#öF×u÷7FGW5öFWf6Uövw&VvFöå÷7FF2ç¦  ¢223â'Ff7B6VÇ0 ¦FW@¤÷fW&Æ6öFRÖöæÇ¤ ¥4Ó#Sb3S3636CSVC##ccC#6csFSvcFcCS#6&33C#c#3c3&ScCvfCsvP¦fÆW3Óp¤5$3Õ50 ¤gVÆÂ6öFRÖöæÇ¤ ¥4Ó#SbC33s#FCf3VcCCS#cFCssvCs6CC33VC33&cv&c6C#cf¦fÆW3ÓS#p¤5$3Õ50¦  ¢223âWfFVæ6R7FFP ¤&¶RVçf&öæÖVçBFöW2æ÷B6öçFâ'W7BFööÆ6âà ¦FW@¥4õU$4R$´T@¥5DD250¤4ôÕÄRTådU$dTBâ$´RTåd$ôäÔTå@￾SSQHSTQQQQTBTÒPÐSSTQQQQTBTÔPSÑHSTQQQÈÛÛ\[HÜÜYY\ÛZ[H\È[\YÛHÝ]XÈ]Y[ÙKÈÈÌØØ[ÛÛ\[HXØÙ\[ÙBÝÙ\Ú[Ø\ÛÈÚXÚÈ\\ÝÙXÜWØXÚÙ[K[XK\[X\ÙHK[ØÚÙYZBØ\ÛÈÚXÚÈ\\ÙWÝZ[K[XK\[X\ÙHK[ØÚÙYZBØ\ÛÈZ[\\ÙWÝZ[KX[\ÙWÝZ[K\[X\ÙHK[ØÚÙYZB[]\ÝTÔÈYÜHÓÓTSHÛ[Ý[ÛÈÈÌË[[YH]X[YXØ][Û\Ý^THHPÕUBTHPÕUBTHHÐÑTB\]Z\HÝXØÙ\ÜÙ[\]^XÝ\[Ù]XÙHÙYÛY[\Ý]\È\]H[^XÝÛÝ\YÙK[^THHPÕUBÈÈÍPÕUH\ÚXØ[XØÙ\[ÙB\]Z\Y^Ý]\ÈYÙ\^\Ú\ÙY^XÝYÙYÛY[ÈOHÔKXÛÝ\YÙYÛY[Â\\ÙYÛY[Ý]\ÈXYXÚÈÛÝ[H\\ÙYÛY[Ý]\ÈX\Ø\Þ[ÈÛÝ[HÛHÝ\Ý[[X\HXYXÚÂÛHÝ\Ý[[X\HX\Ø\Þ[ÂÝXØÙ\ÜÈÝ[[X\HHM]\ÂØ[Y]HÙ[\][ÛÝÛ[ÝYYÜHÝ]\ÈYZ\ÜÚ[ÛÛÛÝ[Y\ÈÝ]\ÈYZ\ÜÚ[ÛYÙ\ÝHYÈÈØ[Y]HÙZYÚÓKÕHYÈÈÜÝØ[Y]HXÈX]\X[^][ÛÈ]ÈÛ\NØZ]\[Ù[\][ÛÛÜÝ\HTÔÂHYØ]]KÛÛ[]H\ÚXØ[^\HÚÝ[Y][Û[H[[ÛÝ]H\ÝYZ[Y\ÛÝ]X][Û[ZXÝ[ÛYÜHÙ[\][ÛÛ[Ý[ÛÈÈÍK\ÜX[ÙHKÐÛÛ\\N^Ñ\[
ÈHÑÂØ[YHÛÝ\ÙH
ÈHPÕUBÙY\[Ù[]\Ù]ÔKY[UÈÙYÛY[][ÛX^[YYÚÙYÛY[ËKÔÐÑËÐÑ[Ù\Ë[ÙÙÚ[ÈÛXÞH^YYX\Ý\N^Ý]\ÈX\Ø\Þ[ÈÛÝ[Ý]\ÈXYXÚÈ[ØXÝ[ÛÛÝ[Ý]\È]\ÂÝXZ\ÜÚ[ÛXÛÛ\][ÛÛ][\ÂÝ]\Ë[X\àpoll attempts
CPU process time
AdamW scheduler wall time
optimizer-step wall time
generation wall time
```

No exact speedup claim is permitted before physical A/B.

## 36. Successor

After R1 physical closure:

```text
TENSORCUBE-TABLE-R4D-R2
DURABLE PROJECTION HOST COPY COLLAPSE

+ SequentialPack resident .to_vec() elimination
+ bounded source views
+ Vec<u8> / Vec<f32> intermediate collapse
+ M/V streaming projection
+ repeated statistics scan fusion
¬½Õ¹¡½ÍÐÍÉÑ )((ÌÜ¸¥¹°1Ü((øQ¡µ\ÍÑÑÕÌÁå±½¥ÌÑ¥¹ä°ÕÐÑ¡ÁÉ¹ÐÁåÌ½¹¡½ÍÐµ½Õ¹ÉäÑÉ¹ÍÑ¥½¸ÁÈÍµ¹Ð¸((øHÑµHÄÁÉÍÉÙÌÑ¡áÐá¥ÍÑ¥¹ÐµåÑÍµ¹ÐÍÑÑÕÌ½¸Ù¥°ÉÌ½ÍÉÙÑ¥½¸Õ¹Ñ¥°Ñ¡½ÁÑ¥µ¥éÈµÍÑÀÍµ¹Ñ¥ÉÉ¥È°ÉÕÌ±°ÍÑÑÕÍÌ¥¹Ñ¼¥áÄØµåÑÍÕµµÉä°¹É½ÍÍÌÑ¡¡½ÍÐ½Õ¹Éä½¹¸((øµ\¹ÕµÉ¥°µÑ °¹¥ÑÝ¥¡Ð½4½XÉÍ¥¹ä°¹ÍÕµ¥ÍÍ¥½¸µ½µÁ±Ñ¥½¸½Ý¹ÉÍ¡¥ÀÉÁÉÍÉÙ¸¹ÉÑ¥½¸ÁÉ½µ½Ñ¥½¸¥Ì½É¥¸Õ¹Ñ¥°Ñ¡Ù¥ÍÑÑÕÌÍÕµµÉä¥Ìµ¥ÑÑ¸￿