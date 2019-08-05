# --- Standard Library Imports ------------------------------------------------
import collections
from contextlib import contextmanager
from typing import List

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
from rtm.main.exceptions import UninitializedError
from rtm.validation.checks import cell_empty


_fields = None


class WorkItem:

    def __init__(self, index_: int):
        self.index = index_  # work item's vertical position relative to other work items
        # contrast with position, which is which cascade column is marked
        self.cascade_block_contents = OrderedDictList()
        self._parent = UninitializedError()

    def has_parent(self):
        if self.parent >= 0:
            return True
        else:
            return False

    def set_cascade_block_row(self, cascade_block_row: list):
        for index_, value_ in enumerate(cascade_block_row):
            if not cell_empty(value_):
                self.cascade_block_contents[index_] = value_

    @property
    def position(self):
        try:
            return self.cascade_block_contents.get_first_key()
        except IndexError:
            return None

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value_):
        self._parent = value_

    def find_parent(self, work_items):

        # set default
        self.parent = None

        if self.position is None:
            # If no position (row was blank), then no parent
            return
        elif self.position == 0:
            # If in first position, then it's the trunk of a tree!
            self.parent = -1
            return

        # Search back through previous work items
        for index_ in reversed(range(self.position)):

            other = work_items[index_]

            if other.position is None:
                # Skip work items that have a blank cascade. Keep looking.
                continue
            elif other.position == self.position:
                # same position, same parent
                self.parent = other.parent
                return
            elif other.position == self.position - 1:
                # one column to the left; that work item IS the parent
                self.parent = other.index
                return
            elif other.position < self.position - 1:
                # cur_work_item is too far to the left. There's a gap in the chain. No parent
                return
            else:
                # Skip work items that come later in the cascade. Keep looking.
                continue


class WorkItems(collections.abc.Sequence):

    def __init__(self, cascade_block_body: List[list]):
        self._initialize_work_items(cascade_block_body)
        for work_item in self._work_items:
            work_item.find_parent(self._work_items)

    def _initialize_work_items(self, cascade_block_body):
        work_item_count = len(cascade_block_body[0])
        self._work_items = [WorkItem(index_) for index_ in range(work_item_count)]
        for work_item in self._work_items:
            row_data = get_row(cascade_block_body, work_item.index)
            work_item.set_cascade_block_row(row_data)

    def __getitem__(self, item) -> WorkItem:
        return self._work_items[item]

    def __len__(self) -> WorkItem:
        return len(self._work_items)


class OrderedDictList(collections.OrderedDict):
    def value_at_index(self, index_: int):
        try:
            return list(self.values())[index_]
        except IndexError:
            raise IndexError("OrderedDictList index_ out of range")

    def get_first_key(self):
        try:
            return list(self.keys())[0]
        except IndexError:
            return None


def get_row(columns: List[list], index_: int) -> list:
    return [col[index_] for col in columns]


@contextmanager
def set_fields(fields):
    global _fields
    _fields = fields
    yield
    _fields = None


if __name__ == "__main__":

    lst = list("black")
    for index, value in enumerate(reversed(lst)):
        print(index, value)
    print("hello")
    print("rev:", reversed(lst))

    rng = reversed(range(5))
    for index in rng:
        print(index)
    print(type(rng))
