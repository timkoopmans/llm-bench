"""LiveCodeBench 3786 — longest-palindromic-subsequence-after-at-most-k-operations (leetcode, 2025-03-01, medium)

Source: https://leetcode.com/problems/longest_palindromic_subsequence_after_at_most_k_operations/

QUESTION:
You are given a string s and an integer k.
In one operation, you can replace the character at any position with the next or previous letter in the alphabet (wrapping around so that 'a' is after 'z'). For example, replacing 'a' with the next letter results in 'b', and replacing 'a' with the previous letter results in 'z'. Similarly, replacing 'z' with the next letter results in 'a', and replacing 'z' with the previous letter results in 'y'.
Return the length of the longest palindromic subsequence of s that can be obtained after performing at most k operations.
 
Example 1:

Input: s = "abced", k = 2
Output: 3
Explanation:

Replace s[1] with the next letter, and s becomes "acced".
Replace s[4] with the previous letter, and s becomes "accec".

The subsequence "ccc" forms a palindrome of length 3, which is the maximum.

Example 2:

Input: s = "aaazzz", k = 4
Output: 6
Explanation:

Replace s[0] with the previous letter, and s becomes "zaazzz".
Replace s[4] with the next letter, and s becomes "zaazaz".
Replace s[3] with the next letter, and s becomes "zaaaaz".

The entire string forms a palindrome of length 6.

 
Constraints:

1 <= s.length <= 200
1 <= k <= 200
s consists of only lowercase English letters.

NOTE FOR THE MODEL:
Implement class `Solution` with method `longestPalindromicSubsequence` exactly matching
the signature in the starter code below. Do NOT include any tests,
doctests, or `if __name__` block. Your code will be concatenated
above the spec which runs your Solution against canonical tests.

STARTER CODE:
class Solution:
    def longestPalindromicSubsequence(self, s: str, k: int) -> int:
"""
import json
import unittest


class Test_longest_palindromic_subsequence_after_at_most_k_operations(unittest.TestCase):
    def test_public_1(self):
        args = [json.loads(line) for line in '"abced"\n2'.strip().split('\n') if line.strip()]
        expected = json.loads('3')
        result = Solution().longestPalindromicSubsequence(*args)
        self.assertEqual(result, expected)
    def test_public_2(self):
        args = [json.loads(line) for line in '"aaazzz"\n4'.strip().split('\n') if line.strip()]
        expected = json.loads('6')
        result = Solution().longestPalindromicSubsequence(*args)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
