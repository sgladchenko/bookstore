# this is the initializing script of main BookStore's object - Start object.
# this object will initialize all core-objects, such as Hub, Database, Xlsx object.

from start import Start
import os, codecs

# select mode: "normal" or "console"
mode = "normal"

# for normal start
if mode == "normal":
        path = os.path.abspath(os.curdir).decode("cp1251")
        if not path.endswith("\\"): path = path + "\\"
        if not path.endswith("\\BookStore\\"):
                print "Error in path-finding."
        else:
                start = Start(path)

if mode == "console":
        path = os.path.abspath(os.curdir)[:-3].decode("cp1251")
        if not path.endswith("\\"): path = path + "\\"
        if not path.endswith("\\BookStore\\"):
                print "Error in path-finding."
        else:
                start = Start(path)
