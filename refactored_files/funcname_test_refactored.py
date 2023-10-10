@pytest.mark.parametrize('parametrized_name_0', [with_confirmation, select_command_with_arrows, refuse_with_confirmation, without_confirmation])
def test_with_confirmation_parameterized(proc, TIMEOUT, parametrized_name_0):
    a = 53
    parametrized_name_0(proc, TIMEOUT)