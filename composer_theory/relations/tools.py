from typing import Dict, Iterable, Set
from ..domain.enums.core import Intervals
from ..domain.enums.harmony import Functions


def function_evidence(*, tonic_iv: Intervals, third_iv: Intervals) -> Dict[Functions, Dict[Intervals, float]]:
    return {
        Functions.Tonic: {tonic_iv: 1.0, third_iv: 3.0},
        Functions.Dominant: {Intervals.P5: 1.0, Intervals.M7: 3.0},
        Functions.Subdominant: {Intervals.P4: 3.0, Intervals.A4: 3.0, Intervals.m6: 2.0, Intervals.M6: 1.0},
    }


def score_functions_from_intervals(
    *,
    present: Iterable[Intervals],
    tonic_iv: Intervals,
    third_iv: Intervals,
) -> Dict[Functions, float]:
    present_set: Set[Intervals] = set(present)
    result: Dict[Functions, float] = {f: 0.0 for f in Functions}
    evidence = function_evidence(tonic_iv=tonic_iv, third_iv=third_iv)
    for func, iv_weights in evidence.items():
        score = 0.0
        for iv, weight in iv_weights.items():
            if iv in present_set:
                score += weight
        result[func] += score
    return result
