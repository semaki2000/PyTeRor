
def test_none():
    a = b = 1
    return None

def test_name():
    a = b = 1
    return a


"""Nicad sees None as a name, not a literal. This means that these two are clones for nicad, 
despite one being a name in the ast, and the other being a literal."""