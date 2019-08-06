"""
Whereas the validation functions return results that will be outputted by the RTM Validator,
these "check" functions perform smaller tasks, like checking individual cells.
"""


def cell_empty(value) -> bool:
    if isinstance(value, bool):
        return False
    if not value:
        return True
    return False
