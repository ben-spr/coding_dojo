import abc
import dataclasses


class Container(abc.ABC):

    @property
    @abc.abstractmethod
    def amount(self)->float:
        return 0

    @amount.setter
    @abc.abstractmethod
    def amount(self, amount:float)->None:
        pass

    @abc.abstractmethod
    def _connect(self, other: "Container")->None:
        pass

    def connect(self, other:"Container")->None:
        if type(self) is not type(other):
            raise TypeError(f"Cannot connect {type(self).__name__} with {type(other).__name__}")
        self._connect(other)

class FirstContainer(Container):
    def __init__(self):
        self._group:set[Container] = {self}
        self._group_amount:float = 0.0

    @property
    def amount(self)->float:
        # O(1)
        return self._group_amount/len(self._group)

    @amount.setter
    def amount(self, amount):
        # O(n)
        property_offset = self.amount  # TODO: difficult to understand. refactor code to improve
        for container in self._group:
            container._group_amount += amount - property_offset

    def _connect(self, other: "Container"):
        # O(n)
        if other in self._group:
            return
        total_amount = self._group_amount + other._group_amount
        all_connected = self._group.union(other._group)
        for container in all_connected:
            container._group = all_connected
            container._group_amount = total_amount

@dataclasses.dataclass
class Group:
    members:set[Container] = dataclasses.field(default_factory=set)
    total_amount:float = 0.0
    number_of_members:int = 0

class FastAmountChangeContainerWithGroupObject(Container):
    def __init__(self):
        self._group = Group()
        self._group.members.add(self)
        self._group.number_of_members = 1

    @property
    def amount(self) -> float:
        return self._group.total_amount/self._group.number_of_members

    @amount.setter
    def amount(self, amount: float):
        self._group.total_amount # Hier weiter

    def _connect(self, other: "Container") -> None:
        pass


class FastAmountChangeContainerWithDictionary(Container):
    pass

class FastConnectContainer(Container):
    pass

class FastOnAverageContainer(Container):
    pass

def demonstrate_usage():
    """
    Demonstrates water distribution among four containers.
    Each step shows the expected state using ASCII-art diagrams:
      - Lines (---, ┌---┐, etc.) indicate connections.
      - Numbers in brackets show the amount of water in each container.

    See:
    Seriously Good Software: Code That Works, Survives, and Wins
    https://accenture.percipio.com/books/0bf5181b-2be2-401d-b932-705f86a69a26
    https://www.amazon.de/-/en/dp/B08DZC34WF

    """

    a = FirstContainer()
    b = FirstContainer()
    c = FirstContainer()
    d = FirstContainer()

    def assert_amounts(a_amount: float, b_amount: float, c_amount: float, d_amount: float) -> None:
        assert a.amount == a_amount, f"a: expected {a_amount}, got {a.amount}"
        assert b.amount == b_amount, f"b: expected {b_amount}, got {b.amount}"
        assert c.amount == c_amount, f"c: expected {c_amount}, got {c.amount}"
        assert d.amount == d_amount, f"d: expected {d_amount}, got {d.amount}"

    a.amount = 12.0
    d.amount = 8.0
    #  a   b   c   d
    # [12][ 0][ 0][ 8]
    assert_amounts(12.0,0.0,0.0,8.0)

    a.connect(b)
    #  a---b   c   d
    # [ 6][ 6][ 0][ 8]
    assert_amounts(6.0,6.0,0.0,8.0)

    #####
    # c.connect(d)
    #  a---b   c---d
    # [ 6][ 6][ 4][ 4]
    # assert_amounts(6.0,6.0,4.0,4.0)
    ####

    b.connect(c)
    #  a---b---c   d
    # [ 4][ 4][ 4][ 8]
    assert_amounts(4.0,4.0,4.0,8.0) # a is now indirectly connected to c (via b)

    b.connect(d)
    #      ┌-------┐
    #  a---b---c   d
    # [ 5][ 5][ 5][ 5]
    assert_amounts(5.0,5.0,5.0,5.0)

    a.amount += 4.0 # Additional amount is split into the four containers
    #      ┌-------┐
    #  a---b---c   d
    # [ 6][ 6][ 6][ 6]
    assert_amounts(6.0,6.0,6.0,6.0)

def demonstrate_performance():
    # Create 20k Containers
    # Add Random Amount to all of them
    # Connect pairs of 2
    # Add Random Amount to each pair
    # Query the Amount in each pair
    # Connect Pairs of Containers until they are all connected, each time add some water to the new group and read.
    pass

if __name__ == '__main__':
    demonstrate_usage()
