from typing import List, Tuple, Union
from ..domain.chord import Chord
from ..domain.enums.core import Degrees
from ..domain.enums.harmony import ModeAccess, Modes, VariantForm
from ..domain.key import Key
from ..domain.mode import Mode
from ..domain.ids import ChordId, ModeId, RootVariantScaleRef, SubVScaleRef
from ..relations.chord_in_key import ChordInKeyHit
from ..relations.chord_in_mode import ChordInModeHit
from ..relations.mode_in_key import ModeInKeyHit

_AnyResolveHit = Union[
    ChordInModeHit,
    ModeInKeyHit,
    ChordInKeyHit,
]


class Resolver:
    def resolve(self, a, b) -> List[_AnyResolveHit]:
        hits: List[_AnyResolveHit] = []
        swapped = self._should_swap(a, b)
        if swapped:
            a, b = b, a
        if isinstance(a, Chord) and isinstance(b, Mode):
            hits.extend(self._resolve_chord_in_mode(chord=a, mode=b))
            return hits
        if isinstance(a, Mode) and isinstance(b, Key):
            hits.extend(self._resolve_mode_in_key(mode=a, key=b))
            return hits
        if isinstance(a, Chord) and isinstance(b, Key):
            hits.extend(self._resolve_chord_in_key(chord=a, key=b))
            return hits
        return hits

    def _resolve_chord_in_mode(self, chord: Chord, mode: Mode) -> List[_AnyResolveHit]:
        hits = self._resolve_chord_in_mode_exact(chord=chord, mode=mode)
        if hits:
            return hits
        return [ChordInModeHit(mode=mode, chord_id=None, chord=chord)]

    @staticmethod
    def _resolve_mode_in_key(mode: Mode, key: Key) -> List[_AnyResolveHit]:
        hits: List[_AnyResolveHit] = []
        for mt in Modes:
            if key[mt] == mode:
                hits.append(ModeInKeyHit(key=key, mode_id=ModeId(role=mt, access=ModeAccess.Substitute)))
        for deg in Degrees:
            if key[deg] == mode:
                hits.append(ModeInKeyHit(key=key, mode_id=ModeId(role=deg, access=ModeAccess.Relative)))
        if hits:
            return hits
        return [ModeInKeyHit(key=key, mode_id=None, mode=mode)]

    def _resolve_chord_in_key(self, chord: Chord, key: Key) -> List[_AnyResolveHit]:
        hits: List[_AnyResolveHit] = []

        def extend(mode: Mode, mode_id: ModeId) -> None:
            mode_in_key_hit = ModeInKeyHit(key=key, mode_id=mode_id)
            for h in self._resolve_chord_in_mode_exact(chord=chord, mode=mode):
                hits.append(
                    ChordInKeyHit(
                        mode_in_key_hit=mode_in_key_hit,
                        chord_id=h.chord_id,
                    )
                )

        for mt in Modes:
            m = key[mt]
            extend(m, ModeId(role=mt, access=ModeAccess.Substitute))
        for deg in Degrees:
            m = key[deg]
            extend(m, ModeId(role=deg, access=ModeAccess.Relative))
        if hits:
            return hits
        return [
            ChordInKeyHit(
                mode_in_key_hit=ModeInKeyHit(
                    key=key,
                    mode_id=ModeId(role=key.main_mode_type, access=ModeAccess.Substitute),
                ),
                chord_id=None,
                chord=chord,
            )
        ]

    @staticmethod
    def _should_swap(a, b) -> bool:
        supported = (
            (Chord, Mode),
            (Mode, Key),
            (Chord, Key),
        )

        def is_supported(x, y) -> bool:
            return any(isinstance(x, A) and isinstance(y, B) for (A, B) in supported)

        return (not is_supported(a, b)) and is_supported(b, a)

    @staticmethod
    def _mode_variants(mode: Mode) -> Tuple[VariantForm, ...]:
        return tuple(mode.spec.variants.keys())

    def _resolve_chord_in_mode_exact(self, chord: Chord, mode: Mode) -> List[ChordInModeHit]:
        hits: List[_AnyResolveHit] = []
        seen: set[ChordId] = set()
        variants = self._mode_variants(mode)
        refs = [RootVariantScaleRef(root_degree=degree, variant=variant) for variant in variants for degree in Degrees]
        if mode.supports_subv:
            refs.extend(SubVScaleRef(target_degree=degree) for degree in Degrees)
        for scale_ref in refs:
            try:
                candidate = Chord(mode[scale_ref], chord.composition)
            except ValueError:
                continue
            if candidate.base_notes != chord.base_notes:
                continue
            chord_id = mode._canonical_chord_id(
                ChordId(
                    scale_ref=scale_ref,
                    composition=frozenset(chord.composition),
                )
            )
            if chord_id in seen:
                continue
            seen.add(chord_id)
            hits.append(
                ChordInModeHit(
                    mode=mode,
                    chord_id=chord_id,
                )
            )
        return hits

