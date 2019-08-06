# --- Standard Library Imports ------------------------------------------------
import collections
from typing import List

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
import rtm.main.context_managers as cm
import rtm.validate.validation as val
from rtm.containers.field_base import Field, SingleColumnField
from rtm.validate.validator_output import ValidationResult, OutputHeader


class Fields(collections.abc.Sequence):

    # --- Class handling ------------------------------------------------------

    _field_classes = []

    @classmethod
    def _get_field_classes(cls):
        return cls._field_classes

    @classmethod
    def append_field(cls, field_class: Field):
        # if not issubclass(field_class, Field):
        #     raise TypeError
        cls._field_classes.append(field_class)

    @classmethod
    def collect_field(cls, collect=True):
        def decorator(field):
            if collect: # This is so I can easily switch off the collection of a field
                cls.append_field(field)
            return field
        return decorator

    # --- Object handling -----------------------------------------------------

    def __init__(self):
        self._fields = None

    def initialize(self):
        self._fields = [field_class() for field_class in self._get_field_classes()]

    # --- Sequence ------------------------------------------------------------

    def __getitem__(self, item) -> Field:
        return self._fields[item]

    def __len__(self) -> int:
        return len(self._fields)


fields = Fields()


@fields.collect_field()
class ID(SingleColumnField):
    field_name = "ID"

    def _validation_specific_to_this_field(self) -> List[ValidationResult]:
        results = [
            val.val_cells_not_empty(self._body),
        ]
        results += val.example_results()
        return results


@fields.collect_field()
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

    def validate(self):
        """
        if index=0, level must == 0. If not, error
        """
        validation_outputs = [
            OutputHeader(self.get_name()),
            val.val_cascade_block_only_one_entry(_work_items),
            val.val_cascade_block_x_or_f(_work_items),
            val.val_cascade_block_use_all_columns(_work_items, len(self._subfields))
        ]
        for output in validation_outputs:
            output.print()


# Not a collected field; rolls up under CascadeBlock
class CascadeSubfield(SingleColumnField):
    def __init__(self, all_worksheet_columns, subfield_name):
        self.subfield_name = subfield_name
        super().__init__(all_worksheet_columns)

    def get_field_name(self):
        return self.subfield_name


@fields.collect_field(False)
class CascadeLevel(SingleColumnField):
    field_name = "Cascade Level"

    def _validation_specific_to_this_field(self) -> List[ValidationResult]:
        return val.example_results()


@fields.collect_field(False)
class ReqStatement(SingleColumnField):
    field_name = "Requirement Statement"

    def _validation_specific_to_this_field(self) -> List[ValidationResult]:
        return val.example_results()


@fields.collect_field(False)
class ReqRationale(SingleColumnField):
    field_name = "Requirement Rationale"

    def _validation_specific_to_this_field(self) -> List[ValidationResult]:
        return [val.val_cells_not_empty(self._body)]


@fields.collect_field(False)
class VVStrategy(SingleColumnField):
    field_name = "Verification or Validation Strategy"

    def _validation_specific_to_this_field(self) -> List[ValidationResult]:
        return val.example_results()


@fields.collect_field(False)
class VVResults(SingleColumnField):
    field_name = "Verification or Validation Results"

    def _validation_specific_to_this_field(self) -> List[ValidationResult]:
        return []


@fields.collect_field(False)
class DOFeatures(SingleColumnField):
    field_name = "Design Output Feature (with CTQ ID #)"

    def _validation_specific_to_this_field(self) -> List[ValidationResult]:
        return []


@fields.collect_field(False)
class CTQ(SingleColumnField):
    field_name = "CTQ? Yes, No, N/A"

    def _validation_specific_to_this_field(self) -> List[ValidationResult]:
        return []


@fields.collect_field()
class Devices(SingleColumnField):
    field_name = "Devices"

    def _validation_specific_to_this_field(self) -> List[ValidationResult]:
        return [val.val_cells_not_empty(self._body)]


if __name__ == "__main__":
    for field in fields._field_classes:
        print(field)
