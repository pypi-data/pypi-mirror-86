from pygisty.gisty import version
import sys
def options(args):
    if args == "--help" or args == "-h":
        print("pygisty help")
        print("-f, --file <filename> Uploads the content of the file to the gist.")
        print("-v, --version Prints the program's version")
        print("-h, --help Prints help")
        sys.exit(0)
    if args == "--version" or args == "-v":
        print("pygisty v"+version.version())
        sys.exit(0)
    if args == "--file" or args == "-f":
        print("No file provided. Exiting.")
        sys.exit(1)
    if "--" or "-" in args:
        print("Invalid options. Exiting")
        sys.exit(1)
def fileoptions(file, args):
    if args == "--file" or args == "-f":
        with open(file, "r") as file:
            data = file.read().replace("\n", "\\n").replace("\"", "\\\"")
        return data
