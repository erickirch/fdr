# --- Standard Library Imports ------------------------------------------------
from pathlib import Path
from typing import List

# --- Third Party Imports -----------------------------------------------------
import pytest

# --- Intra-Package Imports ---------------------------------------------------
import rtm.containers.worksheet_columns as wc
from rtm.validate.validator_output import ValidationResult


@pytest.fixture(scope="session")
def dummy_worksheet_columns() -> List[wc.WorksheetColumn]:
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
def ws_cols_from_test_xlsx(rtm_path) -> List[wc.WorksheetColumn]:
    return wc.read_worksheet_columns(rtm_path, "Procedure Based Requirements")


@pytest.fixture(scope="session")
def rtm_path() -> Path:
    return Path(__file__).parent / "test_rtm.xlsx"


@pytest.fixture(scope="session")
def example_val_results() -> List[ValidationResult]:
    return example_results()


@pytest.fixture(scope="session")
def ws_cols_from_test_validation(rtm_path):
    return wc.read_worksheet_columns(rtm_path, worksheet_name='test_validation')

# @pytest.fixture(scope="session")
# def




def example_results() -> List[ValidationResult]:
    explanation = 'This is an example explanation'
    examples = [
        ValidationResult('Pass', 'Pass Example', explanation),
        ValidationResult('Warning', 'Warning Example', explanation),
        ValidationResult('Error', 'Error Example', explanation),
    ]
    return examples
