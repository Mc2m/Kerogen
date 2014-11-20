import json
import traceback
from app.MiscUtils import enum

def loadSchema(schemafile):
    content = None

    try:
        with open(schemafile, 'r') as file:
            content = json.load(file)
    except:
        print("Invalid schema file")
        traceback.print_exc()
        pass

    return content

def testSubInterface(schema):
    #contains x,y,interfacename
    #optionally contains schemaname,width,height

    keep = True

    if not schema.get("x") or not schema.get("y"):
        print("Error: missing x,y coordinates for widget.")
        keep = False
    elif not schema.get("interface"):
        print("Error: missing interface name parameter.")
        keep = False

    return keep

def testDecorator(schema):
    #must contain interface

    keep = True

    if len(schema) < 2:
        print("Error: empty decorator component detected.")
        keep = False
    elif not schema.get("interface"):
        print("Error: no valid data detected in decorator component. Expecting \"name\" attribute.")
        keep = False

    return keep

def testAction(schema):
    #expect function with same size has action
    #accept restriction,data

    keep = True

    if len(schema.get("function")) != len(schema.get("action")):
        print("Error: there should be exactly 1 function for 1 action.")
        keep = False

    return keep


def testPicture(schema):
    keep = True

    if not schema.get("x") or not schema.get("y") or not schema.get("img"):
        print("Error: missing data detected in picture component."
              "Expecting \"x\",\"y\",\"img\" attributes.")
        keep = False
    elif schema.get("action"):
        keep = testAction(schema)

    return keep

def testText(schema):
    #expect x,y,width,height
    #background can be an image or a shape

    keep = True

    if not schema.get("x") or not schema.get("y") or not schema.get("width") or not schema.get("height"):
        print("Error: missing data detected in text component."
              "Expecting \"x\",\"y\",\"width\",\"height\" attributes.")
        keep = False
    elif schema.get("action"):
        keep = testAction(schema)

    bg = schema.get("background")
    if keep and bg:
        keepbg = True

        bgtype = bg.get("type")
        if not bgtype or (bgtype != "SHAPE" and bgtype != "PICTURE"):
            print("Error: invalid background type. Can only be \"PICTURE\" or \"SHAPE\".")
            keepbg = False
        else:
            if (bgtype == "SHAPE"):
                keepbg = testShape(bg)
            else:
                keepbg = testPicture(bg)
        if not keepbg:
            schema.pop('background')
        print("background removed.")

    return remove

def testShape(schema):
    #expect x,y,subtype
    #for Rectangle or Ellipse expect width,height
    #for Polygon expect coordlist
    #for Circle expect radius
    #for Arc expect width,height and startangle,endangle
    #for Line or Antialiased Line expect startpos,endpos
    #for Lines or Antialiased Lines expect coordlist,closed

    keep = True

    subtype = schema.get("subtype")

    if not schema.get("x") or not schema.get("y") or not subtype:
        print("Error: missing data detected in text component."
              "Expecting \"x\",\"y\",\"subtype\" attributes.")
        keep = False
    elif schema.get("action"):
        keep = testAction(schema)

    if keep and subtype:
        if subtype is 'RECTANGLE' or subtype is 'ELLIPSE':
            if not schema.get("width") or not schema.get("height"):
                print("Error: missing data for %s. Expecting \"width\",\"height\"." % subtype.lower())
                keep = False
        elif subtype is 'POLYGON':
            if not schema.get("coordlist"):
                print("Error: missing data for %s. Expecting \"coordlist\"." % subtype.lower())
                keep = False
        elif subtype is 'CIRCLE':
            if not schema.get("radius"):
                print("Error: missing data for %s. Expecting \"radius\"." % subtype.lower())
                keep = False
        elif subtype is 'ARC':
            if not schema.get("width") or not schema.get("height") or not schema.get("startangle") or not schema.get("endangle"):
                print("Error: missing data for %s. Expecting \"width\",\"height\",\"startangle\",\"endangle\"." % subtype.lower())
                keep = False
        elif subtype is 'LINE' or subtype is 'AALINE':
            if not schema.get("startpos") or not schema.get("endpos"):
                print("Error: missing data for %s. Expecting \"startpos\",\"endpos\"." % subtype.lower())
                keep = False
        elif subtype is 'LINES' or subtype is 'AALINES':
            if not schema.get("coordlist") or not schema.get("closed"):
                print("Error: missing data for %s. Expecting \"coordlist\",\"closed\"." % subtype.lower())
                keep = False

    return keep

#TODO console && description
