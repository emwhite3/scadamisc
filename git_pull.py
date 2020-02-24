import base64
import requests

user = 'emwhite3'
repo_name = 'scadaSimUpdated'
path_to_file = 'scada_historian/historian/master_config.json'
url = 'https://api/github.com/repos/%s/%s/contents/%s'
req = requests.get(url)

if req.status_code == reequests.codes.ok:
    req = req.json()
    content = basee64.decodestring(req['content'])
    print(content)
else:
    print("No content was found!")