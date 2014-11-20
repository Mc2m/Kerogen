#!/usr/bin/env python

from Data import SKEY
import interface.widget.WidgetFactory as WF
import packman.SchemaLoader as SL
from interface.Interfaces import GUI
import traceback,os

intdatatup = namedtuple('ID',['width','height','widgets','resizers','shortcuts','data','decorator','renderarea','title','icon'])

def loadGUI(schemafile,module,functionmapper):
    success,data = loadSchema(schemafile,module,functionmapper)
    if not success:
        return None

    resizable = data.data.get("resizable",True)
    focus = data.data.get("focus",True)

    gui = GUI(0,0,module,resizable,focus)
    setInterface(gui,data)

    if data.decorator:
        #(dmodule,data,title,icon)
        resizable = data.decorator[1].data.get("resizable",True)
        focus = data.decorator[1].data.get("focus",True)
        decorator = GUI(0,0,data.decorator[0],resizable,focus)
        setInterface(gui,data.decorator[1].data)

        decorator.title = data.decorator[1].title
        decorator.icon = data.decorator[1].icon
        decorator.setTitle(data.decorator[2])
        decorator.setIcon(data.decorator[3])

        #adjust size and put gui in place of renderarea
        replaceRenderArea(gui,decorator,data.decorator[1].renderarea)

    return gui

def getRelativeResize(resizefactor,renderarea,dimension):
    #resize algorithm
    #(resizeratio/ratio)*ratiosum + (res%ratio + previous ratios)
    #if widget in a group then resize factor

    widget = renderarea
    wresdata = renderarea.resdata[dimension]

    #handle group
    if wresdata.group:
        resizefactor = resizefactor * wresdata.group.resdata.ratio/wresdata.ratio
        widget = wresdata.group

    #sum previous ratio
    previous_ratios = 0
    ratiosum = 0
    wresdata = widget.resdata[dimension]
    ratio = wresdata.ratio

    if wresdata.previous:
        widget = wresdata.previous
        while widget:
            wresdata = widget.resdata[dimension]
            previous_ratios += wresdata.ratio
            widget = wresdata.previous if wresdata.previous else None
    #get ratiosum

    for rs,resizer in decorator.resizer[dimension]:
        if resizer == widget:
            ratiosum = rs

    return (resizefactor/ratio)*ratiosum + ((resizefactor%ratio) + previous_ratios)

def replaceRenderArea(gui,decorator,renderareaid):
    renderarea = decorator.widgets[renderareaid]
    wresdata = renderarea.resdata

    resizewidth = gui.width - renderarea.width
    resizeheight = gui.height - renderarea.height

    if wresdata[0].minres != -1 and resizewidth != 0:
        resizewidth = getRelativeResize(resizewidth,renderarea,0)

    if wresdata[1].minres != -1 and resizeheight != 0:
        resizeheight = getRelativeResize(resizeheight,renderarea,1)

    decorator.resize(resizewidth,resizeheight)

    #put the gui in place
    decorator.widgets[renderareaid] = gui

    gui.wresdata = wresdata

    for j in range(0,2):
        wresdata = gui.wresdata[j]
        if wresdata.group:
            for i,widget in enumerate(wresdata.group.widgets):
                if widget == renderarea:
                    wresdata.group.widgets[i] = gui
                    break
        else:
            if wresdata.next:
                wresdata.next.resdata[j].previous = gui
            if wresdata.previous:
                wresdata.previous.resdata[j].next = gui

def loadSchema(schemafile,module,functionmapper,namesfound = []):
    interfacedata = intdatatup(0,0,[],([],[]),None,None,(None,None),None,None,None)
    idtogroup = ({},{})

    #get the name from the schemafile
    path,filename = os.path.split(schemafile)
    filename = os.path.splitext(filename)[0]

    if filename in namesfound:
        return False,None

    namesfound.append(filename)

    ischema = SL.loadSchema(schemafile)

    #load shortcuts
    interfacedata.shortcuts = ischema.get('shortcuts')

    #load options
    #todo test option
    interfacedata.data = ischema.get('data')

    #load widgets
    wschema = ischema.get('widgets')
    if not wschema:
        return False,None

    for widschema in widgetsschema:
        try:
            schema = type("schema", (), schema)
            schematype = eval("WIDGET.%s" % (schema.type))
            stop = False
            if schematype is WIDGET.GROUP:
                LoadGroup(schema,idtogroup)
            elif schematype is WIDGET.DECORATOR:
                stop = WF.LoadDecorator(schema,interfacedata,path,functionmapper,loadSchema)
            elif schematype is WIDGET.SUB:
                stop = WF.LoadWidget(schema,interfacedata,functionmapper,path,namesfound,loadSchema)
            else:
                stop = WF.LoadBaseWidget(schema,schematype,interfacedata,functionmapper,module)
            if stop:
                return False,None
        except:
            traceback.print_exc()
            print("Failed to load widget %s" % widschema)
            pass

    #finish data processing
    processData(interfacedata,idtogroup)

    return True,interfacedata

def LoadGroup(schema,idtogroup):
    g = WF.MakeGroup(schema.xgroup)
    g.resdata.ratio = schema.ratio

    for wid in schema.widgets:
        idtogroup[int(not schema.xgroup)][wid] = g

def processData(interfacedata,idtogroup):
    for i,widget in enumerate(interfacedata.widgets):
        if widget is tuple:
            widget = interfacedata.widgets[i] = makeGUIFromDataTuple(widget)

        interfacedata.width = max(widget.x+widget.width-1,interfacedata.width)
        interfacedata.height = max(widget.y+widget.height-1,interfacedata.height)

        #set resize data
        #convert widget ids in next and followers to real widgets
        for j in range(0,2):
            wresdata = widget.resdata[j]

            nextw = wresdata.next
            if nextw:
                nextw = getWidget(nextw,interfacedata,idtogroup[j])
                nextw.resdata[j].previous = widget
                if nextw in interfacedata.resizer[j]:
                    interfacedata.resizer[j].remove(nextw)
            wresdata.next = nextw

            wresdata.followers = [interfacedata.widgets[folid] for folid in wresdata.followers]

            #add the widget to the group if it exist and set as resizer if it is one
            group = idtogroup[j].get(i)
            if group:
                group.addWidget(widget)
                if not group.resdata.previous:
                    interfacedata.resizer[j].append(group)
            elif not wresdata.previous:
                interfacedata.resizer[j].append(widget)

def getWidget(wid,interfacedata,group):
    g = group.get(wid)
    if g:
        return g

    widget = interfacedata.widgets[wid]
    if widget is tuple:
        widget = interfacedata.widgets[i] = makeGUIFromDataTuple(widget)

    return widget


def makeGUIFromDataTuple(datatuple):
    #(module,interfacedata,x,y,width,height,(nextw,followers,ratio))
    resizable = datatuple[1].data.get("resizable",True)
    focus = datatuple[1].data.get("focus",True)
    gui = GUI(datatuple[2],datatuple[3],datatuple[0],resizable,focus)
    setInterface(datatuple[1])

    relx = datatuple[5] - gui.width
    rely = datatuple[6] - gui.height
    gui.resize(relx,rely)

    for j in range(0,2):
        wresdata = gui.resdata[j]
        wresdata.next = datatuple[7][0][j]
        wresdata.followers = datatuple[7][1][j]
        wresdata.ratio = datatuple[7][2][j]

    return gui

def setInterface(gui,interfacedata,functionmapper,module):
    gui.updated = gui.widgets = interfacedata.widgets
    for widget in gui.widgets:
        widget.notify = gui.notify

    gui.width = interfacedata.width
    gui.height = interfacedata.height

    if hasattr(gui.module,'setWidgets'):
        gui.module.setWidgets(gui.widgets)

    if gui.resizable:
        gui.resdata[1].minres = interfacedata.data["minh"]
        gui.resdata[0].minres = interfacedata.data["minw"]

    for j in range(0,2):
        for i,resizer in enumerate(interfacedata.resizers[j]):
            wresdata = resizer.resdata[j]
            ratiosum,nextw = wresdata.ratio,wresdata.next
            while(nextw):
                wresdata = nextw.resdata[j]
                ratiosum += wresdata.ratio
                nextw = wresdata.next
            interfacedata.resizers[j][i] = ((ratiosum,interfacedata.resizers[j][i]))
            gui.remainingres[j].append((None,0))

    gui.resizer = interfacedata.resizers

    #shortcuts
    #TODO test shortcut
    for shortcut in interfacedata.shortcuts:
        spkeys = shortcut.get("specialkeys")
        skeys = 0
        if spkeys:
            for skey in spkeys:
                skeys |= eval("SKEY." + skey)
        function = shortcut["function"]
        if hasattr(FUNCTIONS,function):
            function = functionmapper(eval("FUNCTIONS.%s" % function))
            if not function:
                continue
        elif hasattr(module,function):
            function = module.function
        key = shortcut["key"]
        gui.addShortcut(skeys,key,function)

