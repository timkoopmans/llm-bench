"""LiveCodeBench 3720 — minimize-the-maximum-edge-weight-of-graph (leetcode, 2025-01-11, medium)

Source: https://leetcode.com/problems/minimize_the_maximum_edge_weight_of_graph/

QUESTION:
You are given two integers, n and threshold, as well as a directed weighted graph of n nodes numbered from 0 to n - 1. The graph is represented by a 2D integer array edges, where edges[i] = [A_i, B_i, W_i] indicates that there is an edge going from node A_i to node B_i with weight W_i.
You have to remove some edges from this graph (possibly none), so that it satisfies the following conditions:

Node 0 must be reachable from all other nodes.
The maximum edge weight in the resulting graph is minimized.
Each node has at most threshold outgoing edges.

Return the minimum possible value of the maximum edge weight after removing the necessary edges. If it is impossible for all conditions to be satisfied, return -1.
 
Example 1:

Input: n = 5, edges = [[1,0,1],[2,0,2],[3,0,1],[4,3,1],[2,1,1]], threshold = 2
Output: 1
Explanation:

Remove the edge 2 -> 0. The maximum weight among the remaining edges is 1.

Example 2:

Input: n = 5, edges = [[0,1,1],[0,2,2],[0,3,1],[0,4,1],[1,2,1],[1,4,1]], threshold = 1
Output: -1
Explanation: 
It is impossible to reach node 0 from node 2.

Example 3:

Input: n = 5, edges = [[1,2,1],[1,3,3],[1,4,5],[2,3,2],[3,4,2],[4,0,1]], threshold = 1
Output: 2
Explanation: 

Remove the edges 1 -> 3 and 1 -> 4. The maximum weight among the remaining edges is 2.

Example 4:

Input: n = 5, edges = [[1,2,1],[1,3,3],[1,4,5],[2,3,2],[4,0,1]], threshold = 1
Output: -1

 
Constraints:

2 <= n <= 10^5
1 <= threshold <= n - 1
1 <= edges.length <= min(10^5, n * (n - 1) / 2).
edges[i].length == 3
0 <= A_i, B_i < n
A_i != B_i
1 <= W_i <= 10^6
There may be multiple edges between a pair of nodes, but they must have unique weights.

NOTE FOR THE MODEL:
Implement class `Solution` with method `minMaxWeight` exactly matching
the signature in the starter code below. Do NOT include any tests,
doctests, or `if __name__` block. Your code will be concatenated
above the spec which runs your Solution against canonical tests.

STARTER CODE:
class Solution:
    def minMaxWeight(self, n: int, edges: List[List[int]], threshold: int) -> int:
"""
import json
import unittest


class Test_minimize_the_maximum_edge_weight_of_graph(unittest.TestCase):
    def test_public_1(self):
        args = [json.loads(line) for line in '5\n[[1, 0, 1], [2, 0, 2], [3, 0, 1], [4, 3, 1], [2, 1, 1]]\n2'.strip().split('\n') if line.strip()]
        expected = json.loads('1')
        result = Solution().minMaxWeight(*args)
        self.assertEqual(result, expected)
    def test_public_2(self):
        args = [json.loads(line) for line in '5\n[[0, 1, 1], [0, 2, 2], [0, 3, 1], [0, 4, 1], [1, 2, 1], [1, 4, 1]]\n1'.strip().split('\n') if line.strip()]
        expected = json.loads('-1')
        result = Solution().minMaxWeight(*args)
        self.assertEqual(result, expected)
    def test_public_3(self):
        args = [json.loads(line) for line in '5\n[[1, 2, 1], [1, 3, 3], [1, 4, 5], [2, 3, 2], [3, 4, 2], [4, 0, 1]]\n1'.strip().split('\n') if line.strip()]
        expected = json.loads('2')
        result = Solution().minMaxWeight(*args)
        self.assertEqual(result, expected)
    def test_public_4(self):
        args = [json.loads(line) for line in '5\n[[1, 2, 1], [1, 3, 3], [1, 4, 5], [2, 3, 2], [4, 0, 1]]\n1'.strip().split('\n') if line.strip()]
        expected = json.loads('-1')
        result = Solution().minMaxWeight(*args)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
