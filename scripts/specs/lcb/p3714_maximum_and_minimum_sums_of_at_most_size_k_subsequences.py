"""LiveCodeBench 3714 — maximum-and-minimum-sums-of-at-most-size-k-subsequences (leetcode, 2025-01-18, medium)

Source: https://leetcode.com/problems/maximum_and_minimum_sums_of_at_most_size_k_subsequences/

QUESTION:
You are given an integer array nums and a positive integer k. Return the sum of the maximum and minimum elements of all subsequences of nums with at most k elements.
Since the answer may be very large, return it modulo 10^9 + 7.
 
Example 1:

Input: nums = [1,2,3], k = 2
Output: 24
Explanation:
The subsequences of nums with at most 2 elements are:



Subsequence 
Minimum
Maximum
Sum


[1]
1
1
2


[2]
2
2
4


[3]
3
3
6


[1, 2]
1
2
3


[1, 3]
1
3
4


[2, 3]
2
3
5


Final Total
 
 
24



The output would be 24.

Example 2:

Input: nums = [5,0,6], k = 1
Output: 22
Explanation: 
For subsequences with exactly 1 element, the minimum and maximum values are the element itself. Therefore, the total is 5 + 5 + 0 + 0 + 6 + 6 = 22.

Example 3:

Input: nums = [1,1,1], k = 2
Output: 12
Explanation:
The subsequences [1, 1] and [1] each appear 3 times. For all of them, the minimum and maximum are both 1. Thus, the total is 12.

 
Constraints:

1 <= nums.length <= 10^5
0 <= nums[i] <= 10^9
1 <= k <= min(70, nums.length)

NOTE FOR THE MODEL:
Implement class `Solution` with method `minMaxSums` exactly matching
the signature in the starter code below. Do NOT include any tests,
doctests, or `if __name__` block. Your code will be concatenated
above the spec which runs your Solution against canonical tests.

STARTER CODE:
class Solution:
    def minMaxSums(self, nums: List[int], k: int) -> int:
"""
import json
import unittest


class Test_maximum_and_minimum_sums_of_at_most_size_k_subsequences(unittest.TestCase):
    def test_public_1(self):
        args = [json.loads(line) for line in '[1, 2, 3]\n2'.strip().split('\n') if line.strip()]
        expected = json.loads('24')
        result = Solution().minMaxSums(*args)
        self.assertEqual(result, expected)
    def test_public_2(self):
        args = [json.loads(line) for line in '[5, 0, 6]\n1'.strip().split('\n') if line.strip()]
        expected = json.loads('22')
        result = Solution().minMaxSums(*args)
        self.assertEqual(result, expected)
    def test_public_3(self):
        args = [json.loads(line) for line in '[1, 1, 1]\n2'.strip().split('\n') if line.strip()]
        expected = json.loads('12')
        result = Solution().minMaxSums(*args)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
