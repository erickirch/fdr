# --- Standard Library Imports ------------------------------------------------
from contextlib import contextmanager

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
from rtm.main.exceptions import UninitializedError


class ContextManager:

    def __init__(self, name):
        """Easily share data amongst all the functions"""
        self._name = name
        self._value = None

    def __call__(self):
        if self._value is None:
            raise UninitializedError(f"The '{self._name}' ContextManager is not initialized")
        else:
            return self._value

    @contextmanager
    def set(self, value):
        self._value = value
        yield
        self._value = None


worksheet_columns = ContextManager('worksheet_columns')
fields = ContextManager('fields')
work_items = ContextManager('work_items')