"""LiveCodeBench 3817 — maximum-containers-on-a-ship (leetcode, 2025-03-22, easy)

Source: https://leetcode.com/problems/maximum_containers_on_a_ship/

QUESTION:
You are given a positive integer n representing an n x n cargo deck on a ship. Each cell on the deck can hold one container with a weight of exactly w.
However, the total weight of all containers, if loaded onto the deck, must not exceed the ship's maximum weight capacity, maxWeight.
Return the maximum number of containers that can be loaded onto the ship.
 
Example 1:

Input: n = 2, w = 3, maxWeight = 15
Output: 4
Explanation: 
The deck has 4 cells, and each container weighs 3. The total weight of loading all containers is 12, which does not exceed maxWeight.

Example 2:

Input: n = 3, w = 5, maxWeight = 20
Output: 4
Explanation: 
The deck has 9 cells, and each container weighs 5. The maximum number of containers that can be loaded without exceeding maxWeight is 4.

 
Constraints:

1 <= n <= 1000
1 <= w <= 1000
1 <= maxWeight <= 10^9

NOTE FOR THE MODEL:
Implement class `Solution` with method `maxContainers` exactly matching
the signature in the starter code below. Do NOT include any tests,
doctests, or `if __name__` block. Your code will be concatenated
above the spec which runs your Solution against canonical tests.

STARTER CODE:
class Solution:
    def maxContainers(self, n: int, w: int, maxWeight: int) -> int:
"""
import json
import unittest


class Test_maximum_containers_on_a_ship(unittest.TestCase):
    def test_public_1(self):
        args = [json.loads(line) for line in '2\n3\n15'.strip().split('\n') if line.strip()]
        expected = json.loads('4')
        result = Solution().maxContainers(*args)
        self.assertEqual(result, expected)
    def test_public_2(self):
        args = [json.loads(line) for line in '3\n5\n20'.strip().split('\n') if line.strip()]
        expected = json.loads('4')
        result = Solution().maxContainers(*args)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
