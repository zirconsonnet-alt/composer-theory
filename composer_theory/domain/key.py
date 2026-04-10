from typing import Optional, Set, Tuple, Union, overload
from .mode import Mode
from .chord import Chord
from .scale import Scale
from .ids import ModeId, RootVariantScaleRef
from .base_note import BaseNote
from .mode_specs import degree_mode
from .enums.core import Degrees, Intervals
from .enums.harmony import VariantForm, Modes, ModeAccess
from ._intern import InternedMeta, FrozenSlotsMixin


ModeIndex = Tuple[Degrees, ModeAccess]


class Key(FrozenSlotsMixin, metaclass=InternedMeta):
    __slots__ = ("tonic", "main_mode_type", "__weakref__")

    @classmethod
    def _cache_key(cls, tonic: BaseNote, main_mode_type: Modes):
        return tonic, main_mode_type

    def __init__(self, tonic: BaseNote, main_mode_type: Modes):
        self.tonic = tonic
        self.main_mode_type = main_mode_type
        self._freeze()

    def __str__(self) -> str:
        return f"{self[self.main_mode_type]}-Key"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Key):
            return NotImplemented
        return self.tonic == other.tonic and self.main_mode_type == other.main_mode_type

    def __hash__(self) -> int:
        return hash((self.tonic, self.main_mode_type.value))

    @overload
    def __getitem__(self, key: Modes) -> Mode: ...
    @overload
    def __getitem__(self, key: Degrees) -> Mode: ...
    @overload
    def __getitem__(self, key: ModeIndex) -> Mode: ...
    @overload
    def __getitem__(self, key: ModeId) -> Mode: ...

    def __getitem__(self, key: Union[Modes, Degrees, ModeIndex, ModeId]) -> Mode:
        if isinstance(key, ModeId):
            role = key.role
            access = key.access
            if isinstance(role, Modes):
                return self[role]
            if not isinstance(role, Degrees):
                raise KeyError(f"Key 没有这个键: {key!r}")
            return self[(role, access)]
        if isinstance(key, Modes):
            return Mode(self.tonic, key)
        if isinstance(key, Degrees):
            main_mode = Mode(self.tonic, self.main_mode_type)
            main_scale = main_mode[RootVariantScaleRef(Degrees.I, VariantForm.Base)]
            derived_tonic = main_scale[key]
            derived_mode_type = degree_mode(self.main_mode_type, key)
            return Mode(derived_tonic, derived_mode_type)
        if isinstance(key, tuple) and len(key) == 2:
            degree, access = key
            if not isinstance(degree, Degrees) or not isinstance(access, ModeAccess):
                raise KeyError(f"Key 没有这个键: {key!r}")
            if access == ModeAccess.Relative:
                return self[degree]
            raise KeyError(f"Key 未处理的 ModeAccess: {access!r}")
        raise KeyError(f"Key 没有这个键: {key!r}")

    def __contains__(self, key: Union[Mode, Scale, BaseNote, Chord]) -> bool:
        if isinstance(key, Mode):
            return self | key is not None
        if isinstance(key, (Scale, BaseNote, Chord)):
            return bool(self | key)
        return False

    def __or__(self, key: Union[Mode, Scale, BaseNote, Chord]) -> Optional[Union[Modes, Degrees, Set[Union[Modes, Degrees]]]]:
        if isinstance(key, Mode):
            for mt in Modes:
                if self[mt] == key:
                    return mt
            for deg in Degrees:
                if self[deg] == key:
                    return deg
            return None
        if isinstance(key, (Scale, BaseNote, Chord)):
            hits: Set[Union[Modes, Degrees]] = set()
            for mt in Modes:
                if key in self[mt]:
                    hits.add(mt)
            for deg in Degrees:
                if key in self[deg]:
                    hits.add(deg)
            return hits
        return None

    def respell(self, other: "Key") -> bool:
        return (
            isinstance(other, Key)
            and self.main_mode_type == other.main_mode_type
            and self.tonic.respell(other.tonic)
        )

