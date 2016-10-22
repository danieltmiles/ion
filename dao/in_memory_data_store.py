#!/usr/bin/env python

class InMemoryDataStore:
    def __init__(self):
        self._store = {}

    def create(self, obj_id, data):
        self._store[obj_id] = data

    def retrieve(self, obj_id):
        if obj_id in self._store:
            return self._store[obj_id]
        return None

    def update(self, obj_id, data):
        if obj_id in self._store:
            self._store[obj_id].update(data)

    def delete(self, obj_id):
        if obj_id in self._store:
            del self._store[obj_id]
