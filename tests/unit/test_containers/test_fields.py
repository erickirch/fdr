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

# @pytest.mark.parametrize("field_class", Fields.get_field_classes())
# @pytest.mark.parametrize("dups_count", [1, 2])
# def test_init_with_good_data(dummy_worksheet_columns, field_class, dups_count):
#     """Field should successfully initialize with two matching column"""
#     worksheet_columns = dummy_worksheet_columns * dups_count
#     with context.worksheet_columns.set(worksheet_columns):
#         field = field_class()
#         assert field.field_found()
#         if issubclass(field_class, fb.SingleColumnField):
#             assert len(field._indices) == dups_count


@pytest.mark.parametrize("field_class", Fields.get_field_classes())
def test_init_without_matching_col(worksheet_columns, field_class):
    """Field should initialize to 'not found'"""
    name = field_class.get_name()
    ws_cols = [ws_col for ws_col in worksheet_columns if ws_col.header.lower() != name.lower()]
    field = field_class(ws_cols)
    assert not field.field_found()
    assert field._indices is None
    assert len(worksheet_columns) - len(ws_cols) == 1
