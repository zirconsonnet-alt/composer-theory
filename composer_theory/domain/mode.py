from types import MappingProxyType
from typing import AbstractSet, Mapping, Set, Tuple, Union, overload
from .base_note import BaseNote
from .scale import Scale
from .chord import Chord
from .ids import ChordId, RootVariantScaleRef, ScaleRef, SubVScaleRef
from .enums.core import Degrees, Intervals
from .mode_specs import MODE_SPECS, ModeSpec
from .enums.harmony import Modes, VariantForm, Tonality
from ._intern import InternedMeta, FrozenSlotsMixin


class Mode(FrozenSlotsMixin, metaclass=InternedMeta):
    __slots__ = ("tonic", "mode_type", "spec", "_scales", "__weakref__")

    @classmethod
    def _cache_key(cls, tonic: BaseNote, mode_type: Modes):
        return tonic, mode_type

    def __init__(self, tonic: BaseNote, mode_type: Modes):
        if (spec := MODE_SPECS.get(mode_type)) is None:
            raise ValueError(f"未知 mode_type: {mode_type}")
        self.tonic = tonic
        self.mode_type = mode_type
        self.spec: ModeSpec = spec
        self._scales: Mapping[VariantForm, Scale] = MappingProxyType(
            {v: Scale(tonic, spec.variants[v]) for v in spec.variants}
        )
        self._freeze()

    def __str__(self) -> str:
        return f"{self.tonic}-{self.mode_type.name}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Mode):
            return NotImplemented
        return self.tonic == other.tonic and self.mode_type == other.mode_type

    def __hash__(self) -> int:
        return hash((self.tonic, self.mode_type.value))

    @property
    def supports_subv(self) -> bool:
        return self.spec.supports_subv

    def _scale_of_root_variant(self, degree: Degrees, variant: VariantForm = VariantForm.Base) -> Scale:
        if not isinstance(degree, Degrees):
            raise TypeError("degree 必须为 Degrees")
        if not isinstance(variant, VariantForm):
            raise TypeError("variant 必须为 VariantForm")
        if variant not in self._scales:
            raise ValueError(f"{self.mode_type.name} 不支持 variant: {variant.name}")
        parent_scale = self._scales[variant]
        derived_tonic = parent_scale[degree]
        def _rotated_note(target_degree: Degrees) -> BaseNote:
            return parent_scale[degree + (target_degree - Degrees.I)]
        intervals = tuple(derived_tonic | _rotated_note(d) for d in Degrees)
        if intervals[0] != Intervals.P1:
            raise ValueError("派生音阶构造失败：I 级必须为 P1")
        try:
            return Scale(derived_tonic, intervals)
        except ValueError as e:
            raise ValueError(
                f"此派生调式在当前 MAX_SHIFTS={BaseNote.MAX_SHIFTS} 约束下无法拼写："
                f"mode={self}, degree={degree.name}, variant={variant.name}；原因：{e}"
            ) from e

    def _canonical_scale_ref(self, scale_query: ScaleRef) -> ScaleRef:
        if isinstance(scale_query, SubVScaleRef):
            return scale_query
        if not isinstance(scale_query, RootVariantScaleRef):
            raise TypeError(f"未知 scale_query: {scale_query!r}")

        resolved = self._scale_of_root_variant(scale_query.root_degree, scale_query.variant)
        if not self.supports_subv:
            return RootVariantScaleRef(
                root_degree=scale_query.root_degree,
                variant=scale_query.variant,
            )
        for target_degree in Degrees:
            try:
                subv_scale = self[SubVScaleRef(target_degree=target_degree)]
            except ValueError:
                continue
            if resolved == subv_scale:
                return SubVScaleRef(target_degree=target_degree)
        return RootVariantScaleRef(
            root_degree=scale_query.root_degree,
            variant=scale_query.variant,
        )

    def _canonical_chord_id(self, chord_id: ChordId) -> ChordId:
        composition = frozenset(chord_id.composition)
        if Degrees.I not in composition:
            raise ValueError("ChordId.composition 必须包含 Degrees.I")
        return ChordId(
            scale_ref=self._canonical_scale_ref(chord_id.scale_ref),
            composition=composition,
        )

    def chord(self, scale_ref: ScaleRef, composition: AbstractSet[Degrees] | None = None) -> Chord:
        canonical_scale_ref = self._canonical_scale_ref(scale_ref)
        if composition is None:
            return Chord(self[canonical_scale_ref])
        return self[
            ChordId(
                scale_ref=canonical_scale_ref,
                composition=frozenset(composition),
            )
        ]

    def _subv_scale_of_target_degree(self, target_degree: Degrees) -> Scale:
        profile = self.spec.subv_profile
        if profile is None:
            raise ValueError(f"{self.mode_type.name} 不支持 SubV")
        target = self._scale_of_root_variant(Degrees.I, VariantForm.Base)[target_degree]
        sub_root = target + Intervals.m2
        return Scale(sub_root, profile)

    def _resolve_scale_ref(self, scale_ref: ScaleRef) -> Scale:
        if isinstance(scale_ref, RootVariantScaleRef):
            return self._scale_of_root_variant(scale_ref.root_degree, scale_ref.variant)
        if isinstance(scale_ref, SubVScaleRef):
            return self._subv_scale_of_target_degree(scale_ref.target_degree)
        raise TypeError(f"未知 scale_ref: {scale_ref!r}")

    @overload
    def __getitem__(self, key: ScaleRef) -> Scale: ...
    @overload
    def __getitem__(self, key: ChordId) -> Chord: ...

    def __getitem__(self, key: Union[ScaleRef, ChordId]) -> Union[Scale, Chord]:
        if isinstance(key, (RootVariantScaleRef, SubVScaleRef)):
            canonical_scale_ref = self._canonical_scale_ref(key)
            return self._resolve_scale_ref(canonical_scale_ref)
        if isinstance(key, ChordId):
            canonical = self._canonical_chord_id(key)
            return Chord(self[canonical.scale_ref], canonical.composition)
        raise KeyError(f"Mode 没有这个键: {key!r}")

    def __contains__(self, key: Union[BaseNote, Scale, Chord]) -> bool:
        if isinstance(key, BaseNote):
            return len(self | key) > 0
        if isinstance(key, Scale):
            return len(self | key) > 0
        if isinstance(key, Chord):
            return len(self | key) > 0
        return False

    def __or__(self, key: Union[BaseNote, Scale, Chord]) -> Set[Tuple[Degrees, VariantForm]]:
        result: Set[Tuple[Degrees, VariantForm]] = set()
        if isinstance(key, BaseNote):
            for variant in self._scales.keys():
                for degree in Degrees:
                    if key in self._scale_of_root_variant(degree, variant):
                        result.add((degree, variant))
            return result
        if isinstance(key, Scale):
            for variant in self._scales.keys():
                for degree in Degrees:
                    if self._scale_of_root_variant(degree, variant) == key:
                        result.add((degree, variant))
            return result
        if isinstance(key, Chord):
            for variant in self._scales.keys():
                for degree in Degrees:
                    if self._scale_of_root_variant(degree, variant) == key.scale:
                        result.add((degree, variant))
            return result
        return result

    @property
    def characteristic_degree(self) -> Degrees:
        return self.spec.characteristic_degree

    @property
    def tonality(self) -> Tonality:
        base_intervals = self.spec.variants[VariantForm.Base]
        third = base_intervals[2]
        return Tonality.maj if third == Intervals.M3 else Tonality.min
    
    def respell(self, other: "Mode") -> bool:
        return (
            isinstance(other, Mode)
            and self.mode_type == other.mode_type
            and self.tonic.respell(other.tonic)
        )

