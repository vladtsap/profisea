from flask import Flask, request, jsonify
from pymongo import MongoClient
import boto3

app = Flask(__name__)

client = MongoClient('mongodb', 27017)
db = client.tododb


@app.route('/')
def index():
	return '''<h1>Hello, World!</h1><p>Send GET request to /api with 'id' and 'secret' params.</p>'''


@app.errorhandler(400)
def page_missing_params(e):
	return "<h1>400 Bad Request</h1><p>Expecting 2 params but got 1.</p>", 400


@app.errorhandler(404)
def page_not_found(e):
	return "<h1>404 Not Found</h1><p>The resource could not be found.</p>", 404


@app.errorhandler(502)
def page_invalid_params(e, info):
	return "<h1>502 Bad Gateway</h1><p>{}</p>".format(info), 502


@app.route('/api', methods=['GET'])
def api():
	query_parameters = request.args

	key_id = query_parameters.get('id')
	secret_key = query_parameters.get('secret')

	if key_id and secret_key:
		try:
			client = boto3.client(
				'ec2',
				aws_access_key_id=key_id,
				aws_secret_access_key=secret_key,
				region_name='eu-central-1'
			)

			results = client.describe_vpcs()
			return jsonify(results)

		except Exception as e:
			return page_invalid_params(502, str(e))

	elif key_id or secret_key:
		return page_missing_params(400)

	else:
		return page_not_found(404)


if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
