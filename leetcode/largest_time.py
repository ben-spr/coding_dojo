from typing import List
import itertools

class Solution:
    def largestTimeFromDigits(self, arr: List[int]) -> str:
        num = None
        permutations = list(itertools.permutations(arr,4))
        for perm in permutations:
            if self.valid_time(perm):
                num = perm
        if num:
            return f"{num[0]}{num[1]}:{num[2]}{num[3]}"

    def valid_time(self, arr: List[int]) -> bool:
        if (arr[0]*10+arr[1]) < 24 and (arr[2]*10+arr[3]) < 60:
            return True
        else:
            return False


s=Solution()
s.largestTimeFromDigits([1,2,3,4])
