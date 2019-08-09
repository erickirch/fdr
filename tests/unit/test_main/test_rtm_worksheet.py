# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
import rtm.containers.worksheet_columns as wc
from rtm.containers.field_templates import Field
from rtm.main.rtm_worksheet import RTMWorksheet
import rtm.main.context_managers as context


def test_get_worksheet(rtm_path):
    with context.path.set(rtm_path):
        worksheet_columns = wc.read_worksheet_columns("test_worksheet")
    for ws_col in worksheet_columns:
        assert isinstance(ws_col, wc.WorksheetColumn)


if __name__ == "__main__":
    pass
