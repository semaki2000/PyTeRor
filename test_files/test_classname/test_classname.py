"""Tests that tests in a class with a wrong name per pytest test discovery is not parametrized
Tests in TestClassA should parametrize. 
Tests in FestClassB should not.
Tests in global scope should."""

#class scope

class TestClassA:
    def test_a():
        return True

    def test_b():
        return False

#another class scope
    
class FestClassB:
    def test_a():
        return True

    def test_b():
        return False
    
#global scope

def test_a():
    return True

def test_b():
    return False