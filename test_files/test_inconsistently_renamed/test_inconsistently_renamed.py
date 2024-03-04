"""This program gives errors, as a and b are locally defined...
But not in our list of node differences...

"""


def test_a():
    a, b = 1, 2
    a + a

def test_mixed():
    a, b = 1, 2
    a + b
    
def test_b():
    a, b = 1, 2
    b + b

    