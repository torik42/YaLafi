
import sys

def test_1(capsys):
    capsys.readouterr()
    s = 'XXX'
    sys.stderr.write(s)
    sys.stderr.flush()
    captured = capsys.readouterr()
    assert captured.err == s

def test_2(capsys):
    capsys.readouterr()
    s = 'XXX'
    try:
        sys.stderr.write(s)
        sys.stderr.flush()
        sys.exit()
    except SystemExit:
        pass
    captured = capsys.readouterr()
    assert captured.err == s

