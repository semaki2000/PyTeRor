import os
from textwrap import dedent

import pytest

from ert.config.parsing import (
    ConfigValidationError,
    init_user_config_schema,
    lark_parse,
)
@pytest.mark.test
@pytest.mark.usefixtures("use_tmpdir")
def test_that_giving_incorrect_queue_name_in_queue_option_fails():
    test_config_file_name = "test.ert"
    test_config_contents = dedent(
        """
        NUM_REALIZATIONS  1
        QUEUE_OPTION VOCAL MAX_RUNNING 50
        """
    )
    with open(test_config_file_name, "w", encoding="utf-8") as fh:
        fh.write(test_config_contents)

    with pytest.raises(ConfigValidationError, match="VOCAL"):
        _ = lark_parse(test_config_file_name, schema=init_user_config_schema())



@pytest.mark.usefixtures("use_tmpdir")
def test_that_invalid_boolean_values_are_handled_gracefully():
    test_config_file_name = "test.ert"
    test_config_contents = dedent(
        """
        NUM_REALIZATIONS  1
        STOP_LONG_RUNNING NOT_YES
        """
    )
    with open(test_config_file_name, "w", encoding="utf-8") as fh:
        fh.write(test_config_contents)

    with pytest.raises(ConfigValidationError, match="boolean"):
        _ = lark_parse(test_config_file_name, schema=init_user_config_schema())



@pytest.mark.usefixtures("use_tmpdir")
def test_that_giving_non_int_values_give_config_validation_error():
    test_config_file_name = "test.ert"
    test_config_contents = dedent(
        """
        NUM_REALIZATIONS  hello
        """
    )
    with open(test_config_file_name, "w", encoding="utf-8") as fh:
        fh.write(test_config_contents)

    with pytest.raises(ConfigValidationError, match="integer"):
        _ = lark_parse(test_config_file_name, schema=init_user_config_schema())


@pytest.mark.usefixtures("use_tmpdir")
def test_that_giving_non_float_values_give_config_validation_error():
    test_config_file_name = "test.ert"
    test_config_contents = dedent(
        """
        NUM_REALIZATIONS  1
        ENKF_ALPHA  hello
        """
    )
    with open(test_config_file_name, "w", encoding="utf-8") as fh:
        fh.write(test_config_contents)

    with pytest.raises(ConfigValidationError, match="number"):
        _ = lark_parse(test_config_file_name, schema=init_user_config_schema())


@pytest.mark.usefixtures("use_tmpdir")
def test_that_giving_non_executable_gives_config_validation_error():
    test_config_file_name = "test.ert"
    test_config_contents = dedent(
        """
        NUM_REALIZATIONS  1
        JOB_SCRIPT  hello
        """
    )
    with open(test_config_file_name, "w", encoding="utf-8") as fh:
        fh.write(test_config_contents)

    with pytest.raises(ConfigValidationError, match="executable"):
        _ = lark_parse(test_config_file_name, schema=init_user_config_schema())


@pytest.mark.usefixtures("use_tmpdir")
def test_that_giving_too_many_arguments_gives_config_validation_error():
    test_config_file_name = "test.ert"
    test_config_contents = dedent(
        """
        NUM_REALIZATIONS  1
        ENKF_ALPHA 1.0 2.0 3.0
        """
    )
    with open(test_config_file_name, "w", encoding="utf-8") as fh:
        fh.write(test_config_contents)

    with pytest.raises(ConfigValidationError, match="maximum 1 arguments"):
        _ = lark_parse(test_config_file_name, schema=init_user_config_schema())


@pytest.mark.usefixtures("use_tmpdir")
def test_that_giving_too_few_arguments_gives_config_validation_error():
    test_config_file_name = "test.ert"
    test_config_contents = dedent(
        """
        NUM_REALIZATIONS  1
        ENKF_ALPHA
        """
    )
    with open(test_config_file_name, "w", encoding="utf-8") as fh:
        fh.write(test_config_contents)

    with pytest.raises(ConfigValidationError, match="at least 1 arguments"):
        _ = lark_parse(test_config_file_name, schema=init_user_config_schema())
