# --- Standard Library Imports ------------------------------------------------
from typing import List
from rtm.fields.field import Field
from rtm.worksheet_columns import WorksheetColumn
# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
import rtm.fields.validation as val
from rtm.fields import Field
from rtm.fields.validation_results import ValidationResult


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


@collect_field
class Devices(Field):
    field_name = "Devices"

    def _validate_this_field(self) -> List[ValidationResult]:
        return [val.val_cells_not_empty(self._body)]


if __name__ == "__main__":
    pass
