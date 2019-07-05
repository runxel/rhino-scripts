# -*- coding: utf-8 -*-

""" Opens a corresponding GH file (if existing) when opening a Rhino file.
    It is recommended to have this script in your Rhino startup command list:
    _-RunPythonScript AutoLoadGrasshopperDef.py

    Caveat! This script can't do anything when Rhino is not already open 
            and you double-click open a Rhino file.
            Also just works when opening .3dm files.
"""
import Rhino
import scriptcontext
import os.path, logging, sys

logging.basicConfig(stream=sys.stderr, level=logging.INFO)

""" 
https://developer.rhino3d.com/samples/rhinopython/current-model-info/
    which was originally not working, since the script gets started in the
    document context of the previous document, which not longer exists, when
    the user is opening a new Rhino file
    this is also the reason why we don't use 
    rs.Command("! _-Grasshopper _Document _Open {} _Enter".format(new_path))
    in the delegate – it will simply not work
    
https://discourse.mcneel.com/t/execute-script-on-file-opening
    in this thread @clement sheds some light on it and has some fantastic 
    workarounds up his sleeve
    this Script wouldn't be possible without his help!
"""

def OpenDefinition(file_path):
    """ Another workaround because we can't use rs.Command() """
    logging.debug("OpenDefinition: {}".format(file_path))
    
    Grasshopper = Rhino.RhinoApp.GetPlugInObject("Grasshopper")
    if not Grasshopper: return False
    
    Grasshopper.OpenDocument(file_path)

def AfterLoadEvent(sender, e):
    """ event handler / delegate """
    path = e.FileName  # can't use rs.DocumentPath()
    if path[-3:] == "3dm":
        new_path = path[:-4] + ".gh"  # switch ".3dm" with ".gh"
        # Windows and its backslash paths:...
        new_path = new_path.split("\\")
        new_path = "\\".join(new_path)
        # not using
        # os.path.join(*new_path)  ### splat operator * for list unpacking
        # because it's faulty with absolute Win paths (drive letters, duh!)
        exists = os.path.isfile(new_path)
        if exists:
            OpenDefinition(new_path)
        else:
            print "No corresponding GH file found."

def AutoLoadGrasshopperDef():
    """ Subscribe to the EndOpenDocument event so we know when it's okay 
        to fire the Grasshopper definition load
    """
    key_after_load = "AfterLoadEvent"
    if scriptcontext.sticky.has_key(key_after_load):
        logging.debug("GH autoload deactivated")
        Rhino.RhinoDoc.EndOpenDocument -= scriptcontext.sticky[key_after_load]
        scriptcontext.sticky.Remove(key_after_load)
    else:
        logging.debug("GH autoload activated")
        scriptcontext.sticky[key_after_load] = eval(key_after_load)
        Rhino.RhinoDoc.EndOpenDocument += eval(key_after_load)

########################
if __name__=="__main__":
    AutoLoadGrasshopperDef()
