import itertools
from typing import List, Set, Tuple

from ..domain.base_note import BaseNote
from ..domain.color_shift import ColorShift
from ..domain.enums.core import Degrees, NoteNames
from ..domain.enums.harmony import Modes, ModeAccess, VariantForm
from ..domain.ids import RootVariantScaleRef, SubVScaleRef
from ..domain.key import Key
from ..domain.mode import Mode

__all__ = ["get_all_color_shifts"]

_BASE_SCALE_REF = RootVariantScaleRef(Degrees.I, VariantForm.Base)


def _mode_color_shift(src: Mode, dst: Mode) -> ColorShift:
    src_scale = src[_BASE_SCALE_REF]
    dst_scale = dst[_BASE_SCALE_REF]
    return src_scale - dst_scale


def _access_modes(key: Key) -> List[Tuple[ModeAccess, Degrees | Modes, Mode]]:
    rel = [(ModeAccess.Relative, d, key[d]) for d in Degrees]
    sub = [(ModeAccess.Substitute, m, key[m]) for m in Modes]
    return rel + sub


def _build_color_shifts() -> Set[ColorShift]:
    shifts: Set[ColorShift] = set()
    key = Key(BaseNote(NoteNames.C), Modes.Ionian)
    modes = _access_modes(key)

    def _try_add(src: Mode, dst: Mode) -> None:
        try:
            shifts.add(_mode_color_shift(src, dst))
        except ValueError:
            return

    for (_, _, src), (_, _, dst) in itertools.permutations(modes, 2):
        _try_add(src, dst)
    for deg in Degrees:
        rel_mode = key[deg]
        if not rel_mode.supports_subv:
            continue
        subv_scale = rel_mode[SubVScaleRef(target_degree=Degrees.I)]
        subv_mode = Mode(subv_scale.tonic, Modes.Mixolydian)
        _try_add(subv_mode, rel_mode)
        _try_add(rel_mode, subv_mode)
    return shifts


_ALL_COLOR_SHIFTS: Set[ColorShift] | None = None


def get_all_color_shifts() -> Set[ColorShift]:
    global _ALL_COLOR_SHIFTS
    if _ALL_COLOR_SHIFTS is None:
        _ALL_COLOR_SHIFTS = _build_color_shifts()
    return _ALL_COLOR_SHIFTS
