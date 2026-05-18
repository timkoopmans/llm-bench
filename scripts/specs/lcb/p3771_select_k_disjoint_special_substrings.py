"""LiveCodeBench 3771 — select-k-disjoint-special-substrings (leetcode, 2025-02-15, medium)

Source: https://leetcode.com/problems/select_k_disjoint_special_substrings/

QUESTION:
Given a string s of length n and an integer k, determine whether it is possible to select k disjoint special substrings.
A special substring is a substring where:

Any character present inside the substring should not appear outside it in the string.
The substring is not the entire string s.

Note that all k substrings must be disjoint, meaning they cannot overlap.
Return true if it is possible to select k such disjoint special substrings; otherwise, return false.
 
Example 1:

Input: s = "abcdbaefab", k = 2
Output: true
Explanation:

We can select two disjoint special substrings: "cd" and "ef".
"cd" contains the characters 'c' and 'd', which do not appear elsewhere in s.
"ef" contains the characters 'e' and 'f', which do not appear elsewhere in s.


Example 2:

Input: s = "cdefdc", k = 3
Output: false
Explanation:
There can be at most 2 disjoint special substrings: "e" and "f". Since k = 3, the output is false.

Example 3:

Input: s = "abeabe", k = 0
Output: true

 
Constraints:

2 <= n == s.length <= 5 * 10^4
0 <= k <= 26
s consists only of lowercase English letters.

NOTE FOR THE MODEL:
Implement class `Solution` with method `maxSubstringLength` exactly matching
the signature in the starter code below. Do NOT include any tests,
doctests, or `if __name__` block. Your code will be concatenated
above the spec which runs your Solution against canonical tests.

STARTER CODE:
class Solution:
    def maxSubstringLength(self, s: str, k: int) -> bool:
"""
import json
import unittest


class Test_select_k_disjoint_special_substrings(unittest.TestCase):
    def test_public_1(self):
        args = [json.loads(line) for line in '"abcdbaefab"\n2'.strip().split('\n') if line.strip()]
        expected = json.loads('true')
        result = Solution().maxSubstringLength(*args)
        self.assertEqual(result, expected)
    def test_public_2(self):
        args = [json.loads(line) for line in '"cdefdc"\n3'.strip().split('\n') if line.strip()]
        expected = json.loads('false')
        result = Solution().maxSubstringLength(*args)
        self.assertEqual(result, expected)
    def test_public_3(self):
        args = [json.loads(line) for line in '"abeabe"\n0'.strip().split('\n') if line.strip()]
        expected = json.loads('true')
        result = Solution().maxSubstringLength(*args)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
