class Container:
    def __init__(self):
        self._group:set[Container] = {self}
        self._group_amount:float = 0.0

    @property
    def amount(self)->float:
        return self._group_amount/len(self._group)

    @amount.setter
    def amount(self, amount):
        property_offset = self.amount  # TODO: difficult to understand. refactor code to improve
        for container in self._group:
            container._group_amount += amount - property_offset

    def connect(self, other:"Container"):
        if other in self._group:
            return
        total_amount = self._group_amount + other._group_amount
        all_connected = self._group.union(other._group)
        for container in all_connected:
            container._group = all_connected
            container._group_amount = total_amount


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

    a = Container()
    b = Container()
    c = Container()
    d = Container()

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
    # a.amount = a.amount + 4.0 # Additional amount is split into the four containers
    #      ┌-------┐
    #  a---b---c   d
    # [ 6][ 6][ 6][ 6]
    assert_amounts(6.0,6.0,6.0,6.0)


if __name__ == '__main__':
    demonstrate_usage()
    print("All correct!") 
