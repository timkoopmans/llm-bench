"""LiveCodeBench 3788 — maximum-unique-subarray-sum-after-deletion (leetcode, 2025-03-15, easy)

Source: https://leetcode.com/problems/maximum_unique_subarray_sum_after_deletion/

QUESTION:
You are given an integer array nums.
You are allowed to delete any number of elements from nums without making it empty. After performing the deletions, select a subarray of nums such that:

All elements in the subarray are unique.
The sum of the elements in the subarray is maximized.

Return the maximum sum of such a subarray.
 
Example 1:

Input: nums = [1,2,3,4,5]
Output: 15
Explanation:
Select the entire array without deleting any element to obtain the maximum sum.

Example 2:

Input: nums = [1,1,0,1,1]
Output: 1
Explanation:
Delete the element nums[0] == 1, nums[1] == 1, nums[2] == 0, and nums[3] == 1. Select the entire array [1] to obtain the maximum sum.

Example 3:

Input: nums = [1,2,-1,-2,1,0,-1]
Output: 3
Explanation:
Delete the elements nums[2] == -1 and nums[3] == -2, and select the subarray [2, 1] from [1, 2, 1, 0, -1] to obtain the maximum sum.

 
Constraints:

1 <= nums.length <= 100
-100 <= nums[i] <= 100

NOTE FOR THE MODEL:
Implement class `Solution` with method `maxSum` exactly matching
the signature in the starter code below. Do NOT include any tests,
doctests, or `if __name__` block. Your code will be concatenated
above the spec which runs your Solution against canonical tests.

STARTER CODE:
class Solution:
    def maxSum(self, nums: List[int]) -> int:
"""
import json
import unittest


class Test_maximum_unique_subarray_sum_after_deletion(unittest.TestCase):
    def test_public_1(self):
        args = [json.loads(line) for line in '[1, 2, 3, 4, 5]'.strip().split('\n') if line.strip()]
        expected = json.loads('15')
        result = Solution().maxSum(*args)
        self.assertEqual(result, expected)
    def test_public_2(self):
        args = [json.loads(line) for line in '[1, 1, 0, 1, 1]'.strip().split('\n') if line.strip()]
        expected = json.loads('1')
        result = Solution().maxSum(*args)
        self.assertEqual(result, expected)
    def test_public_3(self):
        args = [json.loads(line) for line in '[1, 2, -1, -2, 1, 0, -1]'.strip().split('\n') if line.strip()]
        expected = json.loads('3')
        result = Solution().maxSum(*args)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
