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
# import tests.conftest as conftest


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

    @abc.abstractmethod
    def get_index(self):
        return

    @abc.abstractmethod
    def get_min_index_for_field_right(self):
        return

    @abc.abstractmethod
    def get_previous_field(self):
        return

    @abc.abstractmethod
    def get_name(self):
        return



class SingleColumnField(Field):

    def __init__(self):

        # --- Get matching columns --------------------------------------------
        matching_worksheet_columns = get_matching_worksheet_columns(
            cm.worksheet_columns(),
            self.get_name()
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
            validator_output.OutputHeader(self.get_name()),  # Start with header
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

    def get_index(self):
        return self._indices[0]

    def validate_position(self):
        """Check that this field comes after the previous one. Return this column number."""
        if not self.field_found():
            return previous_index
        if self.get_index() > previous_index:
            self._correct_position = True
        else:
            self._correct_position = False
        return self.get_index()

    def get_body(self):
        return self._body

    def get_name(self):
        return self._name

    def get_min_index_for_field_right(self):
        return self.get_index()


if __name__ == "__main__":
    pass
