"""LiveCodeBench 3791 — fruits-into-baskets-iii (leetcode, 2025-03-08, medium)

Source: https://leetcode.com/problems/fruits_into_baskets_iii/

QUESTION:
You are given two arrays of integers, fruits and baskets, each of length n, where fruits[i] represents the quantity of the i^th type of fruit, and baskets[j] represents the capacity of the j^th basket.
From left to right, place the fruits according to these rules:

Each fruit type must be placed in the leftmost available basket with a capacity greater than or equal to the quantity of that fruit type.
Each basket can hold only one type of fruit.
If a fruit type cannot be placed in any basket, it remains unplaced.

Return the number of fruit types that remain unplaced after all possible allocations are made.
 
Example 1:

Input: fruits = [4,2,5], baskets = [3,5,4]
Output: 1
Explanation:

fruits[0] = 4 is placed in baskets[1] = 5.
fruits[1] = 2 is placed in baskets[0] = 3.
fruits[2] = 5 cannot be placed in baskets[2] = 4.

Since one fruit type remains unplaced, we return 1.

Example 2:

Input: fruits = [3,6,1], baskets = [6,4,7]
Output: 0
Explanation:

fruits[0] = 3 is placed in baskets[0] = 6.
fruits[1] = 6 cannot be placed in baskets[1] = 4 (insufficient capacity) but can be placed in the next available basket, baskets[2] = 7.
fruits[2] = 1 is placed in baskets[1] = 4.

Since all fruits are successfully placed, we return 0.

 
Constraints:

n == fruits.length == baskets.length
1 <= n <= 10^5
1 <= fruits[i], baskets[i] <= 10^9

NOTE FOR THE MODEL:
Implement class `Solution` with method `numOfUnplacedFruits` exactly matching
the signature in the starter code below. Do NOT include any tests,
doctests, or `if __name__` block. Your code will be concatenated
above the spec which runs your Solution against canonical tests.

STARTER CODE:
class Solution:
    def numOfUnplacedFruits(self, fruits: List[int], baskets: List[int]) -> int:
"""
import json
import unittest


class Test_fruits_into_baskets_iii(unittest.TestCase):
    def test_public_1(self):
        args = [json.loads(line) for line in '[4, 2, 5]\n[3, 5, 4]'.strip().split('\n') if line.strip()]
        expected = json.loads('1')
        result = Solution().numOfUnplacedFruits(*args)
        self.assertEqual(result, expected)
    def test_public_2(self):
        args = [json.loads(line) for line in '[3, 6, 1]\n[6, 4, 7]'.strip().split('\n') if line.strip()]
        expected = json.loads('0')
        result = Solution().numOfUnplacedFruits(*args)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
