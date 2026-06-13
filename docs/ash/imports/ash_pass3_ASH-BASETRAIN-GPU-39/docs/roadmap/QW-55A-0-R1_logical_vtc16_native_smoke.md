# QW-55A-0-R1 Roadmap Note

## 위치

QW-55A-0은 기존 TensorCube 8x8 MicroTile Atlas에 `Tile16LogicalFromTile8` mode와 QW-55A 16채널 계약을 추가했다.

QW-55A-0-R1은 그 논리 16x16 mode가 native smoke 계층에서 기존 8x8 runner를 반복 호출할 수 있음을 증거화한다.

## 다음 단계

권장 후속 패치:

```txt
QW-55A-0-R2
Logical VTC16 Dispatch Telemetry / Step Receipt Chain Seal
```

R2에서는 8-step dispatch telemetry chain을 별도 receipt로 더 촘촘하게 봉인한다.

## 아직 하지 않는 것

```txt
QW-55A selector 구현
TopK root candidate collection
path feature atlas materialization
root aggregate score
final token commit 변경
greedy authority removal
runtime profile enable
infer_only CLI enable
```
