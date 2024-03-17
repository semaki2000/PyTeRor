import pytest

@pytest.mark.parametrize(
    "parametrized_name_1, command, parametrized_name_0",
    [
        pytest.param(
            ["blame", "phase", "rebase"],
            Command(
                "hg base",
                """hg: unknown command 'base'
(did you mean one of blame, phase, rebase?)""",
            ),
            extract_possibilities,
            id="test_extract_possibilities",
        ),
        pytest.param(
            ["branch", "branches"],
            Command(
                "hg branchch",
                """hg: unknown command 'branchch'
(did you mean one of branch, branches?)""",
            ),
            extract_possibilities,
            id="test_extract_possibilities",
        ),
        pytest.param(
            ["revert"],
            Command(
                "hg vert",
                """hg: unknown command 'vert'
(did you mean one of revert?)""",
            ),
            extract_possibilities,
            id="test_extract_possibilities",
        ),
        pytest.param(
            ["log"],
            Command(
                "hg lgo -r tip",
                """hg: command 're' is ambiguous:
(did you mean one of log?)""",
            ),
            extract_possibilities,
            id="test_extract_possibilities",
        ),
        pytest.param(
            ["revert"],
            Command(
                "hg rerere",
                """hg: unknown command 'rerere'
(did you mean one of revert?)""",
            ),
            extract_possibilities,
            id="test_extract_possibilities",
        ),
        pytest.param(
            ["rebase", "recover", "remove", "rename", "resolve", "revert"],
            Command(
                "hg re",
                """hg: command 're' is ambiguous:
    rebase recover remove rename resolve revert""",
            ),
            extract_possibilities,
            id="test_extract_possibilities",
        ),
        pytest.param(
            ["rebase", "recover", "remove", "rename", "resolve", "revert"],
            Command(
                "hg re re",
                """hg: command 're' is ambiguous:
    rebase recover remove rename resolve revert""",
            ),
            extract_possibilities,
            id="test_extract_possibilities",
        ),
        pytest.param(
            "hg rebase",
            Command(
                "hg base",
                """hg: unknown command 'base'
(did you mean one of blame, phase, rebase?)""",
            ),
            get_new_command,
            id="test_get_new_command",
        ),
        pytest.param(
            "hg branch",
            Command(
                "hg branchch",
                """hg: unknown command 'branchch'
(did you mean one of branch, branches?)""",
            ),
            get_new_command,
            id="test_get_new_command",
        ),
        pytest.param(
            "hg revert",
            Command(
                "hg vert",
                """hg: unknown command 'vert'
(did you mean one of revert?)""",
            ),
            get_new_command,
            id="test_get_new_command",
        ),
        pytest.param(
            "hg log -r tip",
            Command(
                "hg lgo -r tip",
                """hg: command 're' is ambiguous:
(did you mean one of log?)""",
            ),
            get_new_command,
            id="test_get_new_command",
        ),
        pytest.param(
            "hg revert",
            Command(
                "hg rerere",
                """hg: unknown command 'rerere'
(did you mean one of revert?)""",
            ),
            get_new_command,
            id="test_get_new_command",
        ),
        pytest.param(
            "hg rebase",
            Command(
                "hg re",
                """hg: command 're' is ambiguous:
    rebase recover remove rename resolve revert""",
            ),
            get_new_command,
            id="test_get_new_command",
        ),
        pytest.param(
            "hg rebase re",
            Command(
                "hg re re",
                """hg: command 're' is ambiguous:
    rebase recover remove rename resolve revert""",
            ),
            get_new_command,
            id="test_get_new_command",
        ),
    ],
)
def test_extract_possibilities_parametrized(parametrized_name_0, parametrized_name_1, command):
    assert parametrized_name_0(command) == parametrized_name_1


