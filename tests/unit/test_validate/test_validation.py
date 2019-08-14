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


@pytest.mark.parametrize('reverse', [False, True])
def test_column_sort(initialized_fields_simple, reverse):

    if not reverse:
        fields = initialized_fields_simple
        scores_should = ['Pass'] * len(fields)
    else:
        fields = list(reversed(initialized_fields_simple))
        scores_should = ['Pass'] + ['Error'] * (len(fields) - 1)

    with context.fields.set(fields):
        scores_actual = [
            val.val_column_sort(field)._score
            for field
            in fields
        ]

    assert len(scores_actual) > 0
    assert scores_actual == scores_should


@pytest.mark.skip("not yet implemented")
def test_cells_not_empty():
    pass


def test_val_startswithp():
    pass
    #passlist = ['P0000']
    #testout = val.val_starts_with_p(passlist)
    #assert testout =

if __name__ == "__main__":
    pass
