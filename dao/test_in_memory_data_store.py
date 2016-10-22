#!/usr/bin/env python

import unittest
from in_memory_data_store import InMemoryDataStore

class TestInMemoryDataStore(unittest.TestCase):

    def setUp(self):
        self.store = InMemoryDataStore()

    def test_create(self):
        self.store.create(1, {"key": "value"})
        self.assertEqual(self.store._store[1], {"key": "value"})

    def test_retrieve(self):
        self.store.create(1, {"key": "value"})
        retrieved = self.store.retrieve(1)
        self.assertEqual(retrieved, {"key": "value"})

    def test_update(self):
        self.store.create(1, {"key": "value"})
        self.store.update(1, {"second_key": "second_value"})
        self.assertEquals(len(self.store._store.keys()), 1)
        self.assertEquals(len(self.store._store[1]), 2)
        self.assertEquals(self.store._store[1]["key"], "value")
        self.assertEquals(self.store._store[1]["second_key"], "second_value")

    def test_delete(self):
        self.store.create(1, {"key": "value"})
        self.assertEqual(self.store._store[1], {"key": "value"})
        self.store.delete(1)
        self.assertEqual(self.store._store, {})


if __name__ == '__main__':
    unittest.main()
