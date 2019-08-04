# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
import rtm.worksheet_columns as wc
from rtm.fields.field import Field
from rtm.fields.fields import field_classes as fc
from rtm.rtm_worksheet import RTMWorksheet


def test_initialize_fields(worksheet_columns):
    fields = RTMWorksheet._initialize_fields(
        field_classes=fc, worksheet_columns=worksheet_columns
    )
    for field in fields:
        assert field.field_found


def test_get_worksheet(rtm_path):
    worksheet_columns = wc.get_worksheet_columns(
        path=rtm_path, worksheet_name="test_worksheet"
    )
    for ws_col in worksheet_columns:
        assert isinstance(ws_col, wc.WorksheetColumn)


def test_init_rtm_worksheet(rtm_path):
    rtm_worksheet = RTMWorksheet(rtm_path)
    for field in rtm_worksheet.fields:
        assert isinstance(field, Field)


if __name__ == "__main__":
    # test_import_worksheet()
    pass
