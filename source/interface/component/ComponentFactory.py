from game.Data import COMPONENT,SHAPE
from interface.component.Picture import Picture,Component
from interface.component.Shape import Shape
from interface.component.Text import Text
from collections import namedtuple
import traceback

def loadSchema(schema,notifier):
    intdatatup = namedtuple('ID',['components','decorator','sideinterfaces','data','renderarea','title','icon'])
    interfacedata = intdatatup([],None,[],(None,None),None,None,None)

    for compschema in schema:
        try:
            stop = LoadComponent(compschema,interfacedata,notifier)
            if stop:
                return False,interfacedata
        except:
            traceback.print_exc()
            print("Failed to load component %s" % compschema)
            pass

    return True,interfacedata

def LoadComponent(schema,interfacedata,notifier):
    schema = type("schema", (), schema)
    schematype = eval("COMPONENT.%s" % (schema.type))

    if schematype is COMPONENT.DECORATOR:
        if interfacedata.decorator:
            print("Error: Multiple decorators defined while only one is acceptable")
            return True
        interfacedata.decorator = schema.name

    elif schematype is COMPONENT.DATA:
        if interfacedata.data:
            print("Error: Multiple data defined while only one is acceptable")
            return True

        title = icon = None
        if hasattr(schema,'title'):
            title = schema.title
        if hasattr(schema,'icon'):
            icon = schema.icon
        if title or icon:
            interfacedata.data = (title,icon)

    elif schematype is COMPONENT.NEAR:
        name = schema.name
        positions = []
        for position in schema.positions:
            position = eval("RELPOS.%s" % (position))
            if position != RELPOS.CENTER:
                positions.append(position)
        interfacedata.sideinterfaces.append((name,positions))
    else:
        component = LoadRenderComponent(schema,schematype,interfacedata,notifier)

def LoadRenderComponent(schema,schematype,interfacedata,notifier):
    component = None

    if schematype is COMPONENT.TEXT:
        component = Text()
        if hasattr(schema,"background"):
            component.background = LoadComponent(schema.background,interfacedata,notifier)
    elif schematype is COMPONENT.PICTURE:
        component = Picture()
    elif schematype is COMPONENT.SHAPE:
        component = Shape()
    else:
        print("Component type %s not recognised." % (schema.type))
        return

    try:
        component.notify = notifier
        component.load(schema)
        if hasattr(schema,'renderarea'):
            interfacedata.renderarea = component
        elif hasattr(schema,'title'):
            interfacedata.title = component
        elif hasattr(schema,'icon'):
            interfacedata.icon = component
    except:
        traceback.print_exc()
        return

    interfacedata.components.append(component)

def cleaningBox(box):
    component = Shape()
    component.x,component.y = box[0][0],box[0][1]
    component.width,component.height = box[1][0]-component.x,box[1][1]-component.y
    component.subtype = SHAPE.RECTANGLE
    component.color = (0,0,0)

    return component
