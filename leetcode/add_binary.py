# from abc import abstractmethod

# class Node:
#     def __init__(self, value: str = "0", in_1 = None, in_2 = None):
#         self.value = value
#         self.in_1 = in_1
#         self.in_2 = in_2

#     @abstractmethod
#     def eval(self):
#         pass

# class XOR(Node):
#     def eval(self):
#         if (in_1.value == "1" and in_2.value == "0") or (in_1.value == "0" and in_2.value == "1"):
#             self.value = "1"
#         else:
#             self.value = "0"

class Solution:
    def addBinary(self, a: str, b: str) -> str:
        digits = max(len(a), len(b)) + 1
        a = a.zfill(digits)
        b = b.zfill(digits)
        c = ["0"] * digits
        carryover = "0"
        for i in range(-1, -1 * digits - 1, -1):
            c[i] = XOR( XOR(a[i], b[i]), carryover )
            carryover = OR(AND(a[i], b[i]), AND(carryover, OR(a[i], b[i])))
        
        return "".join(c) if c[0] == "1" else "".join(c[1:])
    
def AND(a: str, b: str) -> str:
    if a == "1" and b == "1":
        return "1"
    return "0"

def OR(a: str, b: str) -> str:
    if a == "1" or b == "1":
        return "1"
    return "0"

def XOR(a: str, b: str) -> str:
    if (a == "0" and b == "1") or (a == "1" and b == "0"):
        return "1"
    return "0"

def NEITHER(a: str, b: str) -> str:
    if a == "0" and b == "0":
        return "1"
    return "0"

def main():
    test_inputs = [
        ("1000", "0101"),
        ("11111", "00001"),
    ]
    solution = Solution()
    for a, b in test_inputs:
        print(solution.addBinary(a, b))

main()
