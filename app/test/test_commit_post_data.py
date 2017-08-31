import requests
from datetime import datetime
import json

location = ""
dt=datetime.now()
body = json.dumps({
    'revision': 'nnkjhohlnhkjhkgv1jf2325553423hgj',
        'last_update': dt.strftime('%Y%m%d%H%M%S'),
        'author': "alexander",
        'author_email': "alex@123.com",
        'commit_date': dt.strftime('%Y%m%d%H%M%S'),
        'committer': "alexee_zhu",
        'committer_email': "alexee@234.com",
        'title': "hello",
        'message': "hello world"
})

r = requests.post('http://127.0.0.1:5000/repo/2/commit', data=body)
print(r.text)