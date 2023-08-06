import json
import sys
from pygisty.gisty import headless, post
from pygisty import options
from appdirs import *
from pygisty.options import fileoptions

def main():
    global authtoken
    appname = "pygisty"
    appauthor = "BlyatManGopnik"
    configdir = user_data_dir(appname, appauthor)
    if not os.path.exists(configdir):
        print("Creating " + configdir)
        os.makedirs(configdir)
    if len(sys.argv) > 3:
        print("Too many options. Exiting.")
        sys.exit(1)
    if len(sys.argv) == 2:
        options.options(sys.argv[1])
    clientid = "7da0ffca60ba4ae64eb3"
    print("pygisty v0.0.5")
    if os.path.exists(configdir + "/access_token.json") == False:
        authtoken = headless.headless(clientid, configdir)
    else:
        with open(configdir + "/access_token.json", "r") as configfile:
            jsondata = json.load(configfile)
            authtoken = jsondata["access_token"]
    if len(sys.argv) == 3:
        sentence = options.fileoptions(sys.argv[2], sys.argv[1])
    else:
        sentence = input("Put a sentence here!: ")
    if len(sys.argv) < 3:
        html = post.post(authtoken, sentence, "pygisty.txt")
    else:
        html = post.post(authtoken, sentence, sys.argv[2])
    print("We got the URL!: " + html)
if __name__ == '__main__':
    main()
