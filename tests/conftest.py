# --- Standard Library Imports ------------------------------------------------
from pathlib import Path
from typing import List

# --- Third Party Imports -----------------------------------------------------
import pytest

# --- Intra-Package Imports ---------------------------------------------------
import rtm.containers.worksheet_columns as wc
from rtm.validate.validator_output import ValidationResult
from rtm.containers.fields import Fields
import rtm.main.context_managers as context


# --- Worksheet Path ----------------------------------------------------------

@pytest.fixture(scope="session")
def rtm_path() -> Path:
    return Path(__file__).parent / "test_rtm.xlsx"


# --- Generate Worksheet Columns ----------------------------------------------

def get_dummy_worksheet_headers(reverse=False):
    headers = [
        "ID",
        # "Procedure Step",
        # "User Need",
        # "Design Input",
        # "DO Solution L1",
        # "DO Solution L2",
        # "DO Solution L3",
        # "Cascade Level",
        # "Requirement Statement",
        # "Requirement Rationale",
        # "Verification or Validation Strategy",
        # "Verification or Validation Results",
        # "Design Output Feature (with CTQ ID #)",
        "CTQ? Yes, No, N/A",
        "Devices",
    ]
    if reverse:
        headers = list(reversed(headers))
    ws_cols = []
    for index, header in enumerate(headers):
        col = index + 1
        ws_col = wc.WorksheetColumn(
            header=header,
            body=[1, 2, 3],
            index=index,
            column=col,
        )
        ws_cols.append(ws_col)
    return ws_cols


@pytest.fixture(scope="session")
def dummy_worksheet_columns() -> List[wc.WorksheetColumn]:
    return get_dummy_worksheet_headers()


@pytest.fixture(scope="session")
def dummy_worksheet_columns_reverse():
    return get_dummy_worksheet_headers(reverse=True)


@pytest.fixture(scope="session")
def ws_cols_from_test_xlsx(rtm_path) -> List[wc.WorksheetColumn]:
    return wc.read_worksheet_columns(rtm_path, "Procedure Based Requirements")


@pytest.fixture(scope="session")
def ws_cols_from_test_validation(rtm_path):
    return wc.read_worksheet_columns(rtm_path, worksheet_name='test_validation')


# --- Fields ------------------------------------------------------------------

@pytest.fixture(scope="function")
def initialized_fields_simple(dummy_worksheet_columns):
    with context.worksheet_columns.set(dummy_worksheet_columns):
        fields = Fields()
    return fields

# TODO fixture that generates list of fields
#