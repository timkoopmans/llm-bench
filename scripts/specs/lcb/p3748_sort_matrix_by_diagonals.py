"""LiveCodeBench 3748 — sort-matrix-by-diagonals (leetcode, 2025-02-08, medium)

Source: https://leetcode.com/problems/sort_matrix_by_diagonals/

QUESTION:
You are given an n x n square matrix of integers grid. Return the matrix such that:

The diagonals in the bottom-left triangle (including the middle diagonal) are sorted in non-increasing order.
The diagonals in the top-right triangle are sorted in non-decreasing order.

 
Example 1:

Input: grid = [[1,7,3],[9,8,2],[4,5,6]]
Output: [[8,2,3],[9,6,7],[4,5,1]]
Explanation:

The diagonals with a black arrow (bottom-left triangle) should be sorted in non-increasing order:

[1, 8, 6] becomes [8, 6, 1].
[9, 5] and [4] remain unchanged.

The diagonals with a blue arrow (top-right triangle) should be sorted in non-decreasing order:

[7, 2] becomes [2, 7].
[3] remains unchanged.


Example 2:

Input: grid = [[0,1],[1,2]]
Output: [[2,1],[1,0]]
Explanation:

The diagonals with a black arrow must be non-increasing, so [0, 2] is changed to [2, 0]. The other diagonals are already in the correct order.

Example 3:

Input: grid = [[1]]
Output: [[1]]
Explanation:
Diagonals with exactly one element are already in order, so no changes are needed.

 
Constraints:

grid.length == grid[i].length == n
1 <= n <= 10
-10^5 <= grid[i][j] <= 10^5

NOTE FOR THE MODEL:
Implement class `Solution` with method `sortMatrix` exactly matching
the signature in the starter code below. Do NOT include any tests,
doctests, or `if __name__` block. Your code will be concatenated
above the spec which runs your Solution against canonical tests.

STARTER CODE:
class Solution:
    def sortMatrix(self, grid: List[List[int]]) -> List[List[int]]:
"""
import json
import unittest


class Test_sort_matrix_by_diagonals(unittest.TestCase):
    def test_public_1(self):
        args = [json.loads(line) for line in '[[1, 7, 3], [9, 8, 2], [4, 5, 6]]'.strip().split('\n') if line.strip()]
        expected = json.loads('[[8, 2, 3], [9, 6, 7], [4, 5, 1]]')
        result = Solution().sortMatrix(*args)
        self.assertEqual(result, expected)
    def test_public_2(self):
        args = [json.loads(line) for line in '[[0, 1], [1, 2]]'.strip().split('\n') if line.strip()]
        expected = json.loads('[[2, 1], [1, 0]]')
        result = Solution().sortMatrix(*args)
        self.assertEqual(result, expected)
    def test_public_3(self):
        args = [json.loads(line) for line in '[[1]]'.strip().split('\n') if line.strip()]
        expected = json.loads('[[1]]')
        result = Solution().sortMatrix(*args)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
