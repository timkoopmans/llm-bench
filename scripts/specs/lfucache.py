"""Canonical spec for LFUCache (LeetCode 460 semantics).

Run as: model_impl + this file.

Semantics:
- LFUCache(capacity): integer capacity, 0 is valid (never stores).
- get(key) -> value, or -1 if missing. Increments frequency.
- put(key, value): if key exists, update value AND increment frequency.
  If new and at capacity, evict least-frequently-used; ties broken by
  least-recently-used (the one that was touched least recently).
"""
import unittest


class TestLFUCache(unittest.TestCase):
    # ---- basic API ----
    def test_basic_hit(self):
        c = LFUCache(2)
        c.put(1, 100)
        self.assertEqual(c.get(1), 100)

    def test_miss_returns_minus_one(self):
        c = LFUCache(2)
        self.assertEqual(c.get(99), -1)

    def test_capacity_0_never_stores(self):
        c = LFUCache(0)
        c.put(1, "a"); c.put(2, "b")
        self.assertEqual(c.get(1), -1)
        self.assertEqual(c.get(2), -1)

    def test_capacity_1_evicts_on_second_distinct_put(self):
        c = LFUCache(1)
        c.put(1, "a"); c.put(2, "b")
        self.assertEqual(c.get(1), -1)
        self.assertEqual(c.get(2), "b")

    # ---- LFU eviction ----
    def test_evicts_lfu_when_full(self):
        c = LFUCache(2)
        c.put(1, "a"); c.put(2, "b")
        c.get(1)              # freq: 1→2, 2→1
        c.put(3, "c")          # evicts 2 (lowest freq)
        self.assertEqual(c.get(2), -1)
        self.assertEqual(c.get(1), "a")
        self.assertEqual(c.get(3), "c")

    def test_lfu_tie_broken_by_lru(self):
        c = LFUCache(2)
        c.put(1, "a")          # freq 1
        c.put(2, "b")          # freq 1; 2 is more recently used than 1
        c.put(3, "c")          # both 1 and 2 at freq 1 → evict 1 (LRU)
        self.assertEqual(c.get(1), -1)
        self.assertEqual(c.get(2), "b")
        self.assertEqual(c.get(3), "c")

    def test_get_bumps_frequency_avoids_eviction(self):
        c = LFUCache(2)
        c.put(1, "a"); c.put(2, "b")
        # bump 1 several times so it survives next eviction
        for _ in range(3):
            c.get(1)
        c.put(3, "c")          # evicts 2 (freq 1 < 1's freq 4)
        self.assertEqual(c.get(2), -1)
        self.assertEqual(c.get(1), "a")
        self.assertEqual(c.get(3), "c")

    # ---- put-on-existing semantics ----
    def test_put_existing_updates_value(self):
        c = LFUCache(2)
        c.put(1, "old")
        c.put(1, "new")
        self.assertEqual(c.get(1), "new")

    def test_put_existing_bumps_frequency(self):
        c = LFUCache(2)
        c.put(1, "a"); c.put(2, "b")
        c.put(1, "a2")         # freq 1→2, still in cache
        c.put(3, "c")          # evicts 2 (freq 1) not 1 (freq 2)
        self.assertEqual(c.get(2), -1)
        self.assertEqual(c.get(1), "a2")
        self.assertEqual(c.get(3), "c")

    # ---- recency within same freq ----
    def test_recency_only_matters_within_same_freq(self):
        c = LFUCache(3)
        c.put(1, "a"); c.put(2, "b"); c.put(3, "c")  # all freq 1
        c.get(2); c.get(3)                            # 2,3 → freq 2; 1 stays at 1
        c.put(4, "d")                                  # evicts 1 (lowest freq)
        self.assertEqual(c.get(1), -1)
        self.assertEqual(c.get(2), "b")
        self.assertEqual(c.get(3), "c")
        self.assertEqual(c.get(4), "d")

    # ---- canonical LeetCode 460 sequence ----
    def test_leetcode_460_sequence(self):
        c = LFUCache(2)
        c.put(1, 1)
        c.put(2, 2)
        self.assertEqual(c.get(1), 1)   # freq 1=2, 2=1
        c.put(3, 3)                      # evicts 2 (lowest freq)
        self.assertEqual(c.get(2), -1)
        self.assertEqual(c.get(3), 3)   # freq 3=2
        c.put(4, 4)                      # freq 1=2, 3=2 → evict 1 (LRU among freq 2)
        self.assertEqual(c.get(1), -1)
        self.assertEqual(c.get(3), 3)
        self.assertEqual(c.get(4), 4)

    def test_high_freq_key_survives_many_evictions(self):
        c = LFUCache(2)
        c.put(1, "hot")
        for _ in range(10):
            c.get(1)                     # freq 1 = 11
        c.put(2, "a"); c.put(3, "b")    # 2 evicted (LFU)
        self.assertEqual(c.get(2), -1)
        self.assertEqual(c.get(1), "hot")
        self.assertEqual(c.get(3), "b")

    def test_multiple_evictions(self):
        c = LFUCache(2)
        c.put(1, "a"); c.put(2, "b")
        c.put(3, "c")                    # evict 1 or 2 (both freq 1, LRU=1)
        self.assertEqual(c.get(1), -1)
        c.put(4, "d")                    # evict 2 (freq 1, LRU)
        self.assertEqual(c.get(2), -1)
        self.assertEqual(c.get(3), "c")
        self.assertEqual(c.get(4), "d")

    def test_size_never_exceeds_capacity(self):
        c = LFUCache(2)
        for k in range(20):
            c.put(k, k * 10)
        live = sum(1 for k in range(20) if c.get(k) != -1)
        self.assertLessEqual(live, 2)

    def test_overwrite_does_not_grow_size(self):
        c = LFUCache(2)
        c.put(1, "a"); c.put(2, "b")
        c.put(1, "a2")                   # update only
        # Both should still be retrievable; capacity not exceeded
        self.assertEqual(c.get(1), "a2")
        self.assertEqual(c.get(2), "b")


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
