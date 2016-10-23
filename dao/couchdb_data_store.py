#!/usr/bin/env python
import json
import requests

class CouchdbDataStore:

    def __init__(self, server_base_url, db_name, create=True):
        self.server_base_url = server_base_url
        self.db_name = db_name
        if create:
            resp = requests.get(self.server_base_url + "/_all_dbs")
            if resp.status_code != 200:
                raise Exception("unable to connect to couchdb, status code %s" % resp.status_code)
            databases = json.loads(resp.text)
            if self.db_name not in databases:
                uri = "%s/%s" % (self.server_base_url, self.db_name)
                requests.put(uri)

    def create(self, obj_id, data):
        uri = "%s/%s/%s" % (self.server_base_url, self.db_name, obj_id)
        resp = requests.put(uri, data=json.dumps(data))
        if resp.status_code != 200:
            raise Exception("unable to write to database (%s): %s" % (resp.status_code, resp.text))

    def retrieve(self, obj_id):
        uri = "%s/%s/%s" % (self.server_base_url, self.db_name, obj_id)
        resp = requests.get(uri)
        if resp.status_code != 200:
            raise Exception("unable to fetch object id %s from the database (%s) %s" %(obj_id, resp.status_code, resp.text))
        couch_data = json.loads(resp.text)
        del couch_data["_id"]
        del couch_data["_rev"]
        return couch_data


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
