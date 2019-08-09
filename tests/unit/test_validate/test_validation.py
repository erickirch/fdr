"""
Unit tests for validation.py functions
"""
# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
import pytest

# --- Intra-Package Imports ---------------------------------------------------
import rtm.containers.worksheet_columns as wc
import rtm.validate.validation as val
import rtm.main.context_managers as context


def test_column_exist(capsys):
    io = [
        (True, f'\tPass\tFIELD EXIST\n'),
        (False, f'\tError\tFIELD EXIST - Field not found\n')
    ]
    for item in io:
        result = val.val_column_exist(item[0])
        result.print()
        captured = capsys.readouterr()
        assert captured.out == item[1]


# TODO parameterize inputs:
#   Two lists of fields (context manager)
#       1) fields in correct order (all pass)
#       2) fields in opposite order (all fail except for the first)
#   field to be searched for
#   each field must be initialized.
def test_column_sort(initialized_fields_simple):
    print('hello')
    testing = initialized_fields_simple[0]
    print(initialized_fields_simple)
    print('bye')
    with context.fields.set(initialized_fields_simple):
        scores_actual = [
            val.val_column_sort(field)._score
            for field
            in initialized_fields_simple
        ]
    scores_should = ['Pass']*3#len(scores_actual)
    assert scores_actual == scores_should


# def test_column_sort_reverse(initialized_fields_simple):
#     reversed_fields = reversed(initialized_fields_simple)
#     with context.fields.set(reversed_fields):
#         scores_actual = [
#             val.val_column_sort(field)._score
#             for field
#             in initialized_fields_simple
#         ]
#     scores_should = ['Pass'] + ['Error']*(len(scores_actual) - 1)
#     assert scores_actual == scores_should


def test_cells_not_empty():
    pass


@pytest.mark.parametrize('val_func', val.cell_validation_functions)
def test_cell_functions(ws_cols_from_test_validation, val_func):
    # ws_cols = ws_cols_from_test_validation
    # header = val_cells_not_empty.__name__
    # try:
    #     ws_col: WorksheetColumn = get_first_matching_worksheet_column(ws_cols, header)
    # except IndexError:
    #     raise IndexError(f"The test_validation ws is likely missing a '{header}' column")
    # cells_to_be_tested = ws_col.body
    # val_result = val_cells_not_empty(cells_to_be_tested)
    # failed_indices = tuple(val_result.indices)
    # assert failed_indices == tuple(range(5))
    ws_cols = ws_cols_from_test_validation
    header = val_func.__name__
    try:
        ws_col: wc.WorksheetColumn = wc.get_first_matching_worksheet_column(ws_cols, header)
    except IndexError:
        # raise IndexError(f"The test_validation ws is likely missing a '{header}' column")
        assert False
    else:
        cells_to_be_tested = ws_col.body
        val_result = val_func(cells_to_be_tested)
        failed_indices = tuple(val_result.indices)
        assert failed_indices == tuple(range(5))


if __name__ == "__main__":
    pass
