from threading import Condition, Lock
from typing import Callable


class DiningPhilosophers_CondPhilosophers:

    def __init__(self):
        # self.forks_in_use: list[bool] = [False]*5
        self.is_eating: list[bool] = [False] * 5
        self.cond: Condition = Condition()
        self.debug = False

    # call the functions directly to execute, for example, eat()
    def wantsToEat(self,
                   philosopher: int,
                   pickLeftFork: Callable[[], None],
                   pickRightFork: Callable[[], None],
                   eat: Callable[[], None],
                   putLeftFork: Callable[[], None],
                   putRightFork: Callable[[], None]) -> None:

        if self.debug: print(f"Philosopher {philosopher} wants to eat")

        with self.cond:
            if self.debug: print(f"Philosopher {philosopher} entered condition")
            self.cond.wait_for(
                lambda: not self.is_eating[(philosopher - 1) % 5] and not self.is_eating[(philosopher + 1) % 5])
            if self.debug: print(f"Philosopher {philosopher} past wait for")
            self.is_eating[philosopher] = True
            if self.debug: print(f"Philosopher {philosopher} started eating")

        if self.debug: print(f"Philosopher {philosopher} pickLeft")
        pickLeftFork()
        if self.debug: print(f"Philosopher {philosopher} pickRight")
        pickRightFork()
        if self.debug: print(f"Philosopher {philosopher} Eat")
        eat()
        if self.debug: print(f"Philosopher {philosopher} putLeft")
        putLeftFork()
        if self.debug: print(f"Philosopher {philosopher} putRight")
        putRightFork()
        if self.debug: print(f"Philosopher {philosopher} stop eating")
        self.is_eating[philosopher] = False
        if self.debug: print(f"Philosopher {philosopher} pre Notify")
        with self.cond:
            self.cond.notify_all()

class DiningPhilosophers_CondFork:
    def __init__(self):
        self.forks = [True for _ in range(5)]
        # self.fork_lock = threading.Lock()
        self.fork_cond = Condition()
        self.debug = True

    # call the functions directly to execute, for example, eat()
    def wantsToEat(self,
                   philosopher: int,
                   pickLeftFork: 'Callable[[], None]',
                   pickRightFork: 'Callable[[], None]',
                   eat: 'Callable[[], None]',
                   putLeftFork: 'Callable[[], None]',
                   putRightFork: 'Callable[[], None]') -> None:
        with self.fork_cond:
            # if self.debug: print(f"")
            if self.debug: print(f"Condition initially acquired by {philosopher=}.")
            self.fork_cond.wait_for(lambda : (self.forks[philosopher] and self.forks[philosopher-1]) )
            pickLeftFork()
            self.forks[philosopher-1] = False
            # self.fork_cond.notify_all()
            pickRightFork()
            self.forks[philosopher-1] = False
            # self.fork_cond.notify_all()
            eat()
            putLeftFork()
            self.forks[philosopher-1] = True
            self.fork_cond.notify_all()
            putRightFork()
            self.forks[philosopher-1] = True
            self.fork_cond.notify_all()


class DiningPhilosophers_Lock:
    def __init__(self):
        self.forks = [True for n in range(5)]
        self.lock = Lock()

    # call the functions directly to execute, for example, eat()
    def wantsToEat(self,
                   philosopher: int,
                   pickLeftFork: 'Callable[[], None]',
                   pickRightFork: 'Callable[[], None]',
                   eat: 'Callable[[], None]',
                   putLeftFork: 'Callable[[], None]',
                   putRightFork: 'Callable[[], None]') -> None:
        with self.lock:
            pickLeftFork()
            pickRightFork()
            eat()
            putLeftFork()
            putRightFork()
        