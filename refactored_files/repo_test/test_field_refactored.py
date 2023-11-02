import os
from pathlib import Path
import pytest
import xtgeo
from ert.config import ConfigValidationError, ConfigWarning, Field
from ert.config.field import TRANSFORM_FUNCTIONS
from ert.config.parsing import init_user_config_schema, lark_parse
from ert.field_utils import Shape, read_field

@pytest.mark.parametrize('parametrized_constant_0, parametrized_name_0', [('FIELD f PARAMETER f.roff INIT_FILES:f%d.grdecl OUTPUT_TRANSFORM:', transform), ('INIT_TRANSFORM', transform), ('OUTPUT_TRANSFORM', transform), ('FIELD f PARAMETER f.roff INIT_FILES:f%d.grdecl INIT_TRANSFORM:', transform), ('INIT_TRANSFORM', transform), ('OUTPUT_TRANSFORM', transform), ('FIELD f PARAMETER f.roff INIT_FILES:f%d.grdecl FORWARD_INIT:', boolean), (True, boolean), (False, boolean), ('a', boolean), ('B', boolean)])
def test_output_transform_is_gotten_from_keyword_parametrized(parse_field_line, parametrized_constant_0, parametrized_name_0):
    field = parse_field_line(f'{parametrized_constant_0}{parametrized_name_0}')
    assert field.output_transformation == parametrized_name_0