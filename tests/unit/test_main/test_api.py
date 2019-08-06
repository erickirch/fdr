# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
from rtm.main.api import validate


def test_validate(rtm_path):
    validate(rtm_path)
