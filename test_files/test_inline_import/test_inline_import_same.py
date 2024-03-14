    

def test_a():
    from docs_src.dependency_testing.tutorial001_an_py310 import (
        test_override_in_items_with_q,
    )
    a = 1
    test_override_in_items_with_q()


def test_b():
    from docs_src.dependency_testing.tutorial001_an_py310 import (
        test_override_in_items_with_q,
    )
    a = 2
    test_override_in_items_with_q()