import pytest

from thefuck.rules.git_branch_0flag import get_new_command, match
from thefuck.types import Command


@pytest.fixture
def output_branch_exists():
    return "fatal: A branch named 'bar' already exists."


@pytest.mark.parametrize(
    "script",
    [
        "git branch 0a",
        "git branch 0d",
        "git branch 0f",
        "git branch 0r",
        "git branch 0v",
        "git branch 0d foo",
        "git branch 0D foo",
    ],
)
def test_match(script, output_branch_exists):
    assert match(Command(script, output_branch_exists))


@pytest.mark.parametrize(
    "script",
    [
        "git branch -a",
        "git branch -r",
        "git branch -v",
        "git branch -d foo",
        "git branch -D foo",
    ],
)
def test_not_match(script, output_branch_exists):
    assert not match(Command(script, ""))


@pytest.mark.parametrize(
    "script, new_command, parametrized_name_0",
    [
        pytest.param(
            "git branch 0a",
            "git branch -D 0a && git branch -a",
            output_branch_exists,
            id="test_get_new_command_branch_exists",
        ),
        pytest.param(
            "git branch 0v",
            "git branch -D 0v && git branch -v",
            output_branch_exists,
            id="test_get_new_command_branch_exists",
        ),
        pytest.param(
            "git branch 0d foo",
            "git branch -D 0d && git branch -d foo",
            output_branch_exists,
            id="test_get_new_command_branch_exists",
        ),
        pytest.param(
            "git branch 0D foo",
            "git branch -D 0D && git branch -D foo",
            output_branch_exists,
            id="test_get_new_command_branch_exists",
        ),
        pytest.param(
            "git branch 0l 'maint-*'",
            "git branch -D 0l && git branch -l 'maint-*'",
            output_branch_exists,
            id="test_get_new_command_branch_exists",
        ),
        pytest.param(
            "git branch 0u upstream",
            "git branch -D 0u && git branch -u upstream",
            output_branch_exists,
            id="test_get_new_command_branch_exists",
        ),
        pytest.param(
            "git branch 0l 'maint-*'",
            "git branch -l 'maint-*'",
            output_not_valid_object,
            id="test_get_new_command_not_valid_object",
        ),
        pytest.param(
            "git branch 0u upstream",
            "git branch -u upstream",
            output_not_valid_object,
            id="test_get_new_command_not_valid_object",
        ),
    ],
)
def test_get_new_command_branch_exists_parametrized(script, new_command, parametrized_name_0):
    assert get_new_command(Command(script, parametrized_name_0)) == new_command


@pytest.fixture
def output_not_valid_object():
    return "fatal: Not a valid object name: 'bar'."


