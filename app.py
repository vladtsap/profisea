from flask import Flask, request, jsonify
import pymongo
import boto3

app = Flask(__name__)

# db_client = pymongo.MongoClient('mongo', 27017)  # for running in Docker
db_client = pymongo.MongoClient('mongodb://localhost:27017/')  # for running in PyCharm


@app.route('/')
def index():
	"""Start page with hints"""
	return '''<h1>Hello, World!</h1><p>Send GET request to /api with 'id' and 'secret' params.</p>'''


@app.errorhandler(400)
def page_missing_params(e):
	"""Error page when missing parameter"""
	return "<h1>400 Bad Request</h1><p>Expecting 2 params but got 1.</p>", 400


@app.errorhandler(404)
def page_not_found(e):
	"""Error when page is not exist"""
	return "<h1>404 Not Found</h1><p>The resource could not be found.</p>", 404


@app.errorhandler(502)
def page_invalid_params(e, info):
	"""Error when parameters are invalid"""
	return "<h1>502 Bad Gateway</h1><p>{}</p>".format(info), 502


def vpc_info(key_id, secret_key):
	"""Get info about VPCs"""
	boto3_client = boto3.client(
		'ec2',
		aws_access_key_id=key_id,
		aws_secret_access_key=secret_key,
		region_name='eu-central-1'
	)

	return boto3_client.describe_vpcs()


@app.route('/api', methods=['GET'])
def api():
	"""Process API requests"""
	query_parameters = request.args

	key_id = query_parameters.get('id')
	secret_key = query_parameters.get('secret')

	if key_id and secret_key:
		try:
			results = vpc_info(key_id, secret_key)
			return jsonify(results)

		except Exception as e:
			return page_invalid_params(502, str(e))

	elif key_id or secret_key:
		return page_missing_params(400)

	else:
		return page_not_found(404)


if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
