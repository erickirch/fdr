"""
These functions each check a specific aspect of an RTM field and return a ValidationResult object,
ready to be printed on the terminal as the final output of this app.
"""

# --- Standard Library Imports ------------------------------------------------
from typing import List

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
import rtm.validate.checks as check
from rtm.validate.validator_output import ValidationResult


def val_column_exist(field_found) -> ValidationResult:
    title = "Field Exist"
    if field_found:
        score = 'Pass'
        explanation = None
    else:
        score = 'Error'
        explanation = 'Field not found'
    return ValidationResult(score, title, explanation)


def val_column_sort(field) -> ValidationResult:
    """Does the argument field actually appear after the one it's supposed to?"""
    title = "Left/Right Order"

    field_left = check.get_expected_field_left(field)
    if field_left is None:
        # argument field is supposed to be all the way to the left. It's always in the correct position.
        score = 'Pass'
        explanation = 'This field appears to the left of all the others'
    elif field_left.get_min_index_for_field_right() <= field.get_index():
        # argument field is to the right of its expected left-hand neighbor
        score = 'Pass'
        explanation = f'This field comes after the {field_left.get_name()} field as it should'
    else:
        score = 'Error'
        explanation = f'This field should come after {field_left.get_name()}'
    return ValidationResult(score, title, explanation)


def val_cells_not_empty(values) -> ValidationResult:
    title = "Not Empty"
    indices = []
    for index, value in enumerate(values):
        if check.cell_empty(value):
            indices.append(index)
    if not indices:
        score = 'Pass'
        explanation = 'All cells are non-blank'
    else:
        score = 'Error'
        explanation = 'Action Required. The following rows are blank:'
    return ValidationResult(score, title, explanation, indices)


def val_cascade_block_only_one_entry(work_items):
    title = "Single Entry"
    indices = []
    for work_item in work_items:
        _len = len(work_item.cascade_block_contents)
        if _len != 1:
            indices.append(work_item.index)
    if not indices:
        score = 'Pass'
        explanation = 'All rows have a single entry'
    else:
        score = 'Error'
        explanation = 'Action Required. The following rows are blank or have multiple entries:'
    return ValidationResult(score, title, explanation, indices)


def val_cascade_block_x_or_f(work_items) -> ValidationResult:
    title = "X or F"
    indices = []
    acceptable_entries = ['X', 'F']
    for work_item in work_items:
        if work_item.cascade_block_contents[0] not in acceptable_entries:
            indices.append(work_item.index)
    if not indices:
        score = 'Pass'
        explanation = f'All entries are one of {acceptable_entries}'
    else:
        score = 'Error'
        explanation = f'Action Required. The following rows contain something other than the allowed {acceptable_entries}:'
    return ValidationResult(score, title, explanation, indices)


def val_cascade_block_use_all_columns(work_items, subfield_count: int) -> ValidationResult:
    title = "Use All Columns"
    indices = []
    max_position = max(work_item.position for work_item in work_items)
    if max_position + 1 == subfield_count:
        score = 'Pass'
        explanation = f'All cascade levels were used.'
    elif max_position >= subfield_count:
        raise IndexError("Cascade level mismatch")
    else:
        score = 'Warning'
        unused_levels = subfield_count-max_position-1
        explanation = f'The last {unused_levels} cascade levels are unused.'
    return ValidationResult(score, title, explanation)


def get_row(index):
    return index + 2


# TODO: replace with something more maintainable / straightforward
cell_validation_functions = [globals()[name] for name in globals() if name.startswith('val_cells_')]


if __name__ == "__main__":
    print(cell_validation_functions)
