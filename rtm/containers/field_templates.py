# --- Standard Library Imports ------------------------------------------------
import abc
from typing import List

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
import rtm.main.context_managers as cm
import rtm.validate.validation as val
from rtm.containers.worksheet_columns import get_matching_worksheet_columns
from rtm.main.exceptions import UninitializedError
from rtm.validate import validator_output
import tests.conftest as conftest


class Field(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def validate(self):
        return

    @abc.abstractmethod
    def print(self):
        return

    @abc.abstractmethod
    def get_body(self):
        """Return all values from this field (exclude the header)"""
        return

    @abc.abstractmethod
    def field_found(self):
        return


def add_previous_field_finder(field_class):

    def get_previous_field(self):
        fields = cm.fields()
        index_prev_field = None
        for index, field in enumerate(fields):
            if self is field:
                index_prev_field = field - 1
                break
        if index_prev_field is None:
            raise ValueError
        elif index_prev_field == -1:
            return None
        else:
            return fields[index_prev_field]

    setattr(field_class, get_previous_field.__name__, get_previous_field)

    return field_class


@add_previous_field_finder
class SingleColumnField(Field):

    field_name = None

    def __init__(self):

        # --- Get matching columns --------------------------------------------
        matching_worksheet_columns = get_matching_worksheet_columns(
            cm.worksheet_columns(),
            self.get_field_name()
        )

        # --- Set Defaults ----------------------------------------------------
        self._indices = None  # Used in later check of relative column position
        self._body = None  # column data
        self._correct_position = None  # Checked during the Validation step
        self._val_results = None

        # --- Override defaults if matches are found --------------------------
        if len(matching_worksheet_columns) >= 1:
            # Get all matching indices (used for checking duplicate data and proper sorting)
            self._indices = [col.index for col in matching_worksheet_columns]
            # Get first matching column data (any duplicate columns are ignored; user rcv warning)
            self._body = matching_worksheet_columns[0].body

    def validate(self) -> None:

        # --- Was the field found? --------------------------------------------
        field_found = self.field_found()

        # --- Generate the minimum output message -----------------------------
        self._val_results = [
            validator_output.OutputHeader(self.get_field_name()),  # Start with header
            val.val_column_exist(field_found),
        ]

        # --- Perform remaining validation if the field was found -------------
        if field_found:
            self._val_results.append(val.val_column_sort(self._correct_position))
            self._val_results += self._validation_specific_to_this_field()

    def _validation_specific_to_this_field(self) -> List[validator_output.ValidatorOutput]:
        return conftest.example_val_results()

    def print(self):
        for result in self._val_results:
            result.print()

    def field_found(self):
        if self._body is None:
            return False
        return True

    def _get_index(self):
        return self._indices[0]

    def validate_position(self, previous_index):
        """Check that this field comes after the previous one. Return this column number."""
        if not self.field_found():
            return previous_index
        if self._get_index() > previous_index:
            self._correct_position = True
        else:
            self._correct_position = False
        return self._get_index()

    def get_body(self):
        return self._body

    @classmethod
    def get_field_name(cls):
        if cls.field_name is None:
            raise UninitializedError("A field hasn't implemented a field name yet.")
        return cls.field_name


if __name__ == "__main__":
    pass