import os
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb', 27017)
db = client.tododb


@app.route('/')
def index():
	return '''<h1>Header 1</h1>
<p>A paragraph with some text inside.</p>'''


if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
