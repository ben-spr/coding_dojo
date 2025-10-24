import random
import pathlib

nums = [random.randint() for _ in range(10000)]

newfile = pathlib.Path( pathlib.Path(__file__).parent + "nums.txt" )
