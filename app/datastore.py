from google.cloud import datastore
import datetime

project_id = 'tema-cloud3'

def get_client():
	return datastore.Client(project=project_id)
	
def insert(datastore_client, uploaded_file):	
	complete_key = datastore_client.key('File')
	task = datastore.Entity(key=complete_key)
	task.update({
		'filename': uploaded_file.filename,
		'added': datetime.datetime.utcnow()
	})
	datastore_client.put(task)
	
def list_files(datastore_client):
	query = datastore_client.query(kind='File')
	results = list(query.fetch())
	return results

#nu merge
def delete_files(datastore_client):
	complete_key = datastore_client.key('File')
	datastore_client.delete(complete_key)
	return "Deleted all files"
