#!/usr/bin/env python
from flask import Flask, request
app = Flask(__name__)

@app.route("/v1/status")
def status():
    return "OK\n"

@app.route("/v1/products/<int:product_id>", methods=['GET', 'POST'])
def product_id(product_id):
    if request.method == 'POST':
        print "request data: " + request.get_data()
        return "post\n"
    return "get\n"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
