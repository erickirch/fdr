# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
import pytest

# --- Intra-Package Imports ---------------------------------------------------
import rtm.main.context_managers as context
import rtm.containers.field_templates as fb
from rtm.containers.fields import Fields


def test_init_fields_list(dummy_worksheet_columns):
    """Test internals of Fields class constructor"""
    field_classes = Fields.get_field_classes()
    with context.worksheet_columns.set(dummy_worksheet_columns):
        fields = [field_class() for field_class in field_classes]
        fields_found = [field for field in fields if field.field_found()]
        assert len(fields_found) == len(fields)


def test_init_fields_class(dummy_worksheet_columns):
    """Test constructor of Fields class"""
    with context.worksheet_columns.set(dummy_worksheet_columns):
        fields = Fields()
        fields_found = [field for field in fields if field.field_found()]
        assert len(fields_found) == len(fields)


def test_fields_reverse(dummy_worksheet_columns):
    with context.worksheet_columns.set(dummy_worksheet_columns):
        fields = Fields()
        fields_reverse = list(reversed(fields))
        assert fields[0] == fields_reverse[-1]
        assert len(fields) == len(fields_reverse)


def test_fields_not_found(fields_not_found):
    """Fields should all initialize to 'not found'"""
    result_actual = [field.field_found() for field in fields_not_found]
    result_expected = [False] * len(fields_not_found)
    assert result_actual == result_expected
