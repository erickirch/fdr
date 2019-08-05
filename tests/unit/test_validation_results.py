# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
import rtm.validation.validator_output as vr


def test_print_validation_report(example_val_results):
    vr.print_validation_report("Test Field", example_val_results)


def test_print_val_header():
    vr.print_val_header("Test Field")
