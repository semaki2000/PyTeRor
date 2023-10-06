
def test_with_confirmation(proc, TIMEOUT):
    a = 53
    with_confirmation(proc, TIMEOUT)

def test_select_command_with_arrows(proc, TIMEOUT):
    a = 53
    select_command_with_arrows(proc, TIMEOUT)

@pytest.mark.parametrize('b', [100, 200])
def test_refuse_with_confirmation(proc, TIMEOUT):
    b = 53
    refuse_with_confirmation(proc, TIMEOUT)

@pytest.mark.parametrize('proc, TIMEOUT', [("a", 1), ("b", 2)])
def test_without_confirmation(proc, TIMEOUT):
    a = 53
    without_confirmation(proc, TIMEOUT)