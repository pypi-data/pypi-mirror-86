import pathlib
import shutil
import subprocess

import pytest
from linemux import command
from test.test_linemux import read_file

OUT = 'test/_directory'


def test_sample_urls(capsys):
    shutil.rmtree(OUT, ignore_errors=True)
    command.main(['-d', OUT, 'test/sample.urls'])
    stdout = capsys.readouterr().out
    print(stdout)
    assert stdout.split('\n')[0:-1] == [
        'httpswww.oulu.fi', 'httpswww.google.com', 'httpswww.oulu.fi_2', 'httpwww.oulu.fiuniversity']
    assert read_file(pathlib.Path(OUT) / 'httpswww.oulu.fi') == 'https://www.oulu.fi\nhttps://www.oulu.fi\n'
    assert read_file(pathlib.Path(OUT) / 'httpswww.oulu.fi_2') == 'https://www.oulu.fi/\nhttps://www.oulu.fi/\n'
    assert read_file(pathlib.Path(OUT) / 'httpwww.oulu.fiuniversity') == 'http://www.oulu.fi/university/\n'
    assert read_file(pathlib.Path(OUT) / 'httpswww.google.com') == 'https://www.google.com\nhttps://www.google.com\n'


def test_sample_memorydump():
    shutil.rmtree(OUT, ignore_errors=True)
    p = subprocess.run(['sh', 'sample_memorydump.sh'], cwd='test')
    assert p.returncode == 0
