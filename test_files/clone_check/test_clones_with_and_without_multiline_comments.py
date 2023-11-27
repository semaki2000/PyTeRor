def test1():
    """Comment for this test"""
    return 1+2+3

def test2():
    return 4+5+6

def test3():
    return 1+2+3
    """Comment for this test"""


"""Problem:
Nicad marks test1 and test2 as clones. It ignores multiline strings that are the first statement in a function body.
This means that we have to do this as well."""