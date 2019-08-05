# --- Standard Library Imports ------------------------------------------------
from pathlib import Path
from typing import List

# --- Third Party Imports -----------------------------------------------------
import pytest

# --- Intra-Package Imports ---------------------------------------------------
import rtm.containers.worksheet_columns as wc
from rtm.validation.validation import example_results
from rtm.validation.validator_output import ValidationResult


@pytest.fixture(scope="session")
def worksheet_columns() -> List[wc.WorksheetColumn]:
    headers = [
        "ID",
        "Devices",
        "Requirement Statement",
        "Requirement Rationale",
        "Cascade Level",
        "Verification or Validation Strategy",
        "Verification or Validation Results",
        "Design Output Feature (with CTQ ID #)",
        "CTQ? Yes, No, N/A",
    ]
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
def rtm_path() -> Path:
    return Path(__file__).parent / "test_rtm.xlsx"


@pytest.fixture(scope="session")
def example_val_results() -> List[ValidationResult]:
    return example_results()


@pytest.fixture(scope="session")
def ws_cols_from_test_validation(rtm_path):
    return wc.get_worksheet_columns(rtm_path, worksheet_name='test_validation')

# @pytest.fixture(scope="session")
# def
