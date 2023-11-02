import os
from textwrap import dedent
import pytest
from ert.config.parsing import ConfigValidationError, init_user_config_schema, lark_parse

@pytest.mark.parametrize('parametrized_constant_0, parametrized_constant_1', [("""
        NUM_REALIZATIONS  1
        QUEUE_OPTION VOCAL MAX_RUNNING 50
        """, 'VOCAL'), ("""
        NUM_REALIZATIONS  1
        ENKF_ALPHA
        """, 'at least 1 arguments'), ("""
        NUM_REALIZATIONS  1
        JOB_SCRIPT  hello
        """, 'executable'), ("""
        NUM_REALIZATIONS  hello
        """, 'integer'), ("""
        NUM_REALIZATIONS  1
        ENKF_ALPHA 1.0 2.0 3.0
        """, 'maximum 1 arguments'), ("""
        NUM_REALIZATIONS  1
        STOP_LONG_RUNNING NOT_YES
        """, 'boolean'), ("""
        NUM_REALIZATIONS  1
        ENKF_ALPHA  hello
        """, 'number')])
@pytest.mark.usefixtures('use_tmpdir')
def test_that_giving_incorrect_queue_name_in_queue_option_fails_parametrized(parametrized_constant_0, parametrized_constant_1):
    test_config_file_name = 'test.ert'
    test_config_contents = dedent(parametrized_constant_0)
    with open(test_config_file_name, 'w', encoding='utf-8') as fh:
        fh.write(test_config_contents)
    with pytest.raises(ConfigValidationError, match=parametrized_constant_1):
        _ = lark_parse(test_config_file_name, schema=init_user_config_schema())