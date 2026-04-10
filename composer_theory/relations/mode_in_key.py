from dataclasses import dataclass, field
from typing import Dict, FrozenSet, Optional, Tuple, cast
from ..domain.chord import Chord
from ..domain.color_shift import ColorShift
from ..domain.enums.core import Degrees, Intervals
from ..domain.enums.harmony import Functions, ModeAccess, VariantForm
from ..domain.key import Key
from ..domain.mode import Mode
from ..domain.ids import ChordId, ModeId, RootVariantScaleRef
from ..domain.transition import Transition
from ..tools import effective_role_degree
from .hit import ResolveHit, format_role
from .tools import score_functions_from_intervals


_ANALYSIS_MISSING = object()
_DEFAULT_TONIC_TRIAD = frozenset({Degrees.I, Degrees.III, Degrees.V})
_BASE_SCALE_REF = RootVariantScaleRef(Degrees.I, VariantForm.Base)


@dataclass(frozen=True, slots=True)
class ModeInKeyHit(ResolveHit):
    key: Key
    mode_id: Optional[ModeId]
    mode: Mode | None = field(default=None, repr=False)
    _function_scores: object = field(default=_ANALYSIS_MISSING, init=False, repr=False, compare=False)
    _chromatic_score: object = field(default=_ANALYSIS_MISSING, init=False, repr=False, compare=False)
    _color: object = field(default=_ANALYSIS_MISSING, init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self.mode is not None:
            return
        if self.mode_id is None:
            raise ValueError("ModeInKeyHit 在 mode_id 缺失时必须携带 mode")
        object.__setattr__(self, "mode", self.key[self.mode_id])

    @property
    def is_member(self) -> bool:
        return self.mode_id is not None

    @property
    def access(self) -> ModeAccess | None:
        return None if self.mode_id is None else self.mode_id.access

    @property
    def role(self):
        return None if self.mode_id is None else self.mode_id.role

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
        if self.mode_id is None:
            return f"[Mode∈Key] mode={self.mode} -> direct analysis in key={self.key}"
        return (
            f"[Mode∈Key] mode={self.mode} -> access={self.mode_id.access.name}, "
            f"role={format_role(self.mode_id.role)} in key={self.key}"
        )

    def _ensure_function_scores(self) -> None:
        if self._function_scores is _ANALYSIS_MISSING:
            main_mode = self.key[self.key.main_mode_type]
            main_base = main_mode[_BASE_SCALE_REF]
            tonic_iv = main_mode.tonic | main_base[Degrees.I]
            third_iv = main_mode.tonic | main_base[Degrees.III]
            object.__setattr__(
                self,
                "_function_scores",
                score_functions_from_intervals(
                    present=self._skeleton_intervals_in_key_main_base(),
                    tonic_iv=tonic_iv,
                    third_iv=third_iv,
                ),
            )

    def _ensure_chromatic_score(self) -> None:
        if self._chromatic_score is _ANALYSIS_MISSING:
            object.__setattr__(self, "_chromatic_score", float(len(self._altered_degrees())))

    def _ensure_color(self) -> None:
        if self._color is _ANALYSIS_MISSING:
            object.__setattr__(self, "_color", self._skeleton_chord - self._main_tonic_chord)

    @property
    def _skeleton_chord(self) -> Chord:
        return self.mode[
            ChordId(
                scale_ref=_BASE_SCALE_REF,
                composition=_DEFAULT_TONIC_TRIAD,
            )
        ]

    @property
    def _main_tonic_chord(self) -> Chord:
        main_mode = self.key[self.key.main_mode_type]
        return main_mode[
            ChordId(
                scale_ref=_BASE_SCALE_REF,
                composition=_DEFAULT_TONIC_TRIAD,
            )
        ]

    def _skeleton_intervals_in_key_main_base(self) -> FrozenSet[Intervals]:
        main_mode = self.key[self.key.main_mode_type]
        tonic = main_mode.tonic
        chord = self._skeleton_chord
        return frozenset(tonic | note for note in chord.base_notes)

    def _altered_degrees(self) -> FrozenSet[Degrees]:
        main_mode = self.key[self.key.main_mode_type]
        if self.mode_id is None:
            main_offsets = frozenset(main_mode[_BASE_SCALE_REF][degree].offset for degree in Degrees)
            base_scale = self.mode[_BASE_SCALE_REF]
            return frozenset(degree for degree in Degrees if base_scale[degree].offset not in main_offsets)
        base_scale = self.mode[_BASE_SCALE_REF]
        main_base = main_mode[_BASE_SCALE_REF]
        role_degree = effective_role_degree(self.mode_id)
        return frozenset(
            degree
            for degree in Degrees
            if base_scale[degree - role_degree].offset != main_base[degree].offset
        )

    @property
    def _color_transition(self) -> Transition:
        return self.color[0]

    @property
    def _color_shift(self) -> ColorShift:
        return self.color[1]
