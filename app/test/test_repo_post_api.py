import requests
from datetime import datetime
import json

location = ""
dt = datetime.now()
body = json.dumps({"last_update": dt.strftime('%Y%m%d%H%M%S'),
                   "domain": "www.github.com",
                   "group": "zhuke3",
                   "project": "modoojunko4"
                   })

r = requests.post('http://127.0.0.1:5000/repo', data=body)
print(r.text)
