from google.cloud import storage
from google.auth import compute_engine

CLOUD_STORAGE_BUCKET = 'tema-cloud3.appspot.com'
project_id = 'tema-cloud3'

def get_client():
	credentials = compute_engine.Credentials()
	storage_client = storage.Client(credentials=credentials, project=project_id)
	return storage_client
	
def get_buckets(storage_client):
	buckets = list(storage_client.list_buckets())
	print(buckets)
	
def upload_file(storage_client, uploaded_file):
	bucket = storage_client.get_bucket(CLOUD_STORAGE_BUCKET)
	blob = bucket.blob(uploaded_file.filename)
	blob.upload_from_string(uploaded_file.read(), content_type=uploaded_file.content_type)
	return blob.public_url
	
def list_blobs(storage_client):
	bucket = storage_client.get_bucket(CLOUD_STORAGE_BUCKET)
	blobs = bucket.list_blobs()
	blobs_ = []
	for blob in blobs:
		blobs_.append(blob.name)
	return blobs_