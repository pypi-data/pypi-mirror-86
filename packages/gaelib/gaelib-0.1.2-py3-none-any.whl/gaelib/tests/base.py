import unittest
from gaelib.db import helpers
from google.cloud import datastore
from mock import patch
from main import app


class BaseUnitTestCase(unittest.TestCase):
  def setUp(self):
    app.testing = True
    self.client = app.test_client()
    self.clear_database()

  def tearDown(self):
    self.clear_database()

  def clear_database(self):
    # Nosetests use a different database and it also does not use namespace from app.yaml,
    # so for now, we need to use the default namespace,
    # we will change this stuff later after further research.
    client = datastore.Client(namespace=helpers.get_datastore_namespace())
    query = client.query(kind='__kind__')
    query.keys_only()
    kinds = [entity.key.id_or_name for entity in query.fetch()]

    for kind in kinds:
      query = client.query(kind=kind)
      query.keys_only()
      keys = [entity.key for entity in query.fetch()]
      for i in range(0, len(keys), 499):
        client.delete_multi(keys[i:i + 499])

  def mock_storage_client(self):
    self.storage_client_patch = patch(
        'google.cloud.storage.Client')
    self.storage_client = self.storage_client_patch.start()

  def mock_bucket(self):
    self.bucket_patch = patch(
        'google.cloud.storage.Bucket')
    self.bucket = self.bucket_patch.start()

  def mock_blob(self):
    self.blob_patch = patch(
        'google.cloud.storage.Blob')
    self.blob = self.blob_patch.start()

  def mock_flask_request(self):
    self.request_patch = patch('flask.request')
    self.request = self.request_patch.start()
