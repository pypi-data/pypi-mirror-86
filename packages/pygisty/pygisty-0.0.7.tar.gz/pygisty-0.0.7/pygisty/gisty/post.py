import json
import sys
import requests
import os

def post(authtoken, content, filename):
    print("Uploading " + filename)
    if len(sys.argv) == 3:
        filepath = os.path.basename(sys.argv[2]).strip("\n")
    else:
        filepath = filename
    jsondata = "{\"files\": {\""+filepath+"\": {\"content\": \""+content+"\"}}}"
    header = {'User-Agent': "pygisty", "Authorization": "token "+authtoken, "Accept": "application/json"}
    r = requests.Session()
    r.headers.update(header)
    request = r.post("https://api.github.com/gists", data=jsondata.encode(encoding='utf-8'))
    dat = json.loads(request.text)
    try:
        error = dat["message"]
        print("Error: " + error)
        sys.exit(1)
    except KeyError:
        test = ""
    html = dat["html_url"]
    return html
