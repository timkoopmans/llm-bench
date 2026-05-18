"""LiveCodeBench 3705 — find-the-largest-almost-missing-integer (leetcode, 2025-03-01, easy)

Source: https://leetcode.com/problems/find_the_largest_almost_missing_integer/

QUESTION:
You are given an integer array nums and an integer k.
An integer x is almost missing from nums if x appears in exactly one subarray of size k within nums.
Return the largest almost missing integer from nums. If no such integer exists, return -1.
A subarray is a contiguous sequence of elements within an array.
 
Example 1:

Input: nums = [3,9,2,1,7], k = 3
Output: 7
Explanation:

1 appears in 2 subarrays of size 3: [9, 2, 1] and [2, 1, 7].
2 appears in 3 subarrays of size 3: [3, 9, 2], [9, 2, 1], [2, 1, 7].
3 appears in 1 subarray of size 3: [3, 9, 2].
7 appears in 1 subarray of size 3: [2, 1, 7].
9 appears in 2 subarrays of size 3: [3, 9, 2], and [9, 2, 1].

We return 7 since it is the largest integer that appears in exactly one subarray of size k.

Example 2:

Input: nums = [3,9,7,2,1,7], k = 4
Output: 3
Explanation:

1 appears in 2 subarrays of size 4: [9, 7, 2, 1], [7, 2, 1, 7].
2 appears in 3 subarrays of size 4: [3, 9, 7, 2], [9, 7, 2, 1], [7, 2, 1, 7].
3 appears in 1 subarray of size 4: [3, 9, 7, 2].
7 appears in 3 subarrays of size 4: [3, 9, 7, 2], [9, 7, 2, 1], [7, 2, 1, 7].
9 appears in 2 subarrays of size 4: [3, 9, 7, 2], [9, 7, 2, 1].

We return 3 since it is the largest and only integer that appears in exactly one subarray of size k.

Example 3:

Input: nums = [0,0], k = 1
Output: -1
Explanation:
There is no integer that appears in only one subarray of size 1.

 
Constraints:

1 <= nums.length <= 50
0 <= nums[i] <= 50
1 <= k <= nums.length

NOTE FOR THE MODEL:
Implement class `Solution` with method `largestInteger` exactly matching
the signature in the starter code below. Do NOT include any tests,
doctests, or `if __name__` block. Your code will be concatenated
above the spec which runs your Solution against canonical tests.

STARTER CODE:
class Solution:
    def largestInteger(self, nums: List[int], k: int) -> int:
"""
import json
import unittest


class Test_find_the_largest_almost_missing_integer(unittest.TestCase):
    def test_public_1(self):
        args = [json.loads(line) for line in '[3, 9, 2, 1, 7]\n3'.strip().split('\n') if line.strip()]
        expected = json.loads('7')
        result = Solution().largestInteger(*args)
        self.assertEqual(result, expected)
    def test_public_2(self):
        args = [json.loads(line) for line in '[3, 9, 7, 2, 1, 7]\n4'.strip().split('\n') if line.strip()]
        expected = json.loads('3')
        result = Solution().largestInteger(*args)
        self.assertEqual(result, expected)
    def test_public_3(self):
        args = [json.loads(line) for line in '[0, 0]\n1'.strip().split('\n') if line.strip()]
        expected = json.loads('-1')
        result = Solution().largestInteger(*args)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
