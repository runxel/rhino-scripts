"""Creates a specified number of layers and assigns objects from a selection 
randomly to one of the layers created.   Script by Mitch Heynick 20.02.16
modified by Lucas Becker 2016-02-22"""

import rhinoscriptsyntax as rs
import random

def RandomColor():
    r=random.randint(0,255)
    g=random.randint(0,255)
    b=random.randint(0,255)
    return r,g,b

def LayerObjectRandomizer():
    prefix = "RandomLayer"
    separator = "_"
    
    objs = rs.GetObjects("Select objects", preselect=True)
    if not objs: return
    
    intObjLen = len(objs)
    leadZero = len(str(abs(intObjLen)))
    
    layer_count = rs.GetInteger("Number of layers to create?", minimum=1, maximum=intObjLen)
    if not layer_count: return
    
    layer_state = rs.GetBoolean("Group the new layers?", ("ParentLayer", "Off", "On"), True)
    if layer_state is None: return
    if layer_state[0]:
        parentLayer = "Random Layer Parent"
        rs.AddLayer(parentLayer)
    else:
        parentLayer = ""
    
    
    rs.EnableRedraw(False)
    layer_set=[]
    for i in range(layer_count):
        iZero = str(i+1).zfill(leadZero)
        layer="{}{}{}".format(prefix, separator, iZero)
        if not rs.IsLayer(layer):
            layer_set.append(rs.AddLayer(layer, RandomColor(), parent=parentLayer))
    if layer_count == intObjLen:
        for obj in objs:
            popIndex = random.choice(layer_set)
            rs.ObjectLayer(obj, popIndex)
            layer_set.remove(popIndex)
    else:
        for obj in objs:
            rs.ObjectLayer(obj,random.choice(layer_set))

# make the usage as module possible
if ( __name__ == '__main__' ):
    LayerObjectRandomizer()
