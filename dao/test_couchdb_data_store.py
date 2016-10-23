#!/usr/bin/env python

import unittest
from couchdb_data_store import CouchdbDataStore
import httpretty

class TestInMemoryDataStore(unittest.TestCase):

    def setUp(self):
        httpretty.enable()
        httpretty.register_uri(httpretty.GET, "http://pretty/_all_dbs",
                               body='["_replicator","_users"]',
                               content_type="application/json")
        #httpretty.register_uri(httpretty.PUT, "http://pretty/test01", body='{"ok":true}', content_type="application/json")
        httpretty.register_uri(httpretty.PUT, "http://pretty/test01", body='{"ok":true}')
        self.store = CouchdbDataStore("http://pretty", "test01")
    def test_noop(self):
        self.assertEqual(1, 1)

    def test_create(self):
        httpretty.register_uri(httpretty.PUT, "http://pretty/test01/1",
                               body='{"ok":true,"id":"1","rev":"1-ae078ebb7ab2925468c67f92fa301034"}')
        self.store.create(1, {"key": "value"})

    def test_retrieve(self):
        httpretty.register_uri(httpretty.GET, "http://pretty/test01/1",
                body='{"_id":"1","_rev":"1-ae078ebb7ab2925468c67f92fa301034","key": "value"}')
        data_obj = self.store.retrieve(1)
        self.assertEquals({"key": "value"}, data_obj)

    def test_has(self):
        httpretty.register_uri(httpretty.GET, "http://pretty/test01/_all_docs",
                body='{"rows": [{"value": {"rev": "1-ae078ebb7ab2925468c67f92fa301034"}, "id": "1", "key": "1"}, {"value": {"rev": "1-ae078ebb7ab2925468c67f92fa301034"}, "id": "2", "key": "2"}], "total_rows": 2, "offset": 0}')
        self.assertTrue(self.store.has(1))
        self.assertFalse(self.store.has("floozblarg"))


if __name__ == '__main__':
    unittest.main()
