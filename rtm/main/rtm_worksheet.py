# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
import rtm.main.context_managers as context
import rtm.containers.fields as fields
from rtm.containers import worksheet_columns as wc
from rtm.containers import work_items as wi


class RTMWorksheet:

    def __init__(self):
        # --- Get raw data ----------------------------------------------------
        #     Path should already be set by context manager
        worksheet_columns = wc.read_worksheet_columns("Procedure Based Requirements")
        # --- Initialize field objects (i.e. columns) -------------------------
        with context.worksheet_columns.set(worksheet_columns):
            self.fields = fields.Fields()
        # --- Initialize work items (i.e. rows) -------------------------------
        with context.fields.set(self.fields):
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
