from dataclasses import dataclass, field
from typing import Dict, FrozenSet, Optional, Set, Tuple, cast
from ..domain.base_note import BaseNote
from ..domain.chord import Chord
from ..domain.color_shift import ColorShift
from ..domain.enums.core import Degrees, Intervals
from ..domain.enums.harmony import Functions, VariantForm
from ..domain.ids import ChordId, RootVariantScaleRef, SubVScaleRef
from ..domain.transition import Transition
from ..tools import (
    effective_role_degree,
    is_subv_scale_ref,
    map_degree_to_target_root,
    scale_ref_root_degree,
    scale_ref_variant,
)
from .hit import ResolveHit, format_degrees, format_role
from .mode_in_key import ModeInKeyHit


_ANALYSIS_MISSING = object()
_DEFAULT_TONIC_TRIAD = frozenset({Degrees.I, Degrees.III, Degrees.V})
_BASE_SCALE_REF = RootVariantScaleRef(Degrees.I, VariantForm.Base)


@dataclass(frozen=True, slots=True)
class ChordInKeyHit(ResolveHit):
    mode_in_key_hit: ModeInKeyHit
    chord_id: Optional[ChordId]
    chord: Optional[Chord] = field(default=None, repr=False)
    _function_scores: object = field(default=_ANALYSIS_MISSING, init=False, repr=False, compare=False)
    _chromatic_score: object = field(default=_ANALYSIS_MISSING, init=False, repr=False, compare=False)
    _color: object = field(default=_ANALYSIS_MISSING, init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self.chord is not None:
            return
        if self.chord_id is None:
            raise ValueError("ChordInKeyHit 在 chord_id 缺失时必须携带 chord")
        object.__setattr__(self, "chord", self.mode_in_key_hit.mode[self.chord_id])

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

    def __str__(self) -> str:
        if self.chord_id is None:
            return f"[Chord∈Key] chord={self.chord} -> direct analysis in key={self.mode_in_key_hit.key}"
        degrees = format_degrees(frozenset(self.chord_id.composition or []))
        if is_subv_scale_ref(self.chord_id.scale_ref):
            return (
                f"[Chord∈Key] chord={self.chord} -> mode={self.mode_in_key_hit.mode} "
                f"(access={self.mode_in_key_hit.mode_id.access.name}, role={format_role(self.mode_in_key_hit.mode_id.role)}) "
                f"in key={self.mode_in_key_hit.key}; "
                f"subV(target={self.chord_id.scale_ref.target_degree.name}), degrees={degrees}"
            )
        variant = scale_ref_variant(self.chord_id.scale_ref)
        root = scale_ref_root_degree(self.chord_id.scale_ref)
        return (
            f"[Chord∈Key] chord={self.chord} -> mode={self.mode_in_key_hit.mode}[{variant.name if variant is not None else 'Base'}] "
            f"(access={self.mode_in_key_hit.mode_id.access.name}, role={format_role(self.mode_in_key_hit.mode_id.role)}) "
            f"in key={self.mode_in_key_hit.key}; "
            f"root={root.name}, degrees={degrees}"
        )

    def _ensure_function_scores(self) -> None:
        if self._function_scores is _ANALYSIS_MISSING:
            object.__setattr__(
                self,
                "_function_scores",
                self._score_functions_from_intervals(
                    present=self._intervals_in_key_main_base(),
                    third_iv=self._third_interval_in_main_base(),
                ),
            )

    def _ensure_chromatic_score(self) -> None:
        if self._chromatic_score is _ANALYSIS_MISSING:
            object.__setattr__(self, "_chromatic_score", float(len(self._chromatic_pitch_classes())))

    def _ensure_color(self) -> None:
        if self._color is _ANALYSIS_MISSING:
            object.__setattr__(self, "_color", self.chord - self._main_tonic_chord)

    @property
    def _main_tonic_chord(self) -> Chord:
        key = self.mode_in_key_hit.key
        main_mode = key[key.main_mode_type]
        return main_mode[
            ChordId(
                scale_ref=RootVariantScaleRef(
                    root_degree=Degrees.I,
                    variant=VariantForm.Base,
                ),
                composition=_DEFAULT_TONIC_TRIAD,
            )
        ]

    def _chord_degrees_in_key_scale(self) -> Set[Degrees]:
        if self.chord_id is None:
            key = self.mode_in_key_hit.key
            main_mode = key[key.main_mode_type]
            main_base = main_mode[_BASE_SCALE_REF]
            return {degree for degree in Degrees if main_base[degree] in self.chord.base_notes}
        root = scale_ref_root_degree(self.chord_id.scale_ref)
        return {
            map_degree_to_target_root(self.mode_in_key_hit.mode_id, root + degree)
            for degree in self.chord_id.composition
        }

    def _intervals_in_key_main_base(self) -> FrozenSet[Intervals]:
        main_mode = self.mode_in_key_hit.key[self.mode_in_key_hit.key.main_mode_type]
        tonic = main_mode.tonic
        return frozenset(tonic | note for note in self.chord.base_notes)

    def _altered_degrees(self) -> FrozenSet[Degrees]:
        if self.chord_id is None:
            key = self.mode_in_key_hit.key
            main_mode = key[key.main_mode_type]
            main_base = main_mode[_BASE_SCALE_REF]
            diatonic = frozenset(main_base[degree].offset for degree in Degrees)
            result = set()
            for note in self.chord.base_notes:
                if note.offset in diatonic:
                    continue
                degree = self._degree_from_root_and_pitch_class(main_mode.tonic, note.offset)
                if degree is not None:
                    result.add(degree)
            return frozenset(result)
        key = self.mode_in_key_hit.key
        main_mode = key[key.main_mode_type]
        base_scale = self.mode_in_key_hit.mode[_BASE_SCALE_REF]
        main_base = main_mode[_BASE_SCALE_REF]
        role_degree = effective_role_degree(self.mode_in_key_hit.mode_id)
        return frozenset(
            degree
            for degree in Degrees
            if base_scale[degree - role_degree].offset != main_base[degree].offset
        )

    def _chromatic_pitch_classes(self) -> FrozenSet[int]:
        key = self.mode_in_key_hit.key
        main_mode = key[key.main_mode_type]
        main_base = main_mode[_BASE_SCALE_REF]
        diatonic = frozenset(main_base[degree].offset for degree in Degrees)
        pitch_classes = frozenset(note.offset for note in self.chord.base_notes)
        return frozenset(pc for pc in pitch_classes if pc not in diatonic)

    @staticmethod
    def _degree_from_root_and_pitch_class(root: BaseNote, target_pitch_class: int) -> Optional[Degrees]:
        best: Optional[tuple[int, Degrees]] = None
        for degree in Degrees:
            note_name = root.note_name + degree  # type: ignore[operator]
            try:
                spelled = BaseNote.from_name_and_offset(note_name, target_pitch_class)
            except ValueError:
                continue
            candidate = (abs(spelled.shifts), degree)
            if (
                best is None
                or candidate[0] < best[0]
                or (candidate[0] == best[0] and candidate[1].value < best[1].value)
            ):
                best = candidate
        return None if best is None else best[1]

    def _third_interval_in_main_base(self) -> Intervals:
        key = self.mode_in_key_hit.key
        main_mode = key[key.main_mode_type]
        base = main_mode[_BASE_SCALE_REF]
        return main_mode.tonic | base[Degrees.III]

    def _function_evidence(self, *, third_iv: Intervals) -> Dict[Functions, Dict[Intervals, float]]:
        return {
            Functions.Tonic: {Intervals.P1: 1.0, third_iv: 3.0},
            Functions.Dominant: {Intervals.P5: 1.0, Intervals.M7: 3.0},
            Functions.Subdominant: {Intervals.P4: 3.0, Intervals.A4: 3.0, Intervals.m6: 2.0, Intervals.M6: 1.0},
        }

    def _score_functions_from_intervals(
        self,
        *,
        present: FrozenSet[Intervals],
        third_iv: Intervals,
    ) -> Dict[Functions, float]:
        present_set: Set[Intervals] = set(present)
        result: Dict[Functions, float] = {func: 0.0 for func in Functions}
        evidence = self._function_evidence(third_iv=third_iv)
        for func, iv_weights in evidence.items():
            score = 0.0
            for interval, weight in iv_weights.items():
                if interval in present_set:
                    score += weight
            result[func] += score
        return result

    @property
    def _color_transition(self) -> Transition:
        return self.color[0]

    @property
    def _color_shift(self) -> ColorShift:
        return self.color[1]
