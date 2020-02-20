import unittest
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# export GOOGLE_APPLICATION_CREDENTIALS='/c/Users/kazuh/AppData/Roaming/gcloud/directed-portal-xxxxxx.json'
class MyTestCase(unittest.TestCase):
    project_id = 'directed-portal-268501'
    def setUp(self):
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred, {
            'projectId': self.project_id,
        })
        self.db = firestore.client()
        pass

    def tearDown(self):
        pass

    def test_something(self):
        docs = self.db.collection(u'dev-jnl').document(u'status').collection(u'jnl').stream()
        for doc in docs:
            print(u'{} => {}'.format(doc.id, doc.to_dict()))

        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()
