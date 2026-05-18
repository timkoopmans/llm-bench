"""LiveCodeBench 3722 — sum-of-k-subarrays-with-length-at-least-m (leetcode, 2025-03-01, medium)

Source: https://leetcode.com/problems/sum_of_k_subarrays_with_length_at_least_m/

QUESTION:
You are given an integer array nums and two integers, k and m.
Return the maximum sum of k non-overlapping subarrays of nums, where each subarray has a length of at least m.
 
Example 1:

Input: nums = [1,2,-1,3,3,4], k = 2, m = 2
Output: 13
Explanation:
The optimal choice is:

Subarray nums[3..5] with sum 3 + 3 + 4 = 10 (length is 3 >= m).
Subarray nums[0..1] with sum 1 + 2 = 3 (length is 2 >= m).

The total sum is 10 + 3 = 13.

Example 2:

Input: nums = [-10,3,-1,-2], k = 4, m = 1
Output: -10
Explanation:
The optimal choice is choosing each element as a subarray. The output is (-10) + 3 + (-1) + (-2) = -10.

 
Constraints:

1 <= nums.length <= 2000
-10^4 <= nums[i] <= 10^4
1 <= k <= floor(nums.length / m)
1 <= m <= 3

NOTE FOR THE MODEL:
Implement class `Solution` with method `maxSum` exactly matching
the signature in the starter code below. Do NOT include any tests,
doctests, or `if __name__` block. Your code will be concatenated
above the spec which runs your Solution against canonical tests.

STARTER CODE:
class Solution:
    def maxSum(self, nums: List[int], k: int, m: int) -> int:
"""
import json
import unittest


class Test_sum_of_k_subarrays_with_length_at_least_m(unittest.TestCase):
    def test_public_1(self):
        args = [json.loads(line) for line in '[1, 2, -1, 3, 3, 4]\n2\n2'.strip().split('\n') if line.strip()]
        expected = json.loads('13')
        result = Solution().maxSum(*args)
        self.assertEqual(result, expected)
    def test_public_2(self):
        args = [json.loads(line) for line in '[-10, 3, -1, -2]\n4\n1'.strip().split('\n') if line.strip()]
        expected = json.loads('-10')
        result = Solution().maxSum(*args)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
