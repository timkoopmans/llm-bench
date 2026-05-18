"""Canonical spec for LRUCache. Run as: model_impl + this file."""
import unittest


class TestLRUCache(unittest.TestCase):
    def test_basic_hit(self):
        c = LRUCache(2)
        c.put(1, 100)
        self.assertEqual(c.get(1), 100)

    def test_miss_returns_minus_one(self):
        c = LRUCache(2)
        self.assertEqual(c.get(99), -1)

    def test_lru_eviction(self):
        c = LRUCache(2)
        c.put(1, "a"); c.put(2, "b"); c.put(3, "c")
        self.assertEqual(c.get(1), -1)
        self.assertEqual(c.get(2), "b")
        self.assertEqual(c.get(3), "c")

    def test_get_refreshes_recency(self):
        c = LRUCache(2)
        c.put(1, "a"); c.put(2, "b")
        c.get(1)               # 1 now MRU
        c.put(3, "c")          # should evict 2, not 1
        self.assertEqual(c.get(1), "a")
        self.assertEqual(c.get(2), -1)
        self.assertEqual(c.get(3), "c")

    def test_put_existing_updates_value(self):
        c = LRUCache(2)
        c.put(1, "old")
        c.put(1, "new")
        self.assertEqual(c.get(1), "new")

    def test_put_existing_refreshes_recency(self):
        c = LRUCache(2)
        c.put(1, "a"); c.put(2, "b")
        c.put(1, "a2")         # 1 now MRU
        c.put(3, "c")          # should evict 2
        self.assertEqual(c.get(2), -1)
        self.assertEqual(c.get(1), "a2")
        self.assertEqual(c.get(3), "c")

    def test_capacity_1(self):
        c = LRUCache(1)
        c.put(1, "a"); c.put(2, "b")
        self.assertEqual(c.get(1), -1)
        self.assertEqual(c.get(2), "b")

    def test_capacity_0_never_stores(self):
        c = LRUCache(0)
        c.put(1, "a"); c.put(2, "b")
        self.assertEqual(c.get(1), -1)
        self.assertEqual(c.get(2), -1)

    def test_mixed_sequence(self):
        c = LRUCache(3)
        c.put(1, 1); c.put(2, 2); c.put(3, 3)
        self.assertEqual(c.get(2), 2)         # 2 is MRU
        c.put(4, 4)                            # evicts 1 (LRU)
        self.assertEqual(c.get(1), -1)
        self.assertEqual(c.get(3), 3)
        self.assertEqual(c.get(4), 4)

    def test_overwrite_does_not_grow_size(self):
        c = LRUCache(2)
        c.put(1, "a"); c.put(2, "b")
        c.put(1, "a2")                          # update, not insert
        c.put(3, "c")                           # evicts 2
        self.assertEqual(c.get(1), "a2")
        self.assertEqual(c.get(2), -1)
        self.assertEqual(c.get(3), "c")


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
