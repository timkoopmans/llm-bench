"""LiveCodeBench 3704 — count-partitions-with-even-sum-difference (leetcode, 2025-01-25, easy)

Source: https://leetcode.com/problems/count_partitions_with_even_sum_difference/

QUESTION:
You are given an integer array nums of length n.
A partition is defined as an index i where 0 <= i < n - 1, splitting the array into two non-empty subarrays such that:

Left subarray contains indices [0, i].
Right subarray contains indices [i + 1, n - 1].

Return the number of partitions where the difference between the sum of the left and right subarrays is even.
 
Example 1:

Input: nums = [10,10,3,7,6]
Output: 4
Explanation:
The 4 partitions are:

[10], [10, 3, 7, 6] with a sum difference of 10 - 26 = -16, which is even.
[10, 10], [3, 7, 6] with a sum difference of 20 - 16 = 4, which is even.
[10, 10, 3], [7, 6] with a sum difference of 23 - 13 = 10, which is even.
[10, 10, 3, 7], [6] with a sum difference of 30 - 6 = 24, which is even.


Example 2:

Input: nums = [1,2,2]
Output: 0
Explanation:
No partition results in an even sum difference.

Example 3:

Input: nums = [2,4,6,8]
Output: 3
Explanation:
All partitions result in an even sum difference.

 
Constraints:

2 <= n == nums.length <= 100
1 <= nums[i] <= 100

NOTE FOR THE MODEL:
Implement class `Solution` with method `countPartitions` exactly matching
the signature in the starter code below. Do NOT include any tests,
doctests, or `if __name__` block. Your code will be concatenated
above the spec which runs your Solution against canonical tests.

STARTER CODE:
class Solution:
    def countPartitions(self, nums: List[int]) -> int:
"""
import json
import unittest


class Test_count_partitions_with_even_sum_difference(unittest.TestCase):
    def test_public_1(self):
        args = [json.loads(line) for line in '[10, 10, 3, 7, 6]'.strip().split('\n') if line.strip()]
        expected = json.loads('4')
        result = Solution().countPartitions(*args)
        self.assertEqual(result, expected)
    def test_public_2(self):
        args = [json.loads(line) for line in '[1, 2, 2]'.strip().split('\n') if line.strip()]
        expected = json.loads('0')
        result = Solution().countPartitions(*args)
        self.assertEqual(result, expected)
    def test_public_3(self):
        args = [json.loads(line) for line in '[2, 4, 6, 8]'.strip().split('\n') if line.strip()]
        expected = json.loads('3')
        result = Solution().countPartitions(*args)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
