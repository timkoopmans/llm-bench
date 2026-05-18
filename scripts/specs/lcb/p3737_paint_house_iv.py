"""LiveCodeBench 3737 — paint-house-iv (leetcode, 2025-01-18, medium)

Source: https://leetcode.com/problems/paint_house_iv/

QUESTION:
You are given an even integer n representing the number of houses arranged in a straight line, and a 2D array cost of size n x 3, where cost[i][j] represents the cost of painting house i with color j + 1.
The houses will look beautiful if they satisfy the following conditions:

No two adjacent houses are painted the same color.
Houses equidistant from the ends of the row are not painted the same color. For example, if n = 6, houses at positions (0, 5), (1, 4), and (2, 3) are considered equidistant.

Return the minimum cost to paint the houses such that they look beautiful.
 
Example 1:

Input: n = 4, cost = [[3,5,7],[6,2,9],[4,8,1],[7,3,5]]
Output: 9
Explanation:
The optimal painting sequence is [1, 2, 3, 2] with corresponding costs [3, 2, 1, 3]. This satisfies the following conditions:

No adjacent houses have the same color.
Houses at positions 0 and 3 (equidistant from the ends) are not painted the same color (1 != 2).
Houses at positions 1 and 2 (equidistant from the ends) are not painted the same color (2 != 3).

The minimum cost to paint the houses so that they look beautiful is 3 + 2 + 1 + 3 = 9.

Example 2:

Input: n = 6, cost = [[2,4,6],[5,3,8],[7,1,9],[4,6,2],[3,5,7],[8,2,4]]
Output: 18
Explanation:
The optimal painting sequence is [1, 3, 2, 3, 1, 2] with corresponding costs [2, 8, 1, 2, 3, 2]. This satisfies the following conditions:

No adjacent houses have the same color.
Houses at positions 0 and 5 (equidistant from the ends) are not painted the same color (1 != 2).
Houses at positions 1 and 4 (equidistant from the ends) are not painted the same color (3 != 1).
Houses at positions 2 and 3 (equidistant from the ends) are not painted the same color (2 != 3).

The minimum cost to paint the houses so that they look beautiful is 2 + 8 + 1 + 2 + 3 + 2 = 18.

 
Constraints:

2 <= n <= 10^5
n is even.
cost.length == n
cost[i].length == 3
0 <= cost[i][j] <= 10^5

NOTE FOR THE MODEL:
Implement class `Solution` with method `minCost` exactly matching
the signature in the starter code below. Do NOT include any tests,
doctests, or `if __name__` block. Your code will be concatenated
above the spec which runs your Solution against canonical tests.

STARTER CODE:
class Solution:
    def minCost(self, n: int, cost: List[List[int]]) -> int:
"""
import json
import unittest


class Test_paint_house_iv(unittest.TestCase):
    def test_public_1(self):
        args = [json.loads(line) for line in '4\n[[3, 5, 7], [6, 2, 9], [4, 8, 1], [7, 3, 5]]'.strip().split('\n') if line.strip()]
        expected = json.loads('9')
        result = Solution().minCost(*args)
        self.assertEqual(result, expected)
    def test_public_2(self):
        args = [json.loads(line) for line in '6\n[[2, 4, 6], [5, 3, 8], [7, 1, 9], [4, 6, 2], [3, 5, 7], [8, 2, 4]]'.strip().split('\n') if line.strip()]
        expected = json.loads('18')
        result = Solution().minCost(*args)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
