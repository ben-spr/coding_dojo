import itertools
import random
import threading
import typing
from concurrent.futures.thread import ThreadPoolExecutor

import pytest

print_lock = threading.RLock()
print_disable = False


def lprint(message: str) -> None:
    if print_disable:
        return

    with print_lock:
        print(f"{threading.current_thread().name}: {message}")


class H2O:

    def __init__(self):
        # your sync-primitives
        self.lock = threading.Lock()
        self.cv_water = threading.Condition(lock=self.lock)
        self.cv_h = threading.Condition(lock=self.lock)
        self.cv_o = threading.Condition(lock=self.lock)
        self.h_count = 0
        self.o_count = 0
        self.h_waiting = 0
        self.o_waiting = 0
        print("H2O initialized")

    def hydrogen(self, releaseHydrogen: "Callable[[], None]") -> None:
        lprint("Hydrogen thread started")
  
        # Your Code!
        with self.lock:
            while self.h_count == 2:
                self.cv_h.wait()
            self.h_count += 1
            if self.h_waiting == 1 and self.o_waiting == 1:
                self.h_waiting -= 1
                self.o_waiting -= 1
                self.cv_water.notify_all()
            else:
                self.h_waiting += 1
                self.cv_water.wait()
            releaseHydrogen()
            self.h_count -= 1
            self.cv_h.notify()
            # releaseHydrogen() outputs "H". Do not change or remove this line.



    def oxygen(self, releaseOxygen: "Callable[[], None]") -> None:
        lprint("Oxygen thread started")
  
        # Your Code!
        with self.lock:
            while self.o_count == 1:
                self.cv_o.wait()
            if self.h_waiting == 2:
                self.h_waiting -= 2
                self.cv_water.notify_all()
            else:
                self.o_waiting += 1
                self.cv_water.wait()
            releaseOxygen()
            self.o_count -= 1
            self.cv_o.notify()
            # releaseOxygen() outputs "O". Do not change or remove this line.



# ---------- Test Infrastructure, requires Pytest -------------------
def batched(iterable, n):
    it = iter(iterable)
    while batch := list(itertools.islice(it, n)):
        yield batch


def create_input_samples(
    samples_per_length: int, number_of_molecules: int
) -> typing.Generator[tuple[int, list[str]], None, None]:
    sample = list()
    for _ in range(number_of_molecules):
        sample.extend(["H"] * 2 + ["O"])
    for _ in range(samples_per_length):
        random.shuffle(sample)
        yield number_of_molecules, list(sample)


@pytest.mark.parametrize("repetitions", [3])
@pytest.mark.parametrize(
    "number_of_molecules", [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233]
)
def test_h20(repetitions, number_of_molecules):

    for rep_no, (length, sample) in enumerate(
        create_input_samples(repetitions, number_of_molecules), 1
    ):
        print(
            f"\nTesting H2O with {length} molecules, sample {rep_no} of {repetitions}"
        )
        print(f"Sample: {''.join(sample)}")
        h2o = H2O()
        result: list[str] = list()
        with ThreadPoolExecutor(max_workers=number_of_molecules * 3) as executor:
            for atom in sample:
                if atom == "H":
                    executor.submit(lambda: h2o.hydrogen(lambda: result.append("H")))
                elif atom == "O":
                    executor.submit(lambda: h2o.oxygen(lambda: result.append("O")))

        # Wait for all threads to complete
        executor.shutdown()

        assert len(result) == length * 3
        assert result.count("H") == length * 2
        assert result.count("O") == length
        for no, molecule in enumerate(batched(result, 3), 1):
            print(f"Checking molecule {no}/{length}: {''.join(molecule)}")
            assert molecule.count("H") == 2
            assert molecule.count("O") == 1


if __name__ == "__main__":
    print("Running H2O test...")
    pytest.main(["-v", __file__])
 