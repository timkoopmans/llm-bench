"""LiveCodeBench 3731 — sum-of-variable-length-subarrays (leetcode, 2025-01-18, easy)

Source: https://leetcode.com/problems/sum_of_variable_length_subarrays/

QUESTION:
You are given an integer array nums of size n. For each index i where 0 <= i < n, define a subarray nums[start ... i] where start = max(0, i - nums[i]).
Return the total sum of all elements from the subarray defined for each index in the array.
 
Example 1:

Input: nums = [2,3,1]
Output: 11
Explanation:



i
Subarray
Sum


0
nums[0] = [2]
2


1
nums[0 ... 1] = [2, 3]
5


2
nums[1 ... 2] = [3, 1]
4


Total Sum
 
11



The total sum is 11. Hence, 11 is the output.

Example 2:

Input: nums = [3,1,1,2]
Output: 13
Explanation:



i
Subarray
Sum


0
nums[0] = [3]
3


1
nums[0 ... 1] = [3, 1]
4


2
nums[1 ... 2] = [1, 1]
2


3
nums[1 ... 3] = [1, 1, 2]
4


Total Sum
 
13



The total sum is 13. Hence, 13 is the output.

 
Constraints:

1 <= n == nums.length <= 100
1 <= nums[i] <= 1000

NOTE FOR THE MODEL:
Implement class `Solution` with method `subarraySum` exactly matching
the signature in the starter code below. Do NOT include any tests,
doctests, or `if __name__` block. Your code will be concatenated
above the spec which runs your Solution against canonical tests.

STARTER CODE:
class Solution:
    def subarraySum(self, nums: List[int]) -> int:
"""
import json
import unittest


class Test_sum_of_variable_length_subarrays(unittest.TestCase):
    def test_public_1(self):
        args = [json.loads(line) for line in '[2, 3, 1]'.strip().split('\n') if line.strip()]
        expected = json.loads('11')
        result = Solution().subarraySum(*args)
        self.assertEqual(result, expected)
    def test_public_2(self):
        args = [json.loads(line) for line in '[3, 1, 1, 2]'.strip().split('\n') if line.strip()]
        expected = json.loads('13')
        result = Solution().subarraySum(*args)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
