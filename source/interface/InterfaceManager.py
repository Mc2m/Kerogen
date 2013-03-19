from game.Data import ACTIONS,FUNCTIONS,COMPONENT,RESIZE
from app.MiscUtils import positionInRectangle,findExposedAreas,overlay,intersection
import traceback
from option.Option import options
import time
from interface.Interface import Interface

#put here the shortcuts that cannot be put in place
InvalidShortcuts = []

class KiteInterface(object):
    """interface for Kite"""

    def __init__(self, app, renderer):

        self.app = app
        self.renderer = renderer
        renderer.setInterface(self)
        Interface.actionmapper = self.remapActions

        self.interfaces = []    #contains top interfaces (not sublayers).
        self.base = None        #the interface that won't have any focus

        self.refresh = False    #refresh the whole screen
        self.clean = False

        self.shortcuts = {}

        self.focusedcomponent = None

        self.anchorint = self.resizeint = False

        Interface.actionmapper = self.remapActions

    def runScreen(self,screenid):
        pass

    def anchor(self, unused):
        self.anchorint = True

    def resize(self, direction):
        isinrightest = not self.focusedcomponent.x == 0
        isindownest = not self.focusedcomponent.y == 0
        self.resizeint = (direction,isinrightest,isindownest)

    def maximize(self, unused):
        self.interfaces[0].maximize(self.renderer.width,self.renderer.height)

    def minimize(self,unused):
        self.interfaces[0].minimize()

    def restor(self,unused):
        self.interfaces[0].restore()

    def addShortcut(self,action,combo,function):
        #combo is a tuple of button to be pressed
        #e.g. ('ctrl','c')
        if (action,combo) in InvalidShortcuts:
            return

        self.shortcuts[(action,combo)]=function

    def remapActions(self,component,interface):
        #convert functions id/names into real functions
        for action,functionlist in component.actionmapping.items():
            for function in functionlist:
                if type(function[0]) is int:
                    if function[0] is FUNCTIONS.RUNSCREEN:
                        component.actionmapping[action] = (self.runScreen,function[1],function[2])
                    elif function[0] is FUNCTIONS.CLOSE:
                        component.actionmapping[action] = (self.close,None,function[2])
                    elif function[0] is FUNCTIONS.LAUNCH:
                        component.actionmapping[action] = (self.addInterface,function[1],function[2])
                    elif function[0] is FUNCTIONS.ANCHOR:
                        component.actionmapping[action] = (self.anchor,None,function[2])
                    elif function[0] is FUNCTIONS.RESIZE:
                        try:
                            dimension = eval("RESIZE.%s" % function[1])
                            component.actionmapping[action] = (self.resize,dimension,function[2])
                        except:
                            print("Warning : wrong data for resizing. It can only be HORIZONTAL,VERTICAL or DIAGONAL")
                            del component.actionmapping[action]
                    else:
                        print("Warning : Function id %d not recognised", function[0])
                        del component.actionmapping[action]
                elif type(function[0]) is str:
                    component.actionmapping[action] = (getattr(interface, function[0]),function[1],function[2])

    def addBaseInterface(self,device):
        self.base = Interface((0,0),"BASE",device,False)

    def addInterface(self,(name,device)):
        try:
            #TODO set proper relative position
            interface = Interface((30,30),name,device).getTop()

            #no need to handle an empty interface
            if interface.components:
                self.interfaces.insert(0,interface)
        except:
            traceback.print_exc()
            pass

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

    def onKeyPressed(self):
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
                self.renderer.render(surf,(self.base.x,self.base.y))
                self.base.dirty = False
                self.clean = True

            for ui in reversed(self.interfaces):
                surf = ui.updateRender(self.clean)
                if surf:
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
