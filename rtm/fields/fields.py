# --- Standard Library Imports ------------------------------------------------
from typing import List

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
import rtm.fields.validation as val
from rtm.fields.field_base import Field
from rtm.fields.validator_output import ValidationResult


field_classes = []


def collect_field(field):
    field_classes.append(field)
    return field


@collect_field
class ID(Field):
    field_name = "ID"

    def _validate_this_field(self) -> List[ValidationResult]:
        results = [
            val.val_cells_not_empty(self._body),
        ]
        results += val.example_results()
        return results


# @collect_field; ultimately will be a collected field.
class CascadeBlock(Field):
    def __init__(self, all_worksheet_columns):

        # --- Get Matching Subfields; Stop after first Non-Found --------------
        self._subfields = []
        for subfield_name in self._get_subfield_names():
            subfield = CascadeSubfield(all_worksheet_columns, subfield_name)
            if subfield.field_found():
                self._subfields.append(subfield)
            else:
                break

        # --- Get All Matching Columns ----------------------------------------
        # --- Set Defaults ----------------------------------------------------
        # --- Override defaults if matches are found --------------------------
        pass

    @staticmethod
    def _get_subfield_names():
        field_names = ["Procedure Step", "User Need", "Design Input"]
        for i in range(1, 20):
            field_names.append("DO Solution L" + str(i))
        return field_names

    def validate_position(self, previous_index):
        """
        Check that first subfield comes after the previous one and that
        each subfield appears in order. Return column number of last subfield
        """

        # --- Check that subfields appear in order ----------------------------
        for subfield in self._subfields:
            previous_index = subfield.validate_position(previous_index)
        return previous_index


# Not a collected field; rolls up under CascadeBlock
class CascadeSubfield(Field):
    def __init__(self, all_worksheet_columns, subfield_name):
        self.subfield_name = subfield_name
        super().__init__(all_worksheet_columns)

    def get_field_name(self):
        return self.subfield_name


@collect_field
class CascadeLevel(Field):
    field_name = "Cascade Level"

    def _validate_this_field(self) -> List[ValidationResult]:
        return val.example_results()


@collect_field
class ReqStatement(Field):
    field_name = "Requirement Statement"

    def _validate_this_field(self) -> List[ValidationResult]:
        return val.example_results()


@collect_field
class ReqRationale(Field):
    field_name = "Requirement Rationale"

    def _validate_this_field(self) -> List[ValidationResult]:
        return [val.val_cells_not_empty(self._body)]


@collect_field
class VVStrategy(Field):
    field_name = "Verification or Validation Strategy"

    def _validate_this_field(self) -> List[ValidationResult]:
        return val.example_results()


@collect_field
class VVResults(Field):
    field_name = "Verification or Validation Results"

    def _validate_this_field(self) -> List[ValidationResult]:
        return []


@collect_field
class DOFeatures(Field):
    field_name = "Design Output Feature (with CTQ ID #)"

    def _validate_this_field(self) -> List[ValidationResult]:
        return []


@collect_field
class CTQ(Field):
    field_name = "CTQ? Yes, No, N/A"

    def _validate_this_field(self) -> List[ValidationResult]:
        return []


@collect_field
class Devices(Field):
    field_name = "Devices"

    def _validate_this_field(self) -> List[ValidationResult]:
        return [val.val_cells_not_empty(self._body)]


if __name__ == "__main__":
    pass
