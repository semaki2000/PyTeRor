"""This program gives errors, as a and b are locally defined...
But not in our list of node differences...

"""


def test_a():
    a1 = 1
    b = 2
    a1 + a1
    b + b

def test_b():
    a2 = 1
    b = 2
    a2 + a2
    b + b
    
def test_c():
    a3 = 1
    b = 2
    a3 + a3
    b + a3