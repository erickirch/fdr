# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
import pytest

# --- Intra-Package Imports ---------------------------------------------------
import rtm.containers.worksheet_columns as wc
import rtm.validate.validation as val


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


def test_column_sort(capsys):
    result = val.val_column_sort(True, 'Butter Panzer')
    result.print()
    captured = capsys.readouterr()
    assert captured.out == f'\tPass\tFIELD ORDER - This field comes after the Butter Panzer field as it should\n'


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
