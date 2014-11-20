import app.Data as Data
import packman.External as External
from app.MiscUtils import positionInRectangle,findExposedAreas,overlay,intersection
from interface.component.WidgetFactory import loadSchema
from option.Option import options
from interface.Interfaces import GUI
from interface.widget.Widget import Widget
import traceback,time,os

#put here the shortcuts that cannot be put in place
InvalidShortcuts = []

class InterfaceManager(object):

    def __init__(self):
        self.renderer = self.topinterface = None

        self.refresh = False            #refresh the whole screen

        self.shortcuts = {}
        self.specialkeys = 0

        self.currentinterface = None    #contains (topinterface,loadedinterface).
        self.focusedwidget = None

        self.anchorint = self.resizeint = None

    def dirty(self,widget):
        pass

    def setRenderer(self, renderer):
        self.renderer = renderer
        renderer.setInterface(self)

    def setExternal(self,external):
        self.external = external

    def runScreen(self,files):
        modulefile,schemafile = files
        modulefile = os.path.join(self.currentinterface.module.__file__,modulefile)
        schemafile = os.path.join(self.currentinterface.module.__file__,schemafile)

        module,schema = self.external.loadInterface(modulefile,schemafile)

        success,interfacedata = loadSchema(schema,module,self.currentinterface.notify,self.remapActions)
        if success:
            interfacedata.container = None
            interface = self.currentinterface[1]
            interface.setInterface(interfacedata)
        else:
            print("Invalid Interface, aborting screen change")

    def anchor(self, unused):
        self.anchoredint = self.currentinterface

    def resize(self, direction):
        isinrightest = not self.focusedwidget.x == 0
        isindownest = not self.focusedwidget.y == 0
        self.resizeint = (direction,isinrightest,isindownest)

    def maximize(self, unused):
        self.currentinterface.maximize(self.renderer.width,self.renderer.height)

    def minimize(self,unused):
        self.currentinterface.minimize()

    def restore(self,unused):
        self.currentinterface.restore()

    def addShortcut(self,specialkeys,key,action):
        appendin = self.shortcuts
        if specialkeys:
            appendin = self.shortcuts.get(specialkeys)
            if not appendin:
                appendin = {}
                self.shortcuts[specialkeys] = appendin

        appendin[key] = action

    def removeShortcut(self,specialkeys,key):
        removefrom = self.shortcuts
        if specialkeys:
            removefrom = self.shortcuts.get(specialkeys)
            if not removefrom:
                return

        removefrom.pop(key,None)

    def runShortcut(self,specialkeys,key):
        sdict = self.shortcuts
        if specialkeys:
            sdict = self.shortcuts.get(specialkeys)
            if not sdict:
                return

        action = sdict.get(key)
        if action:
            action()

    def getFunctionFromID(self,functionid):
        #convert function id into an actual function
        if functionid is FUNCTIONS.RUNSCREEN:
            return self.runScreen
        elif functionid is FUNCTIONS.CLOSE:
            return self.close
        elif functionid is FUNCTIONS.LAUNCH:
            return self.addInterface
        elif functionid is FUNCTIONS.ANCHOR:
            return self.anchor
        elif functionid is FUNCTIONS.RESIZE:
            return self.resize
        elif functionid is FUNCTIONS.MAXIMIZE:
            return self.maximize
        elif functionid is FUNCTIONS.MINIMIZE:
            return self.minimize
        elif functionid is FUNCTIONS.RESTORE:
            return self.restore
        else:
            print("Warning : Function id %d not recognised" % functionid)
            return None

    def addInterface(self,files,resizable = True,focusable = True):
        modulefile,schemafile = files
        path = os.path.split(modulefile[0])
        module,schema = self.external.loadInterface(modulefile,schemafile)

        success,interfacedata = loadSchema(schema,self.notify)

        if success:
            #no need to handle an empty interface
            if len(interfacedata.widgets) != 0:

                #TODO set proper relative position
                interface = GUI((30,30),name,path,module,resizable,focusable)
                self.interfaces.insert(0,interface.getTop())
                interface.setInterface(interfacedata)
        else:
            print("Failed to load interface")

    def focus(self, index):
        #get top interface from this layer
        top = self.interfaces[index].getTop()

        #remove from the list
        del self.interfaces[index]

        #push front
        self.interfaces.insert(0,top)

        top.focus()

    def findInterfaceAndComponent(self,x,y):
        #returns interfaceindex and component
        index,comp = -1,None
        for i,interface in enumerate(self.interfaces):
            if positionInRectangle((x,y),interface.box()):
                #we clicked on this interface
                index = i
                comp = interface.findComponentAtCoordinates(x,y)
                break

        if index is -1:
            #clicked on the base interface
            comp = self.base.findComponentAtCoordinates(x,y)

        return index,comp

    def onClick(self,x,y,button,down):
        if self.focusedcomponent and self.focusedcomponent.type() == COMPONENT.PICTURE:
            self.focusedcomponent.setStatus(False,False)
        self.focusedcomponent = self.interfacefocused = None

        if self.anchorint or self.resizeint:
            self.anchorint = self.resizeint = False
            return

        i,component = self.findInterfaceAndComponent(x,y)

        if i > 0:
            #focus
            self.focus(i)

        if component:
            self.focusedcomponent = component
            #TODO set status for all components
            if down and component.type() == COMPONENT.PICTURE:
                component.setStatus(False,True)

            #execute component action
            callback = component.actionmapping.get(ACTIONS.MOUSEDOWN if down else ACTIONS.MOUSEUP)
            if callback:
                if callback[2] and callback[2] == button:
                    callback[0](callback[1])

    def onMouseMove(self,x,y,relx,rely):
        #TODO highlight component
        if self.anchorint:
            #move the top interface
            self.interfaces[0].move(relx,rely)

            #redraw
            self.clean = True

        elif self.resizeint:
            direction,isinrightest,isindownest = self.resizeint
            if (direction == RESIZE.HORIZONTAL or
                (rely < 0 and self.interfaces[0].y < y and not isindownest) or
                (rely > 0 and self.interfaces[0].y > y and isindownest)):
                rely = 0
            if (direction == RESIZE.VERTICAL or
                  (relx < 0 and self.interfaces[0].x < x and not isinrightest) or
                  (relx > 0 and self.interfaces[0].x > x and isinrightest)):
                relx = 0

            if rely == 0 and relx == 0:
                return

            #going left while resizing from the left side of a window (increase size) is like
            #moving left then going right from the right side of the window
            if not isinrightest:
                relx = -relx
            if not isindownest:
                rely = -rely

            #resize the interface to the current size
            relx,rely = self.interfaces[0].resize(relx,rely)

            if relx or rely:
                movx = -relx if (not isinrightest) else 0
                movy = -rely if (not isindownest) else 0
                if movx or movy:
                    self.interfaces[0].move(movx,movy)

            #redraw
            self.clean = True

    def onKeyPressed(self,key,unicodek,mod,down):
        #TODO keys
        pass

    def close(self, index = 0):
        if index == None:
            index = 0

        if index < 0 or index > len(self.interfaces):
            return

        self.clean = True

        self.interfaces.pop(index)
        self.focusedcomponent = None

    def kill(self):
        self.app.kill()

    def updateAndRender(self):
        try:
            now = time.time()

            surf = self.base.updateRender(self.clean)
            if surf:
                if self.renderer:
                    self.renderer.render(surf,(self.base.x,self.base.y))
                self.base.dirty = False
                self.clean = True

            for ui in reversed(self.interfaces):
                surf = ui.updateRender(self.clean)
                if surf:
                    if self.renderer:
                        self.renderer.render(surf,(ui.x,ui.y))
                    ui.dirty = False
                    self.clean = True

            self.clean = False
            if surf:
                print("time to update and render %d interfaces: %s" % (len(self.interfaces)+1,str(time.time()-now)))
        except:
            traceback.print_exc()
            pass

    def __str__(self):
        return "KiteInterface:\ninterfaces: %s\n" % (str(self.interfaces))

iman = InterfaceManager()
