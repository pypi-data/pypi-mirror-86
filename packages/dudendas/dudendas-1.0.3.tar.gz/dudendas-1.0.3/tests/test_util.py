from dudendas.util import *


def test_textify():
    assert textify(" foo  bar (3a) ") == "foo bar"
