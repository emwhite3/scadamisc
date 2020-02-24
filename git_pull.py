import base64
import requests
import json
import subprocess
from pathlib import Path

def establish_json(json_name):
    json_file = Path(json_name)
    #check if file exists, if it does then we delete the file
    if json_file.is_file():
        subprocess.call("rm %s"% json_name, shell=True)

    #create file to be written to from network
    subprocess.call("touch %s"% json_name, shell=True)

def git_pull():
    user = 'emwhite3'
    repo_name = 'scadaSimUpdated'
    path_to_file = 'scada_historian/historian/master_config.json'
    url = 'https://api.github.com/repos/%s/%s/contents/%s' % (user, repo_name, path_to_file)
    print(url)
    req = requests.get(url)

    if req.status_code == requests.codes.ok:
        req = req.json()
        content = base64.decodestring(req['content'])
        print(content)
    else:
        print("No content was found!")
    
    establish_json('master_config.json')
    with open('master_config.json', 'w') as outfile:
        json.dump(content, outfile)

git_pull()