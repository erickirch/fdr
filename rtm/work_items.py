# --- Standard Library Imports ------------------------------------------------
import collections
from contextlib import contextmanager
from typing import List

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
from rtm.exceptions import UninitializedError
from rtm.fields.validation import cell_empty


_fields = None


class WorkItems(collections.abc.Sequence):
    def __init__(self, cascade_block_body: List[list]):
        self._initialize_work_items(cascade_block_body)
        self._calculate_parents()

    def _initialize_work_items(self, cascade_block_body):
        work_item_count = len(cascade_block_body[0])
        self._work_items = [WorkItem(index) for index in range(work_item_count)]
        for work_item in self._work_items:
            row = get_row(cascade_block_body, work_item.index)
            work_item.set_cascade_block_row(row)

    def _calculate_parents(self):
        """
        Each item can have only one parent. To determine:
            previous row = the first above that contains at least one value_at_index

            If level = 0, no parent
            If above row is one level to the left, use that row as the parent
            If above row is more than one level to the left: error. Store a list of items that error out
            If above row is same level, use its same parents. If parent errors, this rcv's an error too
        Graph data is stored as follows:
            list, where index = index of each item
            value_at_index: [int], the index of its parent or None if no parent or
        """
        for work_item in self._work_items:

            # set default
            work_item.parent = None

            # If no position (row was blank), then no parent
            if work_item.position is None:
                continue

            # If in first position, then it's the trunk of a tree!
            if work_item.position == 0:
                work_item.parent = -1
                continue

            for index_ in reversed(range(work_item.index)):

                cur_work_item = self._work_items[index_]

                if cur_work_item.position is None:
                    continue
                if work_item.position < cur_work_item.position:
                    continue

                if cur_work_item.position == work_item.position:
                    # same column, same parent
                    work_item.parent = cur_work_item.parent
                elif cur_work_item.position == work_item.position - 1:
                    # one column to the left; that work item IS the parent
                    work_item.parent = cur_work_item.index
                else:
                    # cur_work_item is too far to the left. There's a gap in the chain
                    work_item.parent = None
                break

    def validate(self):
        """
        Check that each row has one and only one entry.
        That entry has to be X or F
        Check: ITEM COUNT: Pass if 1; Error if 0 (if any have errors, convert all warnings to error),
                Warning if >1 (warn that only the first is taken into account)
                or report both if both error and warning?
        if index=0, level must == 0. If not, error
        """
        pass

    def __getitem__(self, item):
        return self._work_items[item]

    def __len__(self):
        return len(self._work_items)


class WorkItem:

    def __init__(self):
        self.parent = None

    # @property
    # def parent(self):
    #     return
    #
    # @parent.setter
    # def parent(self, parent_index: int):
    #     if isinstance()

    def has_parent(self):
        if self.parent >= 0:
            return True
        else:
            return False

    def __init__(self, index_: int):
        self._index = index_
        self._contents = OrderedDictList()
        self._parent = UninitializedError()

    def set_cascade_block_row(self, cascade_block_row: list):
        for index_, value_ in enumerate(cascade_block_row):
            if not cell_empty(value_):
                self._contents[index_] = value_

    @property
    def position(self):
        try:
            return self._contents.get_first_key()
        except IndexError:
            return None

    @property
    def index(self) -> int:
        return self._index

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value_):
        self._parent = value_


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

