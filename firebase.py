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
        opts, args = getopt.getopt(sys.argv[1:], "ho:devs", ["help", "env=", "output=", "search", "days-ago=", "minutes-ago="])
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
        elif o == "-e":
            if "search" in args:
                mc.search_doc()
            verbose = True
        elif o in ("-o", "--output"):
            output = a
        else:
            assert False, "unhandled option"
    # ...

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
        self.args = args
        print(opts)
        print(args)
        for a in args:
            m = re.search('env=(prd|stg|dev)', a)
            if m is not None:
                self.enviroment = m.group(1)
        self.db = firestore.client()
        print('---------------------')
        print(u'[enviroment]: {}'.format(self.enviroment))
        print('---------------------')
        #self.collection = self.db.collection(u'{}-jnl'.format(self.enviroment)).document(u'status').collection(u'jnl')

    def search_doc(self):
        d = self.from_args('days-ago=(\d+)$')
        s = self.from_args('seconds-ago=(\d+)$')
        now = datetime.datetime.now()
        interval_type = 'seconds'
        interval_num = -1
        if d:
            interval_type = 'days'
            interval_num = int(d)
        elif s:
            interval_type = 'seconds'
            interval_num = int(s)
        else:
            print(self.args)
            dt = (now - datetime.timedelta(**{interval_type: interval_num})).strftime("%Y%m%d-%H:%M")
            print(dt)
            print('---------------------')
            sys.exit(0)
        dt = (now - datetime.timedelta(**{interval_type: interval_num})).strftime("%Y%m%d-%H:%M")
        print(dt)
        print('---------------------')
        doc_ref = self.db.collection(u'{}-jnl'.format(self.enviroment)).document(u'status').collection(u'jnl') \
            .where(u"status.bgn", ">=", dt) \
            .order_by(u'status.bgn', direction=firestore.Query.DESCENDING)
        cnt = 0
        for doc in doc_ref.stream():
            if 'exe' in doc.to_dict()['status']:
                if 'fin' not in doc.to_dict()['status']:
                    print("'exe' in doc.to_dict()['status'] and 'fin' not in doc.to_dict()['status']")
                else:
                    continue
                    # print("JOB IS DONE.")
            elif 'exe' not in doc.to_dict()['status']:
                print("not in doc.to_dict()['status']")
            print(u'{}, {}'.format(doc.id, doc.to_dict()))
            #print('---------------------')
            cnt = cnt+1
        print(cnt)
        pass

    def from_args(self, pattern):
        for a in self.args:
            m = re.search(pattern, a)
            if m is not None:
                return m.group(1)
        return None

    def __del__(self):
        print('[{}] END  '.format(datetime.datetime.now()))
        pass

if __name__ == "__main__":
    main()
