"""Test all funcs in rtm.validate.checks"""

import rtm.validate.checks as ch


def test_cell_empty():
    passes = [None, '']
    fails = [True, False, 'hello', 42]
    expected_results = [True] * len(passes) + [False] * len(fails)

    values = passes + fails
    results = [ch.cell_empty(value) for value in values]
    assert results == expected_results
