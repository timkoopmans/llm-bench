"""LiveCodeBench 3751 — maximum-frequency-after-subarray-operation (leetcode, 2025-01-25, medium)

Source: https://leetcode.com/problems/maximum_frequency_after_subarray_operation/

QUESTION:
You are given an array nums of length n. You are also given an integer k.
You perform the following operation on nums once:

Select a subarray nums[i..j] where 0 <= i <= j <= n - 1.
Select an integer x and add x to all the elements in nums[i..j].

Find the maximum frequency of the value k after the operation.
 
Example 1:

Input: nums = [1,2,3,4,5,6], k = 1
Output: 2
Explanation:
After adding -5 to nums[2..5], 1 has a frequency of 2 in [1, 2, -2, -1, 0, 1].

Example 2:

Input: nums = [10,2,3,4,5,5,4,3,2,2], k = 10
Output: 4
Explanation:
After adding 8 to nums[1..9], 10 has a frequency of 4 in [10, 10, 11, 12, 13, 13, 12, 11, 10, 10].

 
Constraints:

1 <= n == nums.length <= 10^5
1 <= nums[i] <= 50
1 <= k <= 50

NOTE FOR THE MODEL:
Implement class `Solution` with method `maxFrequency` exactly matching
the signature in the starter code below. Do NOT include any tests,
doctests, or `if __name__` block. Your code will be concatenated
above the spec which runs your Solution against canonical tests.

STARTER CODE:
class Solution:
    def maxFrequency(self, nums: List[int], k: int) -> int:
"""
import json
import unittest


class Test_maximum_frequency_after_subarray_operation(unittest.TestCase):
    def test_public_1(self):
        args = [json.loads(line) for line in '[1, 2, 3, 4, 5, 6]\n1'.strip().split('\n') if line.strip()]
        expected = json.loads('2')
        result = Solution().maxFrequency(*args)
        self.assertEqual(result, expected)
    def test_public_2(self):
        args = [json.loads(line) for line in '[10, 2, 3, 4, 5, 5, 4, 3, 2, 2]\n10'.strip().split('\n') if line.strip()]
        expected = json.loads('4')
        result = Solution().maxFrequency(*args)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
