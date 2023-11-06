from pathlib import Path
from takenote.note import read_markdown, write_note
from loguru import logger

TEST_NOTE_STR = """

"""

test_note_path = Path(__file__).parent / "test_note.md"
test_note_output = Path(__file__).parent / "output_test.md"


def test_writing():
    """
    Test the writing of markdown files, not an aggressive test, just copying essentially.
    Test is verified visually.
    """
    note = read_markdown(test_note_path)
    logger.info(note.title)
    write_note(test_note_output, note)


def test_reading():
    """Test reading a Markdown file. Test is verified visually."""
    note = read_markdown(test_note_path)
    logger.info(note.title)


if __name__ == "__main__":
    test_reading()
    test_writing()
