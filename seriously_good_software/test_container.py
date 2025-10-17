from container import Container

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

    a.amount = 12
    d.amount = 8
    #  a   b   c   d
    # [12][ 0][ 0][ 8]
    assert_amounts(12,0,0,8)

    a.connect(b)
    #  a---b   c   d
    # [ 6][ 6][ 0][ 8]
    assert_amounts(6,6,0,8)

    b.connect(c)
    #  a---b---c   d
    # [ 4][ 4][ 4][ 8]
    assert_amounts(4,4,4,8) # a is now indirectly connected to c (via b)

    b.connect(d)
    #      ┌-------┐
    #  a---b---c   d
    # [ 5][ 5][ 5][ 5]
    assert_amounts(5,5,5,5)

    a.amount += 4 # Additional amount is split into the four containers
    #      ┌-------┐
    #  a---b---c   d
    # [ 6][ 6][ 6][ 6]
    assert_amounts(6,6,6,6)


if __name__ == '__main__':
    demonstrate_usage()
