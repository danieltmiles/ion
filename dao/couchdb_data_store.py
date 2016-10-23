#!/usr/bin/env python
import json
import pybreaker
import requests
from in_memory_data_store import InMemoryDataStore

class ReplayListener(pybreaker.CircuitBreakerListener):
    def __init__(self, couchDataStore):
        self.couchDataStore = couchDataStore

    def state_change(self, cb, old_state, new_state):
        if new_state.name == "open":
            for k in self.couchDataStore.cache.keys():
                self.couchDataStore.create(k, self.couchDataStore.cache.retrieve(k))
            self.couchDataStore.cache = InMemoryDataStore()

breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=3)


class CouchdbDataStore:

    def __init__(self, server_base_url, db_name, create=True):
        self.server_base_url = server_base_url
        self.db_name = db_name
        self.cache = InMemoryDataStore()
        if create:
            resp = requests.get(self.server_base_url + "/_all_dbs")
            if resp.status_code != 200:
                raise Exception("unable to connect to couchdb, status code %s" % resp.status_code)
            databases = json.loads(resp.text)
            if self.db_name not in databases:
                uri = "%s/%s" % (self.server_base_url, self.db_name)
                requests.put(uri)
        breaker.add_listener(ReplayListener(self))

    def create(self, obj_id, data):
        try:
            return self._create(obj_id, data)
        except pybreaker.CircuitBreakerError:
            return self._create_fallback(obj_id, data)

    @breaker
    def _create(self, obj_id, data):
        uri = "%s/%s/%s" % (self.server_base_url, self.db_name, obj_id)
        resp = requests.put(uri, data=json.dumps(data))
        if resp.status_code != 200:
            raise Exception("unable to write to database (%s): %s" % (resp.status_code, resp.text))

    def _create_fallback(self, obj_id, data):
        self.cache.create(obj_id, data)

    @breaker
    def retrieve(self, obj_id):
        try:
            return self._retrieve(obj_id)
        except pybreaker.CircuitBreakerError:
            return self._retrieve_fallback(obj_id)

    def _retrieve(self, obj_id):
        uri = "%s/%s/%s" % (self.server_base_url, self.db_name, obj_id)
        resp = requests.get(uri)
        if resp.status_code != 200:
            raise Exception("unable to fetch object id %s from the database (%s) %s" %(obj_id, resp.status_code, resp.text))
        couch_data = json.loads(resp.text)
        del couch_data["_id"]
        del couch_data["_rev"]
        return couch_data

    def _retrieve_fallback(self, obj_id):
        return self.cache.retrieve(obj_id)


    #def update(self, obj_id, data):
    #    if obj_id in self._store:
    #        self._store[obj_id].update(data)

    #def delete(self, obj_id):
    #    if obj_id in self._store:
    #        del self._store[obj_id]

    def has(self, obj_id):
        keys = self.keys()
        return "%s" % obj_id in keys


    def keys(self):
        uri = "%s/%s/_all_docs" % (self.server_base_url, self.db_name)
        resp = requests.get(uri)
        if resp.status_code != 200:
            raise Exception("unable to fetch _all_docs from couchdb (%s) %s" % (resp.status_code, resp.text))
        couch_data = json.loads(resp.text)
        keys = [x["key"] for x in couch_data["rows"]]
        return keys
