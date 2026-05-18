"""LiveCodeBench 3754 — maximum-manhattan-distance-after-k-changes (leetcode, 2025-02-01, medium)

Source: https://leetcode.com/problems/maximum_manhattan_distance_after_k_changes/

QUESTION:
You are given a string s consisting of the characters 'N', 'S', 'E', and 'W', where s[i] indicates movements in an infinite grid:

'N' : Move north by 1 unit.
'S' : Move south by 1 unit.
'E' : Move east by 1 unit.
'W' : Move west by 1 unit.

Initially, you are at the origin (0, 0). You can change at most k characters to any of the four directions.
Find the maximum Manhattan distance from the origin that can be achieved at any time while performing the movements in order.
The Manhattan Distance between two cells (x_i, y_i) and (x_j, y_j) is |x_i - x_j| + |y_i - y_j|.
 
Example 1:

Input: s = "NWSE", k = 1
Output: 3
Explanation:
Change s[2] from 'S' to 'N'. The string s becomes "NWNE".



Movement
Position (x, y)
Manhattan Distance
Maximum




s[0] == 'N'
(0, 1)
0 + 1 = 1
1


s[1] == 'W'
(-1, 1)
1 + 1 = 2
2


s[2] == 'N'
(-1, 2)
1 + 2 = 3
3


s[3] == 'E'
(0, 2)
0 + 2 = 2
3



The maximum Manhattan distance from the origin that can be achieved is 3. Hence, 3 is the output.

Example 2:

Input: s = "NSWWEW", k = 3
Output: 6
Explanation:
Change s[1] from 'S' to 'N', and s[4] from 'E' to 'W'. The string s becomes "NNWWWW".
The maximum Manhattan distance from the origin that can be achieved is 6. Hence, 6 is the output.

 
Constraints:

1 <= s.length <= 10^5
0 <= k <= s.length
s consists of only 'N', 'S', 'E', and 'W'.

NOTE FOR THE MODEL:
Implement class `Solution` with method `maxDistance` exactly matching
the signature in the starter code below. Do NOT include any tests,
doctests, or `if __name__` block. Your code will be concatenated
above the spec which runs your Solution against canonical tests.

STARTER CODE:
class Solution:
    def maxDistance(self, s: str, k: int) -> int:
"""
import json
import unittest


class Test_maximum_manhattan_distance_after_k_changes(unittest.TestCase):
    def test_public_1(self):
        args = [json.loads(line) for line in '"NWSE"\n1'.strip().split('\n') if line.strip()]
        expected = json.loads('3')
        result = Solution().maxDistance(*args)
        self.assertEqual(result, expected)
    def test_public_2(self):
        args = [json.loads(line) for line in '"NSWWEW"\n3'.strip().split('\n') if line.strip()]
        expected = json.loads('6')
        result = Solution().maxDistance(*args)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
