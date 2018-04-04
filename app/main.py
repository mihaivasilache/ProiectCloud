import os
import json
from flask import Flask, request
import storage
import datastore
import google.cloud.logging

CLOUD_STORAGE_BUCKET = 'tema-cloud3.appspot.com'
storage_client = None
datastore_client = None
logger = None
project_id = 'tema-cloud3'

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route('/upload', methods=['POST'])
def upload():
	logger.log_text('Request for /upload')
	uploaded_file = request.files.get('file')
	datastore.insert(datastore_client, uploaded_file)
	if not uploaded_file:
		return 'No file uploaded.', 400
	return storage.upload_file(storage_client, uploaded_file)
	
@app.route('/list', methods=['GET'])
def list_files():
	logger.log_text('Request for /list')
	files = []
	for file in datastore.list_files(datastore_client):
		file_ = {}
		items = file.items()
		for item in items:
			if item[0] == 'added':
				file_[item[0]] = str(item[1])
			else:
				file_[item[0]] = item[1]
		files.append(file_)
	storage_files = storage.list_blobs(storage_client)
	print 'in storage: ', storage_files
	print 'in datastore: ', files
	return json.dumps(files)


@app.route('/sorted', methods=['GET'])
def list_files_sorted():
	logger.log_text('Request for /slist')
	files = []
	for file in datastore.descending_sort(datastore_client):
		file_ = {}
		items = file.items()
		for item in items:
			if item[0] == 'added':
				file_[item[0]] = str(item[1])
			else:
				file_[item[0]] = item[1]
		files.append(file_)
	storage_files = storage.list_blobs(storage_client)
	print 'in storage: ', storage_files
	print 'in datastore: ', files
	return json.dumps(files)

	
@app.route('/delete', methods=['DELETE'])
def delete_files():
	return datastore.delete_files(datastore_client)
	
@app.route('/')
def hello():
	logger.log_text('Request for /')
	return 'Hello World!', 200

@app.errorhandler(500)
def server_error(e):
	logger.log_text('An error occurred during a request.')
	return "An internal error occurred: <pre>{}</pre>See logs for full stacktrace.".format(e), 500

@app.before_first_request
def execute_this():
	global logger, storage_client, datastore_client
	logging_client = google.cloud.logging.Client(project_id)
	log_name = 'my-log'
	logger = logging_client.logger(log_name)
	storage_client = storage.get_client()
	datastore_client = datastore.get_client()

'''
def main(environ, start_response):
	app.run(host='127.0.0.1', port=8000, debug=True)
'''
if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8000, debug=True)
