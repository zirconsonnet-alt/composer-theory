from typing import Union
from .domain.enums.core import Degrees
from .domain.enums.harmony import Modes, ModeAccess, VariantForm
from .domain.ids import ModeId, RootVariantScaleRef, ScaleRef, SubVScaleRef

__all__ = [
    "effective_role_degree",
    "map_degree_to_target_root",
    "map_target_root_to_degree",
    "is_root_variant_scale_ref",
    "is_subv_scale_ref",
    "scale_ref_kind",
    "scale_ref_root_degree",
    "scale_ref_variant",
    "scale_ref_target_degree",
]


def effective_role_degree(mode: Union[ModeId, Modes, Degrees]) -> Degrees:
    if isinstance(mode, ModeId):
        if isinstance(mode.role, Modes):
            return Degrees.I
        if not isinstance(mode.role, Degrees):
            raise TypeError("ModeId.role 必须为 Modes 或 Degrees")
        if mode.access == ModeAccess.Relative:
            return mode.role
        return Degrees.I
    if isinstance(mode, Modes):
        return Degrees.I
    if isinstance(mode, Degrees):
        return mode
    raise TypeError("mode 必须为 ModeId / Modes / Degrees")

def map_degree_to_target_root(mode: Union[ModeId, Modes, Degrees], chord_degree: Degrees) -> Degrees:
    return chord_degree + effective_role_degree(mode)

def map_target_root_to_degree(mode: Union[ModeId, Modes, Degrees], target_root: Degrees) -> Degrees:
    return target_root - effective_role_degree(mode)


def is_root_variant_scale_ref(scale_ref: ScaleRef) -> bool:
    return isinstance(scale_ref, RootVariantScaleRef)


def is_subv_scale_ref(scale_ref: ScaleRef) -> bool:
    return isinstance(scale_ref, SubVScaleRef)


def scale_ref_kind(scale_ref: ScaleRef) -> str:
    if isinstance(scale_ref, RootVariantScaleRef):
        return "root_variant"
    if isinstance(scale_ref, SubVScaleRef):
        return "subv"
    raise TypeError("scale_ref 必须为 RootVariantScaleRef / SubVScaleRef")


def scale_ref_root_degree(scale_ref: ScaleRef) -> Degrees:
    if isinstance(scale_ref, RootVariantScaleRef):
        return scale_ref.root_degree
    if isinstance(scale_ref, SubVScaleRef):
        return scale_ref.target_degree + Degrees.II
    raise TypeError("scale_ref 必须为 RootVariantScaleRef / SubVScaleRef")


def scale_ref_variant(scale_ref: ScaleRef) -> VariantForm:
    if isinstance(scale_ref, RootVariantScaleRef):
        return scale_ref.variant
    if isinstance(scale_ref, SubVScaleRef):
        return VariantForm.SubV
    raise TypeError("scale_ref 必须为 RootVariantScaleRef / SubVScaleRef")


def scale_ref_target_degree(scale_ref: ScaleRef) -> Degrees | None:
    if isinstance(scale_ref, RootVariantScaleRef):
        return None
    if isinstance(scale_ref, SubVScaleRef):
        return scale_ref.target_degree
    raise TypeError("scale_ref 必须为 RootVariantScaleRef / SubVScaleRef")

