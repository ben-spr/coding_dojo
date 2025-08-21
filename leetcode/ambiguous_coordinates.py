from itertools import product

class Solution:
    def __init__(self):
        self.significant = {str(num) for num in range(1,10)}

    def ambiguousCoordinates(self, s: str) -> list[str]:
        solution = []
        for slice_index in range(2, len(s)-1):
            left = s[1:slice_index]
            right = s[slice_index:-1]
            if not (sol_left := self.create_permutations(left)):
                continue
            if not (sol_right := self.create_permutations(right)):
                continue
            sols = product(sol_left, sol_right)
            for l, r in sols:
                solution.append(f"({l}, {r})")

        return solution

    @staticmethod
    def create_permutations(s: str) -> list[str]:
        permutations = []
        if len(s) > 1 and s[0] == "0" and s[-1] == "0":
            return permutations
        
        permutations.append(s)
        if len(s) == 1 or s[-1] == "0":
            return permutations
        
        for i in range(1, len(s)):
            left, right = s[:i], s[i:]
            if left == "0":
                return [".".join([left, right])]
            permutations.append(".".join([left, right]))
        return permutations

    # def ambiguousCoordinates(self, s: str) -> list[str]:
    #     solutions = []
    #     s = s[1:-1]
    #     for i in range(1, len(s)):
    #         left = s[:i]
    #         right = s[i:]
    #         # sol_left = self.create_permutations(left)
    #         # sol_right = self.create_permutations(right)
    #         sol_left, sol_right = map(self.create_permutations, (left, right))
    #         if self.debug: print(f"Mapping permutation func to left/right part of the string worked. Output:\n{sol_left=}\n{sol_right=}\n----------")
    #         if sol_left is None or sol_right is None:
    #             continue
    #         solutions += list(product(sol_left, sol_right))
    #     solution = [self.convert_tuple_to_string(sol) for sol in solutions]
    #     if self.debug: print(f"{s=}: {solution=}")
    #     return solution

    # def convert_tuple_to_string(self, t: tuple[str, str]) -> str:
    #     a, b = t
    #     s = f"({a}, {b})"
    #     if self.debug: print(f"Converted tuple {t} to string {s}")
    #     return s
