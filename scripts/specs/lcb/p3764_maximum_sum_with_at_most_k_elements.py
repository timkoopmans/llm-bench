"""LiveCodeBench 3764 — maximum-sum-with-at-most-k-elements (leetcode, 2025-02-22, medium)

Source: https://leetcode.com/problems/maximum_sum_with_at_most_k_elements/

QUESTION:
You are given a 2D integer matrix grid of size n x m, an integer array limits of length n, and an integer k. The task is to find the maximum sum of at most k elements from the matrix grid such that:


The number of elements taken from the i^th row of grid does not exceed limits[i].


Return the maximum sum.
 
Example 1:

Input: grid = [[1,2],[3,4]], limits = [1,2], k = 2
Output: 7
Explanation:

From the second row, we can take at most 2 elements. The elements taken are 4 and 3.
The maximum possible sum of at most 2 selected elements is 4 + 3 = 7.


Example 2:

Input: grid = [[5,3,7],[8,2,6]], limits = [2,2], k = 3
Output: 21
Explanation:

From the first row, we can take at most 2 elements. The element taken is 7.
From the second row, we can take at most 2 elements. The elements taken are 8 and 6.
The maximum possible sum of at most 3 selected elements is 7 + 8 + 6 = 21.


 
Constraints:

n == grid.length == limits.length
m == grid[i].length
1 <= n, m <= 500
0 <= grid[i][j] <= 10^5
0 <= limits[i] <= m
0 <= k <= min(n * m, sum(limits))

NOTE FOR THE MODEL:
Implement class `Solution` with method `maxSum` exactly matching
the signature in the starter code below. Do NOT include any tests,
doctests, or `if __name__` block. Your code will be concatenated
above the spec which runs your Solution against canonical tests.

STARTER CODE:
class Solution:
    def maxSum(self, grid: List[List[int]], limits: List[int], k: int) -> int:
"""
import json
import unittest


class Test_maximum_sum_with_at_most_k_elements(unittest.TestCase):
    def test_public_1(self):
        args = [json.loads(line) for line in '[[1, 2], [3, 4]]\n[1, 2]\n2'.strip().split('\n') if line.strip()]
        expected = json.loads('7')
        result = Solution().maxSum(*args)
        self.assertEqual(result, expected)
    def test_public_2(self):
        args = [json.loads(line) for line in '[[5, 3, 7], [8, 2, 6]]\n[2, 2]\n3'.strip().split('\n') if line.strip()]
        expected = json.loads('21')
        result = Solution().maxSum(*args)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
