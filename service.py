#!/usr/bin/env python
from flask import Flask, request
import json
from dao.in_memory_data_store import InMemoryDataStore

store = InMemoryDataStore()
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
