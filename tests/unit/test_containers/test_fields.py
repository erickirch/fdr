# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
import pytest

# --- Intra-Package Imports ---------------------------------------------------
import rtm.main.context_managers as cm
import rtm.containers.field_base as fb
from rtm.main.exceptions import RTMValidatorError
from rtm.containers.fields import fields


@pytest.mark.parametrize("field_class", fields.get_field_classes())
@pytest.mark.parametrize("dups_count", [1, 2])
def test_init_with_good_data(dummy_worksheet_columns, field_class, dups_count):
    """Field should successfully initialize with two matching column"""
    worksheet_columns = dummy_worksheet_columns * dups_count
    with cm.worksheet_columns.set(worksheet_columns):
        field = field_class()
        assert field.field_found()
        if issubclass(field_class, fb.SingleColumnField):
            assert len(field._indices) == dups_count


@pytest.mark.parametrize("field_class", fields)
def test_init_without_matching_col(worksheet_columns, field_class):
    """Field should initialize to 'not found'"""
    name = field_class.get_field_name()
    ws_cols = [ws_col for ws_col in worksheet_columns if ws_col.header.lower() != name.lower()]
    field = field_class(ws_cols)
    assert not field.field_found()
    assert field._indices is None
    assert len(worksheet_columns) - len(ws_cols) == 1


@pytest.mark.parametrize("field_class", fields)
@pytest.mark.parametrize("not_worksheet_column", ['c', 1, ('a', 'b')])
def test_init_with_incorrect_data(not_worksheet_column, field_class):
    """Field and its subclasses should throw a builtin exception if
    passed something other than a sequence of WorksheetColumns"""
    error_occurred = False
    try:
        field = field_class(not_worksheet_column)
    except RTMValidatorError:
        # This shouldn't happen
        pass
    except:
        # A non-RTMValidatorError should occur
        error_occurred = True
    assert error_occurred
