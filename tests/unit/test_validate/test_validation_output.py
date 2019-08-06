# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
import pytest

# --- Intra-Package Imports ---------------------------------------------------
import rtm.validate.validator_output as vr


@pytest.mark.skip()
def test_print_validation_report(example_val_results):
    vr.print_validation_report("Test Field", example_val_results)



def test_validation_result(capsys):

    # --- Create sample validation output -------------------------------------
    title = 'You fAIL'
    score = 'Error'
    explanation = 'here are the rows that failed: '
    indices = list(range(5))
    validation_result = vr.ValidationResult(score, title, explanation, indices)

    # --- Capture result ------------------------------------------------------
    validation_result.print()
    captured = capsys.readouterr()

    # --- Compare to expected
    expected_capture = '\tError\tYOU FAIL - here are the rows that failed: (0, 1, 2, 3, 4)\n'
    assert captured.out == expected_capture


def test_output_header(capsys):
    output_header = vr.OutputHeader("Hi")
    output_header.print()
    captured = capsys.readouterr()
    expected_capture = '\n++++++++\n+  Hi  +\n++++++++\n\n'
    assert captured.out == expected_capture
