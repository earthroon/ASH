# 16AI-QW-38G-R6A-R12A-R12C — Guard Policy Recheck

R12B created a guard policy candidate after R12 exposed margin overeffect with output stability still PASS. This patch wires that policy into the runtime recheck path so that negative controls become dry-run only and low-margin cases are blocked.
