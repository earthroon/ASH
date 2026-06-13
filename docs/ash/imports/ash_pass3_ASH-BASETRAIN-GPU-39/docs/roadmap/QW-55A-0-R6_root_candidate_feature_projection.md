# QW-55A-0-R6 Roadmap Note

QW-55A-0-R6 completes the candidate-to-feature projection layer.

Previous chain:

1. QW-55A-0: Tile16LogicalFromTile8 mode
2. QW-55A-0-R1: logical VTC16 native smoke
3. QW-55A-0-R2: dispatch telemetry receipt chain
4. QW-55A-0-R3: feature/score matrix fixture dry-run
5. QW-55A-0-R4: backend bridge dry-run
6. QW-55A-0-R5: root candidate snapshot fixture
7. QW-55A-0-R6: root candidate feature projection

Next recommended patch:

```txt
QW-55A-0-R7
Projected Feature Score Shadow Aggregate / No Selector Result Seal
```

R7 may generate score rows and shadow aggregate values, but it must still avoid selector result creation and selected token commit.
