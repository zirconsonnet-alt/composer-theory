import unittest

from composer_theory.domain.base_note import BaseNote
from composer_theory.domain.chord import Chord
from composer_theory.domain.scale import Scale
from composer_theory.domain.enums.core import Degrees, NoteNames
from composer_theory.domain.enums.harmony import (
    Modes,
    VariantForm,
)
from composer_theory.domain.mode import Mode
from composer_theory.domain.ids import ChordId, RootVariantScaleRef, SubVScaleRef
from composer_theory.tools import scale_ref_variant


class IdIndexingTests(unittest.TestCase):
    def test_mode_scale_ref_index_returns_scale(self) -> None:
        mode = Mode(BaseNote(NoteNames.C), Modes.Ionian)
        got = mode[RootVariantScaleRef(Degrees.I, VariantForm.Base)]
        self.assertIsInstance(got, Scale)
        self.assertEqual(str(got), "C, D, E, F, G, A, B")

    def test_mode_subv_scale_ref_index_returns_scale(self) -> None:
        mode = Mode(BaseNote(NoteNames.C), Modes.Ionian)
        got = mode[SubVScaleRef(Degrees.I)]
        self.assertIsInstance(got, Scale)
        self.assertEqual(str(got), "Db, Eb, F, Gb, Ab, Bb, Cb")
        self.assertEqual(scale_ref_variant(SubVScaleRef(Degrees.I)), VariantForm.SubV)

    def test_mode_without_subv_rejects_subv_scale_ref(self) -> None:
        mode = Mode(BaseNote(NoteNames.C), Modes.Lydian)
        with self.assertRaisesRegex(ValueError, r"Lydian 不支持 SubV"):
            _ = mode[SubVScaleRef(Degrees.I)]

    def test_mode_chord_id_equivalent_to_named_scale_ref_entry(self) -> None:
        mode = Mode(BaseNote(NoteNames.C), Modes.Ionian)
        composition = frozenset({Degrees.I, Degrees.III, Degrees.V})
        got = mode[ChordId(RootVariantScaleRef(Degrees.V, VariantForm.Base), composition)]
        expected = mode.chord(RootVariantScaleRef(Degrees.V, VariantForm.Base))
        self.assertIsInstance(got, Chord)
        self.assertEqual(got, expected)

    def test_mode_chord_id_with_composition_equivalent_to_named_scale_ref_entry(self) -> None:
        mode = Mode(BaseNote(NoteNames.C), Modes.Ionian)
        composition = frozenset({Degrees.I, Degrees.III, Degrees.V, Degrees.VII})
        got = mode[ChordId(RootVariantScaleRef(Degrees.II, VariantForm.Base), composition)]
        expected = mode.chord(RootVariantScaleRef(Degrees.II, VariantForm.Base), composition)
        self.assertEqual(got, expected)

    def test_mode_subv_chord_id_builds_subv_chord(self) -> None:
        mode = Mode(BaseNote(NoteNames.C), Modes.Ionian)
        composition = frozenset({Degrees.I, Degrees.III, Degrees.V, Degrees.VII})
        got = mode[ChordId(SubVScaleRef(Degrees.I), composition)]
        self.assertEqual(str(got), "Db_7")

    def test_mode_chord_named_entry_builds_subv_chord(self) -> None:
        mode = Mode(BaseNote(NoteNames.C), Modes.Ionian)
        composition = frozenset({Degrees.I, Degrees.III, Degrees.V, Degrees.VII})
        got = mode.chord(SubVScaleRef(Degrees.I), composition)
        self.assertEqual(str(got), "Db_7")

    def test_mode_rejects_legacy_tuple_indexing(self) -> None:
        mode = Mode(BaseNote(NoteNames.C), Modes.Ionian)
        with self.assertRaises(KeyError):
            _ = mode[(Degrees.V, VariantForm.Base)]

    def test_mode_scale_ref_entry_canonicalizes_equivalent_root_variant(self) -> None:
        mode = Mode(BaseNote(NoteNames.C), Modes.Dorian)
        got = mode[RootVariantScaleRef(Degrees.VII, VariantForm.Base)]
        expected = mode[SubVScaleRef(Degrees.VI)]
        self.assertNotEqual(got, expected)

    def test_mode_chord_id_requires_degree_i_in_composition(self) -> None:
        mode = Mode(BaseNote(NoteNames.C), Modes.Ionian)
        with self.assertRaisesRegex(ValueError, r"ChordId\.composition 必须包含 Degrees\.I"):
            _ = mode[
                ChordId(
                    RootVariantScaleRef(Degrees.V, VariantForm.Base),
                    frozenset({Degrees.III, Degrees.V}),
                )
            ]


if __name__ == "__main__":
    unittest.main()

