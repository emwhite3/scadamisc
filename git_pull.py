import base64
import requests
import json
import subprocess
from pathlib import Path


# Method: establish json
# Description: Checks if json file exists and if not it creates the json file
# Otherwise it purges the current copy and creates a new one
# Arguments:
#
# Returns: void
def establish_json(json_name):
    json_file = Path(json_name)
    #check if file exists, if it does then we delete the file
    if json_file.is_file():
        subprocess.call("rm %s"% json_name, shell=True)

    #create file to be written to from network
    subprocess.call("touch %s"% json_name, shell=True)

def get_json_current(json_name):
    with open(json_name) as json_file:
        return json.load(json_file)

# Method: git pull
# Description: Pulls json file from given repo and dumps into given json file
# Arguments: json file name: string, git user: string, git repo name: string, git path to file: string
# Returns: void
def git_pull(json_file, user, repo_name, path_to_file):
    url = 'https://api.github.com/repos/%s/%s/contents/%s' % (user, repo_name, path_to_file)
    print(url)
    req = requests.get(url)

    if req.status_code == requests.codes.ok:
        req = req.json()
        content = base64.decodestring(req['content'])
        print(content)
    else:
        print("No content was found!")
    
    establish_json(json_file)
    with open('master_config.json', 'w') as outfile:
        json.dump(repr(content), outfile)


json_file = 'master_config.json'
user = 'emwhite3'
repo_name = 'scadaSimUpdated'
path_to_file = 'scada_historian/historian/master_config.json'
git_pull(json_file, user, repo_name, path_to_file)
