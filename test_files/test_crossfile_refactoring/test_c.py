"""These are purposefully different. Should not contain clones"""

def test_c():
    assert 2 == 2 * 1

def test_inconsistency():
    a = 2
    b = 3
    c = 4
    assert a == a == a == a == a