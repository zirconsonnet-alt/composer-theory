from collections import defaultdict
from typing import AbstractSet, DefaultDict, Dict, FrozenSet, Optional, cast
from .scale import Scale
from .quality import Quality
from .base_note import BaseNote
from .dissonance import Resolution
from .enums.core import Degrees
from .transition import Transition
from .color_shift import ColorShift
from ._intern import InternedMeta, FrozenSlotsMixin


_DEFAULT_TRIAD: FrozenSet[Degrees] = frozenset({Degrees.I, Degrees.III, Degrees.V})
_ANALYSIS_MISSING = object()
_TENSION_FULL_SCALE_PRIORITY_SUM = 150.0
_PRIORITY_TO_TENDENCY_WEIGHT = 50.0


def _clip_0_10(value: float) -> float:
    if value <= 0:
        return 0.0
    if value >= 10:
        return 10.0
    return float(value)


def _step_targets(pitch_class: int, resolution: Resolution) -> tuple[int, ...]:
    if resolution == Resolution.STEP_UP:
        return ((pitch_class + 1) % 12, (pitch_class + 2) % 12)
    if resolution == Resolution.STEP_DOWN:
        return ((pitch_class - 1) % 12, (pitch_class - 2) % 12)
    if resolution == Resolution.STEP_EITHER:
        return (
            (pitch_class + 1) % 12,
            (pitch_class + 2) % 12,
            (pitch_class - 1) % 12,
            (pitch_class - 2) % 12,
        )
    return ()


def _degree_from_root_and_pitch_class(root: BaseNote, target_pitch_class: int) -> Optional[Degrees]:
    best: Optional[tuple[int, Degrees]] = None
    for deg in Degrees:
        note_name = root.note_name + deg  # type: ignore[operator]
        try:
            spelled = BaseNote.from_name_and_offset(note_name, target_pitch_class)
        except ValueError:
            continue
        cand = (abs(spelled.shifts), deg)
        if best is None or cand[0] < best[0] or (cand[0] == best[0] and cand[1].value < best[1].value):
            best = cand
    return None if best is None else best[1]


class Chord(FrozenSlotsMixin, metaclass=InternedMeta):
    __slots__ = ("scale", "composition", "base_notes", "quality", "_tension_score", "_target_note_tendencies", "__weakref__")

    @classmethod
    def _cache_key(
        cls,
        scale: Scale,
        composition: AbstractSet[Degrees] | None = None,
    ):
        if composition is None:
            composition = _DEFAULT_TRIAD
        return scale, frozenset(composition)

    def __init__(
        self,
        scale: Scale,
        composition: AbstractSet[Degrees] | None = None,
    ):
        self.scale = scale
        if composition is None:
            composition = _DEFAULT_TRIAD
        self._set_composition(composition)

    def _set_composition(self, composition: AbstractSet[Degrees]) -> None:
        if not all(isinstance(d, Degrees) for d in composition):
            raise TypeError("Chord composition 必须为 Degrees 的集合（表示相对根音的级数差）")
        if Degrees.I not in composition:
            raise ValueError("Chord composition 必须包含 Degrees.I（表示根音）")
        if len(composition) < 2:
            raise ValueError("Chord composition 必须包含 大于等于 2 个级数")
        self.composition: FrozenSet[Degrees] = frozenset(composition)
        self.base_notes: FrozenSet[BaseNote] = frozenset(self.scale[rel] for rel in self.composition)
        interval_set = {self.scale.intervals[rel.value - 1] for rel in self.composition if rel != Degrees.I}
        self.quality = Quality.from_intervals(frozenset(interval_set))
        self._tension_score = _ANALYSIS_MISSING
        self._target_note_tendencies = _ANALYSIS_MISSING
        self._freeze()

    def _ensure_tension_score(self) -> None:
        if self._tension_score is _ANALYSIS_MISSING:
            relations = self.quality.dissonance_relations
            priority_sum = float(sum(rel.priority for rel in relations))
            object.__setattr__(
                self,
                "_tension_score",
                _clip_0_10(10.0 * priority_sum / _TENSION_FULL_SCALE_PRIORITY_SUM),
            )

    def _ensure_target_note_tendencies(self) -> None:
        if self._target_note_tendencies is _ANALYSIS_MISSING:
            relations = self.quality.dissonance_relations
            root_note = self.scale.tonic
            root_pitch_class = root_note.offset
            target_note_tendencies: DefaultDict[Degrees, float] = defaultdict(float)
            for rel in relations:
                weight = float(rel.priority) / _PRIORITY_TO_TENDENCY_WEIGHT
                for interval, resolution in rel.resolution:
                    if resolution == Resolution.NONE:
                        continue
                    source_pitch_class = (root_pitch_class + interval.semitones) % 12
                    for target_pc in _step_targets(source_pitch_class, resolution):
                        degree = _degree_from_root_and_pitch_class(root_note, target_pc)
                        if degree is None:
                            continue
                        target_note_tendencies[degree] += weight
            object.__setattr__(self, "_target_note_tendencies", dict(target_note_tendencies))

    @property
    def tension_score(self) -> float:
        self._ensure_tension_score()
        return cast(float, self._tension_score)

    @property
    def target_note_tendencies(self) -> Dict[Degrees, float]:
        self._ensure_target_note_tendencies()
        return cast(Dict[Degrees, float], self._target_note_tendencies)


    def with_composition(self, composition: AbstractSet[Degrees]) -> "Chord":
        return Chord(self.scale, composition)

    def __getitem__(self, item: Degrees) -> BaseNote:
        return self.scale[item]

    def __str__(self) -> str:
        return f"{self.scale.tonic}{self.quality.name}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Chord):
            return NotImplemented
        return self.scale == other.scale and self.composition == other.composition

    def __contains__(self, item: object) -> bool:
        if isinstance(item, BaseNote):
            return self | item is not None
        return False

    def __or__(self, other: object) -> Optional[Degrees]:
        if isinstance(other, BaseNote):
            degree = self.scale | other
            if degree is None:
                return None
            return degree if degree in self.composition else None
        if isinstance(other, Degrees):
            return other if other in self.composition else None
        return None

    def __iter__(self):
        return iter(self.base_notes)

    def __len__(self) -> int:
        return len(self.base_notes)

    def __sub__(self, other: "Chord") -> tuple[Transition, ColorShift]:
        transition = Transition(
            other.quality,
            (self.scale.tonic.offset - other.scale.tonic.offset) % 12,
            self.quality,
        )
        color_shift = other.scale - self.scale
        return transition, color_shift

    def __add__(self, other: object) -> "Chord":
        if (
            isinstance(other, tuple)
            and len(other) == 2
            and any(isinstance(x, Transition) for x in other)
            and any(isinstance(x, ColorShift) for x in other)
        ):
            transition = next(x for x in other if isinstance(x, Transition))
            color_shift = next(x for x in other if isinstance(x, ColorShift))
        else:
            return NotImplemented
        if transition.src != self.quality:
            raise ValueError("Transition.src 与当前 Chord.quality 不匹配")
        new_scale = self.scale + color_shift
        composition = transition.dst.composition()
        return Chord(new_scale, composition)

    def __hash__(self) -> int:
        return hash((self.scale, self.composition))

    def respell(self, other: "Chord") -> bool:
        return (
            isinstance(other, Chord)
            and frozenset(n.offset for n in self.base_notes)
            == frozenset(n.offset for n in other.base_notes)
        )
    