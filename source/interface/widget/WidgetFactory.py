from Data import WIDGET,SHAPE
from Picture import Picture
from Shape import Shape
from Text import Text
from Composite import Composite
from kge import external
import resman.SchemaLoader as SL
import traceback,os

def LoadDecorator(schema,interfacedata,path,functionmapper,schemaLoader):
    if interfacedata.decorator:
        print("Error: Multiple decorators defined while only one is acceptable")
        return True
    if SL.testDecorator(schema):
        #test for eventual title,icon
        title = icon = None
        if hasattr(schema,'title'):
            title = schema.title
        if hasattr(schema,'icon'):
            icon = schema.icon

        #create paths
        ifilepath = None
        sfilepath = os.path.join(path,schema.schema + ".json")
        if hasattr(schema,"interface"):
            ifilepath = os.path.join(path,schema.interface + ".py")
        else:
            ifilepath = os.path.join(path,schema.schema + ".py")

        #load module
        dmodule,schemafile = external.loadInterface(ifilepath,sfilepath)
        if not dmodule or not schemafile:
            print("Error: Failed to load decorator.")
            return True

        success,data = schemaLoader(schemafile,dmodule,functionmapper)
        if not success:
            print("Error: Failed to load decorator.")
            return True
        if not data.renderarea:
            print("Error: Missing decorator render area.")
            return True

        interfacedata.decorator = (dmodule,data,title,icon)
    return False


def LoadWidget(schema,interfacedata,functionmapper,path,namesfound,schemaLoader):
    if SL.testSubInterface(schema):
        #create paths
        ifilepath = None
        sfilepath = os.path.join(path,schema.schema + ".json")
        if hasattr(schema,"interface"):
            ifilepath = os.path.join(path,schema.interface + ".py")
        else:
            ifilepath = os.path.join(path,schema.schema + ".py")

        #load module
        dmodule,schemafile = external.loadInterface(ifilepath,sfilepath)
        if not dmodule or not schemafile:
            print("Error: Failed to load decorator.")
            return True

        success,data = schemaLoader(schemafile,dmodule,functionmapper,namesfound)
        if not success:
            print("Error: Failed to load decorator.")
            return True

        x = schema.x
        y = schema.y
        width = data.width
        height = data.height
        if hasattr(schema,'width'):
            width = schema.width
        if hasattr(schema,'height'):
            height = schema.height
        nextw = followers = None
        ratio = 0
        if hasattr(schema,'next'):
            nextw = schema.next
            ratio = schema.ratio
        if hasattr(schema,'followers'):
            followers = schema.followers

        interfacedata.widgets.append((dmodule,data,x,y,width,height,(nextw,followers,ratio)))
    return False

def LoadBaseWidget(schema,schematype,interfacedata,functionmapper,module):
    widget = None
    lenwidgets = len(interfacedata.widgets)

    if schematype is WIDGET.TEXT:
        if SL.testText(schema):
            widget = Text()
            if hasattr(schema,'title'):
                interfacedata.title = lenwidgets
    elif schematype is WIDGET.PICTURE:
        if SL.testPicture(schema):
            widget = Picture()
            if hasattr(schema,'icon'):
                interfacedata.icon = lenwidgets
    elif schematype is WIDGET.SHAPE:
        if SL.testShape(schema):
            widget = Shape()
            if hasattr(schema,'renderarea'):
                interfacedata.renderarea = lenwidgets
    else:
        print("Widget type %s not recognised." % (schema.type))
        return True

    if not widget:
        return True

    try:
        widget.load(schema)

        #load actions
        #TODO check actions restrictions here
        loadWidgetAction(widget,schema,functionmapper,module)

    except:
        traceback.print_exc()
        return True

    interfacedata.widgets.append(widget)

    return False

def loadWidgetAction(widget,schema,functionmapper,module):
    if hasattr(schema,"action") and hasattr(schema,"function"):
        for i,straction in enumerate(schema.action):
            action = eval("ACTIONS.%s" % (straction))
            function = schema.function[i]
            if hasattr(FUNCTIONS,function):
                function = functionmapper(eval("FUNCTIONS.%s" % function))
                if not function:
                    continue
            elif hasattr(module,function):
                function = module.function

            data,restriction = None,None
            if hasattr(schema,"data") and i < len(schema.data):
                data = schema.data[i]

            if hasattr(schema,"restriction") and i < len(schema.restriction):
                restriction = eval("MOUSE.%s" % schema.restriction[i])

            self.addAction(action,function,data,restriction)


def cleaningBox(w):
    widget = Shape()
    widget.x,widget.y,widget.width,widget.height = w.x,w.y,w.width,w.height
    widget.subtype = SHAPE.RECTANGLE
    widget.color = (0,0,0)

    return widget
