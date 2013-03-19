import json
import traceback
from app.MiscUtils import enum

SCHEMATYPES = type('schematype', (), {'DESC':1,'INTERFACE':2,'CONSOLE':3})

def loadSchema(schemafile,schematype):
    content = None

    try:
        with open(schemafile, 'r') as file:
            content = json.load(file)
    except:
        print("Invalid schema file")
        traceback.print_exc()
        pass

    if content:
        content = test(content,schematype)

    return content

def test(schema,schematype):
    if schematype is SCHEMATYPES.INTERFACE:
        schema = [x for x in schema if not testComponent(x)]
    #TODO test decription && console

    return schema

def testComponent(schema):
    sctype = schema.get('type')

    if sctype is "DATA":
        return testData(schema)
    elif sctype is "DECORATOR":
        return testDecorator(schema)
    elif sctype is "PICTURE":
        return testPicture(schema)
    elif sctype is "TEXT":
        return testText(schema)
    elif sctype is "SHAPE":
        return testShape(schema)

    return False


def testData(schema):
    #optionally contains title and icon

    remove = False

    hastitle,hasicon = schema.get("title"),schema.get("icon")
    if len(schema) == 0:
        print("Warning: empty data component detected. Component removed.")
        remove = True
    elif not hastitle and not hasicon:
        print("Warning: no valid data detected in data component. Component removed.")
        remove = True

    return remove

def testData(schema):
    #optionally contains title and icon
    #can be empty
    used = ["title","icon"]

    remove = False

    hastitle,hasicon = schema.get("title"),schema.get("icon")
    if len(schema) < 2:
        print("Error: empty data component detected.")
        remove = True
    elif not hastitle and not hasicon:
        print("Error: no valid data detected in data component. Accept \"title\" and \"icon\" attributes.")
        remove = True
    elif len(schema) > 2 and (not hastitle or not hasicon):
        print("Warning: invalid data detected in data component. Only %s will be used." % used)

    return remove

def testDecorator(schema):
    #must contain name

    remove = False
    hasname = schema.get("name")

    if len(schema) < 2:
        print("Error: empty decorator component detected.")
        remove = True
    elif not hasname:
        print("Error: no valid data detected in decorator component. Expecting \"name\" attribute.")
        remove = True
    elif len(schema) > 2:
        print("Warning: invalid data detected in data component. Only name will be used.")

    return remove

def testAction(schema):
    #expect function with same size has action
    #accept restriction,data

    removed = False

    if len(schema.get("function")) != len(schema.get("action")):
        print("Error: there should be exactly 1 function for 1 action.")
        removed = True

    return removed


def testPicture(schema):
    remove = False

    if not schema.get("x") or not schema.get("y") or not schema.get("img"):
        print("Error: missing data detected in picture component."
              "Expecting \"x\",\"y\",\"img\" attributes.")
        remove = True
    elif schema.get("action"):
        remove = testAction(schema)

    return remove

def testText(schema):
    #expect x,y,width,height
    #background can be an image or a shape

    remove = False

    if not schema.get("x") or not schema.get("y") or not schema.get("width") or not schema.get("height"):
        print("Error: missing data detected in text component."
              "Expecting \"x\",\"y\",\"width\",\"height\" attributes.")
        remove = True
    elif schema.get("action"):
        remove = testAction(schema)

    bg = schema.get("background")
    if not remove and bg:
        removebg = False

        bgtype = bg.get("type")
        if not bgtype or (bgtype != "SHAPE" and bgtype != "PICTURE"):
            print("Error: invalid background type. Can only be \"PICTURE\" or \"SHAPE\".")
            removebg = True
        else:
            removebg = testComponent(bg)
        if removebg:
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

    remove = False

    subtype = schema.get("subtype")

    if not schema.get("x") or not schema.get("y") or not subtype:
        print("Error: missing data detected in text component."
              "Expecting \"x\",\"y\",\"subtype\" attributes.")
        remove = True
    elif schema.get("action"):
        remove = testAction(schema)

    if not remove and subtype:
        if subtype is 'RECTANGLE' or subtype is 'ELLIPSE':
            if not schema.get("width") or not schema.get("height"):
                print("Error: missing data for %s. Expecting \"width\",\"height\"." % subtype.lower())
                remove = True
        elif subtype is 'POLYGON':
            if not schema.get("coordlist"):
                print("Error: missing data for %s. Expecting \"coordlist\"." % subtype.lower())
                remove = True
        elif subtype is 'CIRCLE':
            if not schema.get("radius"):
                print("Error: missing data for %s. Expecting \"radius\"." % subtype.lower())
                remove = True
        elif subtype is 'ARC':
            if not schema.get("width") or not schema.get("height") or not schema.get("startangle") or not schema.get("endangle"):
                print("Error: missing data for %s. Expecting \"width\",\"height\",\"startangle\",\"endangle\"." % subtype.lower())
                remove = True
        elif subtype is 'LINE' or subtype is 'AALINE':
            if not schema.get("startpos") or not schema.get("endpos"):
                print("Error: missing data for %s. Expecting \"startpos\",\"endpos\"." % subtype.lower())
                remove = True
        elif subtype is 'LINES' or subtype is 'AALINES':
            if not schema.get("coordlist") or not schema.get("closed"):
                print("Error: missing data for %s. Expecting \"coordlist\",\"closed\"." % subtype.lower())
                remove = True

    return remove
