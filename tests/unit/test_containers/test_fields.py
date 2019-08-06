# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
import pytest

# --- Intra-Package Imports ---------------------------------------------------
import rtm.main.context_managers as cm
import rtm.containers.field_templates as fb
from rtm.containers.fields import Fields


@pytest.mark.parametrize("field_class", Fields.get_field_classes())
@pytest.mark.parametrize("dups_count", [1, 2])
def test_init_with_good_data(dummy_worksheet_columns, field_class, dups_count):
    """Field should successfully initialize with two matching column"""
    worksheet_columns = dummy_worksheet_columns * dups_count
    with cm.worksheet_columns.set(worksheet_columns):
        field = field_class()
        assert field.field_found()
        if issubclass(field_class, fb.SingleColumnField):
            assert len(field._indices) == dups_count


@pytest.mark.parametrize("field_class", Fields.get_field_classes())
def test_init_without_matching_col(worksheet_columns, field_class):
    """Field should initialize to 'not found'"""
    name = field_class.get_field_name()
    ws_cols = [ws_col for ws_col in worksheet_columns if ws_col.header.lower() != name.lower()]
    field = field_class(ws_cols)
    assert not field.field_found()
    assert field._indices is None
    assert len(worksheet_columns) - len(ws_cols) == 1
