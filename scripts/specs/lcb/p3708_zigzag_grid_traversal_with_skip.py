"""LiveCodeBench 3708 — zigzag-grid-traversal-with-skip (leetcode, 2025-01-11, easy)

Source: https://leetcode.com/problems/zigzag_grid_traversal_with_skip/

QUESTION:
You are given an m x n 2D array grid of positive integers.
Your task is to traverse grid in a zigzag pattern while skipping every alternate cell.
Zigzag pattern traversal is defined as following the below actions:

Start at the top-left cell (0, 0).
Move right within a row until the end of the row is reached.
Drop down to the next row, then traverse left until the beginning of the row is reached.
Continue alternating between right and left traversal until every row has been traversed.

Note that you must skip every alternate cell during the traversal.
Return an array of integers result containing, in order, the value of the cells visited during the zigzag traversal with skips.
 
Example 1:

Input: grid = [[1,2],[3,4]]
Output: [1,4]
Explanation:


Example 2:

Input: grid = [[2,1],[2,1],[2,1]]
Output: [2,1,2]
Explanation:


Example 3:

Input: grid = [[1,2,3],[4,5,6],[7,8,9]]
Output: [1,3,5,7,9]
Explanation:


 
Constraints:

2 <= n == grid.length <= 50
2 <= m == grid[i].length <= 50
1 <= grid[i][j] <= 2500

NOTE FOR THE MODEL:
Implement class `Solution` with method `zigzagTraversal` exactly matching
the signature in the starter code below. Do NOT include any tests,
doctests, or `if __name__` block. Your code will be concatenated
above the spec which runs your Solution against canonical tests.

STARTER CODE:
class Solution:
    def zigzagTraversal(self, grid: List[List[int]]) -> List[int]:
"""
import json
import unittest


class Test_zigzag_grid_traversal_with_skip(unittest.TestCase):
    def test_public_1(self):
        args = [json.loads(line) for line in '[[1, 2], [3, 4]]'.strip().split('\n') if line.strip()]
        expected = json.loads('[1, 4]')
        result = Solution().zigzagTraversal(*args)
        self.assertEqual(result, expected)
    def test_public_2(self):
        args = [json.loads(line) for line in '[[2, 1], [2, 1], [2, 1]]'.strip().split('\n') if line.strip()]
        expected = json.loads('[2, 1, 2]')
        result = Solution().zigzagTraversal(*args)
        self.assertEqual(result, expected)
    def test_public_3(self):
        args = [json.loads(line) for line in '[[1, 2, 3], [4, 5, 6], [7, 8, 9]]'.strip().split('\n') if line.strip()]
        expected = json.loads('[1, 3, 5, 7, 9]')
        result = Solution().zigzagTraversal(*args)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
