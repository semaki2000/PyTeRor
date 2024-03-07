

def test_b():
    assert 2

def test_inconsistent_b():
    """This one should not be parametrized between files.
    Should not even be detected as clone, with -cf option enabled
    (Is detected as clone without -cf option, then disregarded as clone class between files)"""
    a = 2
    b = 3
    assert a == a