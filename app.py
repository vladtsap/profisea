from flask import Flask, request, jsonify
import pymongo
import boto3
from datetime import datetime, timedelta

app = Flask(__name__)

# db_client = pymongo.MongoClient('mongo', 27017)  # for running in Docker
db_client = pymongo.MongoClient('mongodb://localhost:27017/')  # for running in PyCharm

db = db_client["AWS"]
coll = db["VPCs"]


def sync_info(key_id, secret_key):
	"""Sync info about VPCs with AWS"""
	boto3_client = boto3.client(
		'ec2',
		aws_access_key_id=key_id,
		aws_secret_access_key=secret_key,
		region_name='eu-central-1'
	)

	return boto3_client.describe_vpcs()['Vpcs']


def get_info(key_id, secret_key):
	"""Process data to get info about VPCs"""
	document = coll.find_one({'key_id': key_id})  # search for document with current key_id

	if document:  # we saw this credentials before

		if datetime.utcnow() >= document['last_update'] + timedelta(minutes=10):  # 10+ mins, need to update
			vpcs_info = sync_info(key_id, secret_key)

			coll.update_one(
				{"key_id": key_id},
				{"$set": {'last_update': datetime.utcnow(),
						  'vpcs_info': vpcs_info}}
			)

		else:  # get value from db
			vpcs_info = document['vpcs_info']

	else:  # if we see this credentials first time
		vpcs_info = sync_info(key_id, secret_key)

		coll.insert_one({'key_id': key_id,
						 'secret_key': secret_key,
						 'last_update': datetime.utcnow(),
						 'vpcs_info': vpcs_info})

	return jsonify(vpcs_info)


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


@app.route('/api', methods=['GET'])
def api():
	"""Process API requests"""
	query_parameters = request.args

	key_id = query_parameters.get('id')
	secret_key = query_parameters.get('secret')

	if key_id and secret_key:  # if credentials are inputted well
		try:
			return get_info(key_id, secret_key)

		except Exception as e:  # exception while we were getting respond from AWS
			return page_invalid_params(502, str(e))

	elif key_id or secret_key:  # if one param is missing
		return page_missing_params(400)

	else:
		return page_not_found(404)


if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
