import os
from pathlib import Path

import pytest
import xtgeo

from ert.config import ConfigValidationError, ConfigWarning, Field
from ert.config.field import TRANSFORM_FUNCTIONS
from ert.config.parsing import init_user_config_schema, lark_parse
from ert.field_utils import Shape, read_field

#1, STRING, transform
@pytest.mark.parametrize("transform", ["INIT_TRANSFORM", "OUTPUT_TRANSFORM"])
def test_output_transform_is_gotten_from_keyword(parse_field_line, transform):
    field = parse_field_line(
        f"FIELD f PARAMETER f.roff INIT_FILES:f%d.grdecl OUTPUT_TRANSFORM:{transform}"
    )
    assert field.output_transformation == transform

#2, STRING, transform
@pytest.mark.parametrize("transform", ["INIT_TRANSFORM", "OUTPUT_TRANSFORM"])
def test_init_transform_is_gotten_from_keyword(parse_field_line, transform):
    field = parse_field_line(
        f"FIELD f PARAMETER f.roff INIT_FILES:f%d.grdecl INIT_TRANSFORM:{transform}"
    )
    assert field.output_transformation == transform

#3, STRING, boolean
@pytest.mark.parametrize("boolean", [(True), (False), ("a"), ("B")])
def test_forward_init_is_gotten_from_keyword(parse_field_line, boolean):
    field = parse_field_line(
        f"FIELD f PARAMETER f.roff INIT_FILES:f%d.grdecl FORWARD_INIT:{boolean}"
    )
    assert field.output_transformation == boolean


