import os
from pathlib import Path
import pytest
import xtgeo
from ert.config import ConfigValidationError, ConfigWarning, Field
from ert.config.field import TRANSFORM_FUNCTIONS
from ert.config.parsing import init_user_config_schema, lark_parse
from ert.field_utils import Shape, read_field

@pytest.mark.parametrize('transform, parametrized_constant_0', [pytest.param('INIT_TRANSFORM', 'FIELD f PARAMETER f.roff INIT_FILES:f%d.grdecl OUTPUT_TRANSFORM:', id='test_output_transform_is_gotten_from_keyword'), pytest.param('OUTPUT_TRANSFORM', 'FIELD f PARAMETER f.roff INIT_FILES:f%d.grdecl OUTPUT_TRANSFORM:', id='test_output_transform_is_gotten_from_keyword'), pytest.param('INIT_TRANSFORM', 'FIELD f PARAMETER f.roff INIT_FILES:f%d.grdecl INIT_TRANSFORM:', id='test_init_transform_is_gotten_from_keyword'), pytest.param('OUTPUT_TRANSFORM', 'FIELD f PARAMETER f.roff INIT_FILES:f%d.grdecl INIT_TRANSFORM:', id='test_init_transform_is_gotten_from_keyword')])
def test_output_transform_is_gotten_from_keyword_parametrized(parse_field_line, transform, parametrized_constant_0):
    field = parse_field_line(f'{parametrized_constant_0}{transform}')
    assert field.output_transformation == transform

@pytest.mark.parametrize('boolean', [True, False, 'a', 'B'])
def test_forward_init_is_gotten_from_keyword(parse_field_line, boolean):
    field = parse_field_line(f'FIELD f PARAMETER f.roff INIT_FILES:f%d.grdecl FORWARD_INIT:{boolean}')
    assert field.forward_init == boolean