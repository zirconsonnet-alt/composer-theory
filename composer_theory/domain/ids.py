from dataclasses import dataclass
from typing import FrozenSet, Union
from .enums.core import Degrees, NoteNames
from .enums.harmony import ModeAccess, Modes, VariantForm

__all__ = [
    "KeyId",
    "ModeId",
    "RootVariantScaleRef",
    "SubVScaleRef",
    "ChordId",
]


@dataclass(frozen=True, slots=True)
class KeyId:
    tonic: NoteNames
    main_mode_type: Modes


@dataclass(frozen=True, slots=True)
class ModeId:
    role: Union[Modes, Degrees]
    access: ModeAccess = ModeAccess.Relative


@dataclass(frozen=True, slots=True)
class RootVariantScaleRef:
    root_degree: Degrees
    variant: VariantForm = VariantForm.Base


@dataclass(frozen=True, slots=True)
class SubVScaleRef:
    target_degree: Degrees


ScaleRef = Union[RootVariantScaleRef, SubVScaleRef]


@dataclass(frozen=True, slots=True)
class ChordId:
    scale_ref: ScaleRef
    composition: FrozenSet[Degrees]

    @property
    def is_subv(self) -> bool:
        return isinstance(self.scale_ref, SubVScaleRef)
