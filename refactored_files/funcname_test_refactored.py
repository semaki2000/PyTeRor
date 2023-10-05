@pytest.mark.parametrize('new_var_0', [('with_confirmation',), ('select_command_with_arrows',), ('refuse_with_confirmation',), ('without_confirmation',)])
def test_with_confirmation(new_var_0, proc, TIMEOUT):
    eval('new_var_0')(proc, TIMEOUT)