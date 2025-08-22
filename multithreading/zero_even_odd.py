import threading
import time


solution = []


def printNumber(n: int):
    solution.append(str(n))




class ZeroEvenOdd:
    def __init__(self, n):
        self.n = n
        self.num = 0
        self.debug = True
        
	# printNumber(x) outputs "x", where x is an integer.
    def zero(self, printNumber: 'Callable[[int], None]') -> None:
        while True:

            printNumber(0)

        
    def even(self, printNumber: 'Callable[[int], None]') -> None:
        while True:
            printNumber(self.num)

        
    def odd(self, printNumber: 'Callable[[int], None]') -> None:
        while True:
            printNumber(self.num)



def main():
    nums = [
        2,
        5,
        # 1,
        # 15,
        # 120,
        # 18,
        # 1000,
    ]
    for num in nums:
        zeo = ZeroEvenOdd(n=num)
        global solution
        solution = []
        threads = [
            threading.Thread(target=zeo.zero, args=[printNumber]),
            threading.Thread(target=zeo.even, args=[printNumber]),
            threading.Thread(target=zeo.odd, args=[printNumber]),
        ]
        for thread in threads: thread.start()
        for thread in threads: thread.join()
        print(f"n={num}, solution: {solution}")
        print("\n----------------------------------------------------------------------------------------------------\n")
        time.sleep(0.2)


if __name__ == "__main__":
    main()
