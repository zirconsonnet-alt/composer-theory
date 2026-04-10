from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main() -> None:
    from composer_theory.domain.base_note import BaseNote
    from composer_theory.domain.enums.core import Degrees, NoteNames
    from composer_theory.domain.enums.harmony import Modes
    from composer_theory.domain.ids import SubVScaleRef
    from composer_theory.domain.mode import Mode

    mode = Mode(BaseNote(NoteNames.C), Modes.Ionian)

    print("C Ionian SubV scales")
    for degree in Degrees:
        scale = mode[SubVScaleRef(target_degree=degree)]
        notes = ", ".join(str(note) for note in scale)
        print(f"{degree.name}: {notes}")


if __name__ == "__main__":
    main()
