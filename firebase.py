import datetime
import getopt
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import os
import re
import sys

# export GOOGLE_APPLICATION_CREDENTIALS='/c/Users/kazuh/AppData/Roaming/gcloud/directed-portal-xxxxxx.json'
def main():

    with open(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')) as f:
        df = json.load(f)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:cdev", ["help", "env=", "output="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    env = None
    output = None
    verbose = False

    mc = MyClass(df['project_id'], opts,args)
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
            verbose = True
        elif o in "-c":
            mc.count_doc()
        elif o == "-e":
            verbose = True
        elif o in ("-o", "--output"):
            output = a
        else:
            assert False, "unhandled option"
    # ...
    # print(opts)
    # print(args)

def usage():
    print("usage")

class MyClass:
    enviroment = 'dev'
    def __init__(self, project_id, opts, args):
        print('[{}] START'.format(datetime.datetime.now()))
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred, {
            'projectId': project_id,
        })
        for a in args:
            m = re.search('env=(prd|stg|dev)', a)
            if m.group(1) is not None:
                self.enviroment = m.group(1)
        self.db = firestore.client()
        print(u'[enviroment]: {}'.format(self.enviroment))
        self.collection = self.db.collection(u'{}-jnl'.format(self.enviroment)).document(u'status').collection(u'jnl')

    def count_doc(self):
        doc_ref = self.db.collection(u'{}-jnl'.format(self.enviroment)).document(u'status').collection(u'jnl') \
            .order_by(u'fid', direction=firestore.Query.DESCENDING).stream()
        # print(doc_ref)
        cnt = 0
        for doc in doc_ref:
            print(u'{}, {}'.format(doc.id, doc.to_dict()))
            cnt = cnt+1
        print(cnt)
        pass

    def __del__(self):
        print('[{}] END  '.format(datetime.datetime.now()))
        pass

if __name__ == "__main__":
    main()