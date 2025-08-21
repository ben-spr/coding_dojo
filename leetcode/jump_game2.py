class Solution:
    def jump(self, nums: List[int]) -> int:
        if len(nums) == 1:
            return 0
        jumps = 0
        jump_length = 1

        while nums:
            
            potential_jump = 0
            for i in range(jump_length):
                potential_jump = max(nums.pop(0) - jump_length + i + 1, potential_jump)
                if potential_jump >= len(nums):
                    return jumps + 1

            jump_length = potential_jump
            jumps += 1
            
        return jumps
    
""" try: greedy algorithm

    [2,3,4,0,5,6,4,8,2,3,8,6,1,2,3,5,6,5,7,!end!]

    [2,  3,4,   0,5,6,4   ,8,2,3,8,6   1,2,3,5,6,5,7,  end]
        2 4     0 3 5 4    3 0 0 7 6   0 0 0 