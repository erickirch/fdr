# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
import rtm.main.context_managers as cm
from rtm.containers import fields as f
from rtm.containers import worksheet_columns as wc
from rtm.containers import work_items as wi


class RTMWorksheet:

    def __init__(self, path):
        # --- Get raw data ----------------------------------------------------
        worksheet_columns = wc.read_worksheet_columns(path, "Procedure Based Requirements")
        # --- Initialize field objects (i.e. columns) -------------------------
        with cm.worksheet_columns.set(worksheet_columns):
            self.fields = [Field() for Field in f.field_classes]
        # --- Initialize work items (i.e. rows) -------------------------------
        with cm.fields(self.fields):
            self.work_items = wi.WorkItems()

    def validate(self):
        # --- Check Field Sorting ---------------------------------------------
        index_current = -1
        for field in self.fields:
            index_current = field.validate_position(index_current)

        # --- Validate Fields and Print Results -------------------------------
        for field in self.fields:
            field.validate()


if __name__ == "__main__":
    pass
