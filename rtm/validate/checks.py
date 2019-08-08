"""
Whereas the validation functions return results that will be outputted by the RTM Validator,
these "check" functions perform smaller tasks, like checking individual cells.
"""

# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
import rtm.main.context_managers as cm
import rtm.containers.field_templates as ft


def cell_empty(value) -> bool:
    # If the cell contained True or False, then clearly it wasn't empty. Return False
    if isinstance(value, bool):
        return False
    if not value:
        return True
    return False


def get_previous_field(field: ft.Field) -> ft.Field:
    """Return the field object that *should* come before the argument field object."""
    initialized_fields = cm.fields()
    index_prev_field = None
    for index, field_current in enumerate(initialized_fields):
        if field is field_current:
            index_prev_field = index - 1
            break
    if index_prev_field is None:
        raise ValueError
    elif index_prev_field == -1:
        return None
    else:
        return initialized_fields[index_prev_field]


def check_sort_order(self: ft.Field):
    """Does the argument field actually appear after the one it's supposed to?"""
    previous_field: ft.Field = self.get_previous_field()
    if previous_field is None:
        return True
    elif previous_field.get_min_index_for_following_field() <= self.get_index():
        return True
    else:
        return False
