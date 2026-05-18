"""LiveCodeBench 3753 — maximum-difference-between-even-and-odd-frequency-i (leetcode, 2025-02-01, easy)

Source: https://leetcode.com/problems/maximum_difference_between_even_and_odd_frequency_i/

QUESTION:
You are given a string s consisting of lowercase English letters. Your task is to find the maximum difference between the frequency of two characters in the string such that:

One of the characters has an even frequency in the string.
The other character has an odd frequency in the string.

Return the maximum difference, calculated as the frequency of the character with an odd frequency minus the frequency of the character with an even frequency.
 
Example 1:

Input: s = "aaaaabbc"
Output: 3
Explanation:

The character 'a' has an odd frequency of 5, and 'b' has an even frequency of 2.
The maximum difference is 5 - 2 = 3.


Example 2:

Input: s = "abcabcab"
Output: 1
Explanation:

The character 'a' has an odd frequency of 3, and 'c' has an even frequency of 2.
The maximum difference is 3 - 2 = 1.


 
Constraints:

3 <= s.length <= 100
s consists only of lowercase English letters.
s contains at least one character with an odd frequency and one with an even frequency.

NOTE FOR THE MODEL:
Implement class `Solution` with method `maxDifference` exactly matching
the signature in the starter code below. Do NOT include any tests,
doctests, or `if __name__` block. Your code will be concatenated
above the spec which runs your Solution against canonical tests.

STARTER CODE:
class Solution:
    def maxDifference(self, s: str) -> int:
"""
import json
import unittest


class Test_maximum_difference_between_even_and_odd_frequency_i(unittest.TestCase):
    def test_public_1(self):
        args = [json.loads(line) for line in '"aaaaabbc"'.strip().split('\n') if line.strip()]
        expected = json.loads('3')
        result = Solution().maxDifference(*args)
        self.assertEqual(result, expected)
    def test_public_2(self):
        args = [json.loads(line) for line in '"abcabcab"'.strip().split('\n') if line.strip()]
        expected = json.loads('1')
        result = Solution().maxDifference(*args)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
