from dataclasses import dataclass, field
from typing import Dict, Optional, Set, Tuple, cast

from ..domain.chord import Chord
from ..domain.color_shift import ColorShift
from ..domain.enums.core import Degrees, Intervals
from ..domain.enums.harmony import Functions, VariantForm
from ..domain.enums.runtime import DegreeVariant, TurningPoints
from ..domain.mode import Mode
from ..domain.ids import ChordId, RootVariantScaleRef, SubVScaleRef
from ..domain.transition import Transition
from ..tools import is_subv_scale_ref, scale_ref_root_degree, scale_ref_variant
from .hit import ResolveHit, format_degrees
from .tools import score_functions_from_intervals


_ANALYSIS_MISSING = object()
_DEFAULT_TONIC_TRIAD = frozenset({Degrees.I, Degrees.III, Degrees.V})
_BASE_SCALE_REF = RootVariantScaleRef(Degrees.I, VariantForm.Base)


@dataclass(frozen=True, slots=True)
class ChordInModeHit(ResolveHit):
    mode: Mode
    chord_id: Optional[ChordId]
    chord: Optional[Chord] = field(default=None, repr=False)
    _function_scores: object = field(default=_ANALYSIS_MISSING, init=False, repr=False, compare=False)
    _chromatic_score: object = field(default=_ANALYSIS_MISSING, init=False, repr=False, compare=False)
    _color: object = field(default=_ANALYSIS_MISSING, init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self.chord is not None:
            return
        if self.chord_id is None:
            raise ValueError("ChordInModeHit 在 chord_id 缺失时必须携带 chord")
        object.__setattr__(self, "chord", self.mode[self.chord_id])

    @property
    def is_member(self) -> bool:
        return self.chord_id is not None

    @property
    def function_scores(self) -> Dict[Functions, float]:
        self._ensure_function_scores()
        return cast(Dict[Functions, float], self._function_scores)

    @property
    def chromatic_score(self) -> float:
        self._ensure_chromatic_score()
        return cast(float, self._chromatic_score)

    @property
    def color(self) -> Tuple[Transition, ColorShift]:
        self._ensure_color()
        return cast(Tuple[Transition, ColorShift], self._color)

    @property
    def turning_points(self) -> Set[TurningPoints]:
        if self.chord_id is None or is_subv_scale_ref(self.chord_id.scale_ref):
            return set()
        variant = scale_ref_variant(self.chord_id.scale_ref)
        if variant == VariantForm.Base:
            return set()
        chord_degrees = self._chord_degrees_in_mode_scale()
        focus = chord_degrees & {Degrees.VI, Degrees.VII}
        tps = set()
        for degree in focus:
            tps.add(TurningPoints(DegreeVariant(degree, variant)))
        return tps

    def __str__(self) -> str:
        if self.chord_id is None:
            return f"[Chord∈Mode] chord={self.chord} -> non-member analysis in mode={self.mode}"
        degrees = format_degrees(frozenset(self.chord_id.composition or []))
        if is_subv_scale_ref(self.chord_id.scale_ref):
            return (
                f"[Chord∈Mode] chord={self.chord} -> subV(target={self.chord_id.scale_ref.target_degree.name}), "
                f"degrees={degrees} in mode={self.mode}"
            )
        variant = scale_ref_variant(self.chord_id.scale_ref)
        root = scale_ref_root_degree(self.chord_id.scale_ref)
        return (
            f"[Chord∈Mode] chord={self.chord} -> root={root.name}, degrees={degrees} "
            f"in mode={self.mode}[{variant.name if variant is not None else 'Base'}]"
        )

    def _ensure_function_scores(self) -> None:
        if self._function_scores is _ANALYSIS_MISSING:
            intervals: Set[Intervals] = {self.mode.tonic | note for note in self.chord.base_notes}
            tonic_iv = self._degree_interval_in_mode_base(Degrees.I)
            third_iv = self._degree_interval_in_mode_base(Degrees.III)
            object.__setattr__(
                self,
                "_function_scores",
                score_functions_from_intervals(present=intervals, tonic_iv=tonic_iv, third_iv=third_iv),
            )

    def _ensure_chromatic_score(self) -> None:
        if self._chromatic_score is _ANALYSIS_MISSING:
            if self.chord_id is None:
                base_notes = frozenset(self.mode[_BASE_SCALE_REF])
                chromatic_score = float(sum(1 for note in self.chord.base_notes if note not in base_notes))
            elif is_subv_scale_ref(self.chord_id.scale_ref):
                base_notes = frozenset(self.mode[_BASE_SCALE_REF])
                chromatic_score = float(sum(1 for note in self.chord.base_notes if note not in base_notes))
            else:
                variant = scale_ref_variant(self.chord_id.scale_ref)
                if variant == VariantForm.Base:
                    chromatic_score = 0.0
                else:
                    chord_degrees = self._chord_degrees_in_mode_scale()
                    base_scale = self.mode[_BASE_SCALE_REF]
                    cur_scale = self.mode[RootVariantScaleRef(Degrees.I, variant)]
                    chromatic_score = 0.0
                    for degree in chord_degrees:
                        if cur_scale[degree].offset != base_scale[degree].offset:
                            chromatic_score += 1.0
            object.__setattr__(self, "_chromatic_score", chromatic_score)

    def _ensure_color(self) -> None:
        if self._color is _ANALYSIS_MISSING:
            object.__setattr__(self, "_color", self.chord - self._tonic_chord)

    @property
    def _tonic_chord(self) -> Chord:
        return self.mode[
            ChordId(
                scale_ref=_BASE_SCALE_REF,
                composition=_DEFAULT_TONIC_TRIAD,
            )
        ]

    def _matched_degrees_in_mode_base(self) -> Set[Degrees]:
        base = self.mode[_BASE_SCALE_REF]
        return {degree for degree in Degrees if base[degree] in self.chord.base_notes}

    def _chord_degrees_in_mode_scale(self) -> Set[Degrees]:
        if self.chord_id is None:
            return self._matched_degrees_in_mode_base()
        root = scale_ref_root_degree(self.chord_id.scale_ref)
        return {root + d for d in self.chord_id.composition}

    def _degree_interval_in_mode_base(self, degree: Degrees) -> Intervals:
        base = self.mode[_BASE_SCALE_REF]
        return self.mode.tonic | base[degree]

    @property
    def _color_transition(self) -> Transition:
        return self.color[0]

    @property
    def _color_shift(self) -> ColorShift:
        return self.color[1]

