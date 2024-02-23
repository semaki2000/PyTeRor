"""This program gives errors, as a and b are locally defined...
But not in our list of node differences...

"""


def test_a():
    a = 1
    b = 2
    a + a
    b + b

def test_b():
    a = 1
    b = 2
    b + b
    a + a
    
def test_c():
    a = 1
    b = 2
    a + b
    b + a