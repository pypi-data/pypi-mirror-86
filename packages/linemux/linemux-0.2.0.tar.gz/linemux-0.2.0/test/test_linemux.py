import pathlib
import shutil
from io import StringIO

from linemux.command import LineMultiplexer


def create_output_directory() -> LineMultiplexer:
    dir = pathlib.Path('test') / '_directory'
    shutil.rmtree(dir, ignore_errors=True)
    dir.mkdir(parents=True,exist_ok=True)
    mux = LineMultiplexer()
    mux.output = dir
    return mux


def read_file(file: pathlib.Path) -> str:
    with file.open("rt") as f:
        return f.read()


def test_basic():
    mux = create_output_directory()
    data = StringIO("aa\nbb\ncc\nbb\ncc")
    mux.process(data)
    assert read_file(mux.output / 'aa') == 'aa\n'
    assert read_file(mux.output / 'bb') == 'bb\nbb\n'
    assert read_file(mux.output / 'cc') == 'cc\ncc'


def test_custom_key():
    mux = create_output_directory()
    mux.key = r"\S+"
    data = StringIO("1 a\n2 b\n3 c\n2 A\n3 B\n2 C")
    mux.process(data)
    assert read_file(mux.output / '1') == '1 a\n'
    assert read_file(mux.output / '2') == '2 b\n2 A\n2 C'
    assert read_file(mux.output / '3') == '3 c\n3 B\n'


def test_character_filtering():
    mux = create_output_directory()
    data = StringIO("a,a\nb|\n--b\n!!b\na!a\na,a\nb|b\n")
    mux.process(data)
    assert read_file(mux.output / 'aa') == 'a,a\na,a\n'
    assert read_file(mux.output / 'aa_2') == 'a!a\n'
    assert read_file(mux.output / 'b') == 'b|\n'
    assert read_file(mux.output / '--b') == '--b\n'
    assert read_file(mux.output / 'b_2') == '!!b\n'
    assert read_file(mux.output / 'bb') == 'b|b\n'


def test_max_line_length():
    mux = create_output_directory()
    mux.max_name_length = 5
    data = StringIO("aaaaaaaaaaaaaa\nbvvvvvv\n12345678\naaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n")
    mux.process(data)
    assert read_file(mux.output / 'aaaaa') == 'aaaaaaaaaaaaaa\n'
    assert read_file(mux.output / 'aaa_2') == 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n'
    assert read_file(mux.output / 'bvvvv') == 'bvvvvvv\n'
    assert read_file(mux.output / '12345') == '12345678\n'


def test_max_line_extreme():
    mux = create_output_directory()
    mux.max_name_length = 1
    data = StringIO("aaaaaaaaaaaaaa\nbvvvvvv\n12345678\naaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n")
    mux.process(data)
    assert read_file(mux.output / 'a') == 'aaaaaaaaaaaaaa\n'
    assert read_file(mux.output / '_2') == 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n'
    assert read_file(mux.output / 'b') == 'bvvvvvv\n'
    assert read_file(mux.output / '1') == '12345678\n'


def test_key_and_value():
    mux = create_output_directory()
    mux.key = r".*:"
    data = StringIO("a:This is a\nb: This is bb\na\na: This is aa\nb:This is bbbb\na: This is aaa")
    mux.process(data)
    assert read_file(mux.output / 'a') == 'a:This is a\na: This is aa\na: This is aaa'
    assert read_file(mux.output / 'b') == 'b: This is bb\nb:This is bbbb\n'


def test_remove_key():
    mux = create_output_directory()
    mux.key = r".*:"
    mux.remove_key = True
    data = StringIO("a:This is a\nb: This is bb\na\na: This is aa\nb:This is bbbb\na: This is aaa")
    mux.process(data)
    assert read_file(mux.output / 'a') == 'This is a\n This is aa\n This is aaa'
    assert read_file(mux.output / 'b') == ' This is bb\nThis is bbbb\n'
