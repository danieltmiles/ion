#!/usr/bin/env python
from flask import Flask, request
import json
import os
from dao.couchdb_data_store import CouchdbDataStore

def get_couch_base_uri():
    couch_addr = "couchdb"
    couch_port = "5984"
    if "COUCHDB_PORT_5984_TCP_ADDR" in os.environ:
        couch_addr = os.environ["COUCHDB_PORT_5984_TCP_ADDR"]
    if "COUCHDB_PORT_5984_TCP_PORT" in os.environ:
        couch_port = os.environ["COUCHDB_PORT_5984_TCP_PORT"]
    print "couch addr: %s" % couch_addr
    print "couch port: %s" % couch_port
    server_base_address="http://%s:%s" % (couch_addr, couch_port)
    return server_base_address

store = CouchdbDataStore(get_couch_base_uri(), db_name="products")
app = Flask(__name__)

@app.route("/v1/status")
def status():
    return "OK\n"

@app.route("/v1/products/<int:product_id>", methods=['GET', 'POST'])
def product_id(product_id):
    if request.method == 'POST':
        data = {}
        try:
            data = json.loads(request.get_data())
        except ValueError:
            return "invalid data, must be JSON-parsable object", 400

        if store.has(product_id):
            store.update(product_id, data)
            return "", 202
        store.create(product_id, data)
        return "", 201
    return json.dumps(store.retrieve(product_id))

@app.route("/v1/products")
def products():
    return json.dumps(store.keys())


if __name__ == "__main__":
    app.run(host='0.0.0.0')


