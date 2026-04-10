from dataclasses import dataclass
from types import MappingProxyType
from typing import Dict, Mapping, Tuple

from .enums.core import Degrees, Intervals
from .enums.harmony import Modes, VariantForm

__all__ = ["ModeSpec"]


_IntervalProfile = Tuple[Intervals, ...]


@dataclass(frozen=True, slots=True)
class ModeSpec:
    mode: Modes
    variants: Mapping[VariantForm, _IntervalProfile]
    subv_profile: _IntervalProfile | None
    characteristic_degree: Degrees

    @property
    def supports_subv(self) -> bool:
        return self.subv_profile is not None


def _patch_profile(base: _IntervalProfile, changes: Mapping[Degrees, Intervals]) -> _IntervalProfile:
    lst = list(base)
    for deg, itv in changes.items():
        idx = deg.value - 1
        lst[idx] = itv
    return tuple(lst)


def _make_spec(
    mode: Modes,
    base: _IntervalProfile,
    characteristic_degree: Degrees,
    *,
    ascending_changes: Mapping[Degrees, Intervals] | None = None,
    descending_changes: Mapping[Degrees, Intervals] | None = None,
    subv_profile: _IntervalProfile | None = None,
) -> ModeSpec:
    variants: Dict[VariantForm, _IntervalProfile] = {VariantForm.Base: base}
    if ascending_changes:
        variants[VariantForm.Ascending] = _patch_profile(base, ascending_changes)
    if descending_changes:
        variants[VariantForm.Descending] = _patch_profile(base, descending_changes)
    return ModeSpec(
        mode=mode,
        variants=MappingProxyType(dict(variants)),
        subv_profile=subv_profile,
        characteristic_degree=characteristic_degree,
    )


_MODE_SPECS: Mapping[Modes, ModeSpec] = MappingProxyType({
    Modes.Ionian: _make_spec(
        mode=Modes.Ionian,
        base=(Intervals.P1, Intervals.M2, Intervals.M3, Intervals.P4, Intervals.P5, Intervals.M6, Intervals.M7),
        characteristic_degree=Degrees.VII,
        subv_profile=(Intervals.P1, Intervals.M2, Intervals.M3, Intervals.P4, Intervals.P5, Intervals.M6, Intervals.m7)
    ),

    Modes.Dorian: _make_spec(
        mode=Modes.Dorian,
        base=(Intervals.P1, Intervals.M2, Intervals.m3, Intervals.P4, Intervals.P5, Intervals.M6, Intervals.m7),
        characteristic_degree=Degrees.VI,
        ascending_changes={Degrees.VII: Intervals.M7},
        descending_changes={Degrees.VI: Intervals.m6},
        subv_profile=(Intervals.P1, Intervals.m2, Intervals.m3, Intervals.P4, Intervals.P5, Intervals.m6, Intervals.m7)
    ),
    Modes.Phrygian: _make_spec(
        mode=Modes.Phrygian,
        base=(Intervals.P1, Intervals.m2, Intervals.m3, Intervals.P4, Intervals.P5, Intervals.m6, Intervals.m7),
        characteristic_degree=Degrees.II,
        ascending_changes={
            Degrees.II: Intervals.M2,
            Degrees.VI: Intervals.M6,
            Degrees.VII: Intervals.M7,
        },
        subv_profile=(Intervals.P1, Intervals.m2, Intervals.m3, Intervals.P4, Intervals.P5, Intervals.m6, Intervals.m7)
    ),
    Modes.Lydian: _make_spec(
        mode=Modes.Lydian,
        base=(Intervals.P1, Intervals.M2, Intervals.M3, Intervals.A4, Intervals.P5, Intervals.M6, Intervals.M7),
        characteristic_degree=Degrees.IV,
    ),
    Modes.Mixolydian: _make_spec(
        mode=Modes.Mixolydian,
        base=(Intervals.P1, Intervals.M2, Intervals.M3, Intervals.P4, Intervals.P5, Intervals.M6, Intervals.m7),
        characteristic_degree=Degrees.VII,
        ascending_changes={Degrees.VII: Intervals.M7},
        subv_profile=(Intervals.P1, Intervals.m2, Intervals.m3, Intervals.P4, Intervals.P5, Intervals.m6, Intervals.m7)
    ),
    Modes.Aeolian: _make_spec(
        mode=Modes.Aeolian,
        base=(Intervals.P1, Intervals.M2, Intervals.m3, Intervals.P4, Intervals.P5, Intervals.m6, Intervals.m7),
        characteristic_degree=Degrees.IV,
        ascending_changes={
            Degrees.VI: Intervals.M6,
            Degrees.VII: Intervals.M7,
        },
        subv_profile=(Intervals.P1, Intervals.m2, Intervals.m3, Intervals.P4, Intervals.P5, Intervals.m6, Intervals.m7)
    ),
    Modes.Locrian: _make_spec(
        mode=Modes.Locrian,
        base=(Intervals.P1, Intervals.m2, Intervals.m3, Intervals.P4, Intervals.d5, Intervals.m6, Intervals.m7),
        characteristic_degree=Degrees.V,
        subv_profile=(Intervals.P1, Intervals.m2, Intervals.m3, Intervals.P4, Intervals.d5, Intervals.m6, Intervals.m7)
    ),
})


def _degree_mode(parent: Modes, degree: Degrees) -> Modes:
    if not isinstance(parent, Modes):
        raise TypeError("parent 必须是 Modes")
    if not isinstance(degree, Degrees):
        raise TypeError("degree 必须是 Degrees")
    modes = tuple(Modes)
    i = modes.index(parent)
    shift = degree.value - 1
    j = (i + shift) % len(modes)
    return modes[j]
