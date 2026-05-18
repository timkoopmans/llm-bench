"""LiveCodeBench 3709 — find-special-substring-of-length-k (leetcode, 2025-02-15, easy)

Source: https://leetcode.com/problems/find_special_substring_of_length_k/

QUESTION:
You are given a string s and an integer k.
Determine if there exists a substring of length exactly k in s that satisfies the following conditions:

The substring consists of only one distinct character (e.g., "aaa" or "bbb").
If there is a character immediately before the substring, it must be different from the character in the substring.
If there is a character immediately after the substring, it must also be different from the character in the substring.

Return true if such a substring exists. Otherwise, return false.
 
Example 1:

Input: s = "aaabaaa", k = 3
Output: true
Explanation:
The substring s[4..6] == "aaa" satisfies the conditions.

It has a length of 3.
All characters are the same.
The character before "aaa" is 'b', which is different from 'a'.
There is no character after "aaa".


Example 2:

Input: s = "abc", k = 2
Output: false
Explanation:
There is no substring of length 2 that consists of one distinct character and satisfies the conditions.

 
Constraints:

1 <= k <= s.length <= 100
s consists of lowercase English letters only.

NOTE FOR THE MODEL:
Implement class `Solution` with method `hasSpecialSubstring` exactly matching
the signature in the starter code below. Do NOT include any tests,
doctests, or `if __name__` block. Your code will be concatenated
above the spec which runs your Solution against canonical tests.

STARTER CODE:
class Solution:
    def hasSpecialSubstring(self, s: str, k: int) -> bool:
"""
import json
import unittest


class Test_find_special_substring_of_length_k(unittest.TestCase):
    def test_public_1(self):
        args = [json.loads(line) for line in '"aaabaaa"\n3'.strip().split('\n') if line.strip()]
        expected = json.loads('true')
        result = Solution().hasSpecialSubstring(*args)
        self.assertEqual(result, expected)
    def test_public_2(self):
        args = [json.loads(line) for line in '"abc"\n2'.strip().split('\n') if line.strip()]
        expected = json.loads('false')
        result = Solution().hasSpecialSubstring(*args)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
