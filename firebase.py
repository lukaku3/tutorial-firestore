import datetime
import getopt
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import re
import sys

# export GOOGLE_APPLICATION_CREDENTIALS='/c/Users/kazuh/AppData/Roaming/gcloud/directed-portal-xxxxxx.json'
def main():
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

    mc = MyClass(opts,args)
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
        print('-------------{}'.format(verbose))
    # ...
    # print(opts)
    # print(args)

def usage():
    print("usage")

class MyClass:
    project_id = 'directed-portal-268501'
    enviroment = 'dev'
    def __init__(self, opts, args):
        print('[{}] START'.format(datetime.datetime.now()))
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred, {
            'projectId': self.project_id,
        })
        for a in args:
            m = re.search('env=(prd|stg|dev)', a)
            if m.group(1) is not None:
                self.enviroment = m.group(1)
                print(self.enviroment)
        self.db = firestore.client()
        self.collection = self.db.collection(u'{}-jnl'.format(self.enviroment)).document(u'status').collection(u'jnl')

    def count_doc(self):
        doc_ref = self.db.collection(u'dev-jnl').document(u'status').collection(u'jnl') \
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