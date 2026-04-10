import unittest

from composer_theory.domain.base_note import BaseNote
from composer_theory.domain.chord import Chord
from composer_theory.domain.enums.core import Degrees, Intervals, NoteNames
from composer_theory.domain.enums.harmony import ModeAccess, Modes
from composer_theory.domain.key import Key
from composer_theory.domain.mode import Mode
from composer_theory.domain.ids import ChordId, ModeId, SubVScaleRef
from composer_theory.domain.scale import Scale
from composer_theory.relations.chord_in_key import ChordInKeyHit
from composer_theory.relations.chord_in_mode import ChordInModeHit
from composer_theory.relations.mode_in_key import ModeInKeyHit
from composer_theory.resolve.resolver import Resolver


class RelationAnalysisTests(unittest.TestCase):
    def setUp(self) -> None:
        self.resolver = Resolver()
        self.mode_c_ionian = Mode(BaseNote(NoteNames.C), Modes.Ionian)
        self.key_c_ionian = Key(BaseNote(NoteNames.C), Modes.Ionian)
        self.g_aeolian = Scale(
            tonic=BaseNote(NoteNames.G),
            intervals=(Intervals.P1, Intervals.M2, Intervals.m3, Intervals.P4, Intervals.P5, Intervals.m6, Intervals.m7),
        )
        self.chord_gm = Chord(self.g_aeolian, composition=frozenset({Degrees.I, Degrees.III, Degrees.V}))

    def test_chord_in_mode_analysis_allows_non_member_chord(self) -> None:
        hits = self.resolver.resolve(self.chord_gm, self.mode_c_ionian)
        chord_hits = [hit for hit in hits if isinstance(hit, ChordInModeHit)]
        self.assertEqual(len(chord_hits), 1)
        hit = chord_hits[0]
        self.assertFalse(hit.is_member)
        self.assertEqual(hit.chord, self.chord_gm)
        self.assertEqual(hit.color, self.chord_gm - hit._tonic_chord)

    def test_mode_in_key_color_uses_mode_tonic_chord_minus_key_tonic_chord(self) -> None:
        mode_d_dorian = self.key_c_ionian[ModeId(role=Degrees.II, access=ModeAccess.Relative)]
        hits = self.resolver.resolve(mode_d_dorian, self.key_c_ionian)
        mode_hits = [hit for hit in hits if isinstance(hit, ModeInKeyHit)]
        self.assertEqual(len(mode_hits), 1)
        hit = mode_hits[0]
        self.assertTrue(hit.is_member)
        self.assertIsInstance(hit.function_scores, dict)
        self.assertEqual(hit.color, hit._skeleton_chord - hit._main_tonic_chord)

    def test_mode_in_key_allows_non_member_mode(self) -> None:
        mode_d_flat_lydian = Mode(BaseNote(NoteNames.D, -1), Modes.Lydian)
        hits = self.resolver.resolve(mode_d_flat_lydian, self.key_c_ionian)
        mode_hits = [hit for hit in hits if isinstance(hit, ModeInKeyHit)]
        self.assertEqual(len(mode_hits), 1)
        hit = mode_hits[0]
        self.assertFalse(hit.is_member)
        self.assertEqual(hit.mode, mode_d_flat_lydian)
        self.assertEqual(hit.color, hit._skeleton_chord - hit._main_tonic_chord)

    def test_chord_in_key_color_uses_chord_minus_key_main_tonic_chord(self) -> None:
        hits = self.resolver.resolve(self.chord_gm, self.key_c_ionian)
        chord_hits = [hit for hit in hits if isinstance(hit, ChordInKeyHit)]
        self.assertGreater(len(chord_hits), 0)
        hit = chord_hits[0]
        self.assertEqual(hit.color, self.chord_gm - hit._main_tonic_chord)

    def test_chord_in_key_falls_back_to_direct_key_analysis_when_no_mode_match(self) -> None:
        chord_c_sharp_maj = Chord(
            Scale(
                tonic=BaseNote(NoteNames.C, 1),
                intervals=(Intervals.P1, Intervals.M2, Intervals.M3, Intervals.P4, Intervals.P5, Intervals.M6, Intervals.M7),
            ),
            composition=frozenset({Degrees.I, Degrees.III, Degrees.V}),
        )
        hits = self.resolver.resolve(chord_c_sharp_maj, self.key_c_ionian)
        chord_hits = [hit for hit in hits if isinstance(hit, ChordInKeyHit)]
        self.assertEqual(len(chord_hits), 1)
        hit = chord_hits[0]
        self.assertFalse(hit.is_member)
        self.assertEqual(hit.chord, chord_c_sharp_maj)
        self.assertEqual(hit.color, chord_c_sharp_maj - hit._main_tonic_chord)

    def test_chord_in_mode_subv_has_no_turning_points(self) -> None:
        chord = self.mode_c_ionian[ChordId(SubVScaleRef(Degrees.I), frozenset({Degrees.I, Degrees.III, Degrees.VII}))]
        hits = self.resolver.resolve(chord, self.mode_c_ionian)
        chord_hits = [hit for hit in hits if isinstance(hit, ChordInModeHit)]
        self.assertEqual(len(chord_hits), 1)
        hit = chord_hits[0]
        self.assertTrue(hit.is_member)
        self.assertTrue(hit.is_subv)
        self.assertEqual(hit.turning_points(), set())


if __name__ == "__main__":
    unittest.main()

