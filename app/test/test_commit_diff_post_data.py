import requests
from datetime import datetime
import json

location = ""
dt = datetime.now()
body = json.dumps({'commit_id': 2,
                   'last_update': dt.strftime('%Y%m%d%H%M%S'),
                   'change_file': "/usr/bin/bash",
                   'add_lines': 32,
                   'del_lines': 20
                   })

r = requests.post('http://127.0.0.1:5000/repo/2/commit/2/commit_diff', data=body)
print(r.text)
