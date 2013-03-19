#!/usr/bin/env python
from game.Data import RESIZE,RELPOS
from external.External import external
from app.MiscUtils import positionInRectangle,overlay,intersection
from interface.component.ComponentFactory import loadSchema
from lib.gameEngine.RendererHelper import prepareComponent,makeSurface,blitSurface

class Interface(object):

    actionmapper = None

    def __init__(self,(x,y),name,device,resizable = True):

        curinterface = external.getInterface(eval("external.INTERFACE.%s" % (name)))
        if curinterface:
            self.updated = []
            success,interfacedata = loadSchema(curinterface[1],self.notify)

            if not success:
                return None

            self.name = name
            self.title,self.icon = interfacedata.data

            self.x,self.y = x,y
            self.width = self.height = self.minw = self.minh = -1
            self.dimensionsto = None
            self.minimized = False

            self.device = device
            self.module = curinterface[0]
            self.components = interfacedata.components

            self.surface = None
            self.dirty = False

            self.decorator,self.sublayers = None,[]
            self.titlecomp,self.iconcomp,self.renderarea = interfacedata.title,interfacedata.icon,interfacedata.renderarea

            self.resizer = [[],[]]

            self.module.setComponents(self.device,self.components)
            self.processComponents(self.components,self.module,resizable)

            if interfacedata.decorator:
                if not self.addDecorator(decorator,resizable):
                    return None

            totalwidth,totalheight = self.width,self.height

            for sideinterface in interfacedata.sideinterfaces:
                inter = self.addSideInterface(sideinterface)
                if not inter:
                    return None


    def notify(self,comp):
        self.updated.append(comp)

    def box(self):
        return (self.x,self.y),(self.x+self.width-1,self.y+self.height-1)

    def minimize(self):
        self.minimize = True

    def maximize(self,width,height):
        self.dimensionsto = (self.x,self.y,-width-self.width,-height-self.height)
        self.x = self.y = 0
        self.resize(width-self.width,height-self.height)

    def restore(self):
        if self.minimize:
            self.minimize = False
        else:
            self.x,self.y = self.dimensionsto[0],self.dimensionsto[1]
            self.resize(self.dimensionsto[2],self.dimensionsto[3])
            self.dimensionsto = None

    def setTitle(self,title):
        if self.decorator:
            self.decorator.setTitle(title)
        elif self.titlecomp:
            self.titlecomp.setText(title)

    def setIcon(self,name):
        if self.decorator:
            self.decorator.setIcon(name)
        elif self.iconcomp:
            self.iconcomp.setPictures(name)

    def findComponent(self,name):
        for comp in self.components:
            if comp.name is name:
                return comp
        return None

    def processComponents(self,components,module,resizable = True):
        #TODO check actions restrictions here

        maxx,maxy = 0,0

        for component in components:
            #compute the interface box
            maxx = max(component.x+component.width-1,maxx)
            maxy = max(component.y+component.height-1,maxy)

            self.actionmapper(component,module)

        self.width,self.height = maxx,maxy

    def nameExists(self,name):
        if self.name == name:
            return True
        found = False
        for layer in self.sublayers:
            found = layer.nameExists(name)
            if found:
                return True

        return found

    def addSideInterface(self,data):
        inter = None

        if data:
            #data contains (name,positions)
            if self.nameExists(data[0]):
                return None
            ox = oy = 0
            for position in data[1]:
                if position == RELPOS.RIGHT:
                    ox = self.x+self.width
                elif position == RELPOS.DOWN:
                    oy = self.y+self.height
            inter = Interface((ox,oy),data[0],self.device,resizable)
            if not inter:
                return None
            if ox == 0:
                temp = self.x
                self.x = inter.x+inter.width
                inter.x = temp
            if oy == 0:
                temp = self.y
                self.y = inter.y+inter.height
                inter.y = temp
            inter = inter.getTop()
            inter.decorator = self.decorator
            self.decorator.sublayers.append(inter)
            self.decorator.resizeComps(inter.width,True)

        return inter

    def addDecorator(self,name,resizable):
        if name:
            if self.nameExists(name):
                return False
            self.decorator = Interface((0,0),name,self.device,resizable)
            if not self.decorator:
                return False
            self.decorator.sublayers.append(self)

        return True

    def getTop(self):
        if self.decorator:
            return self.decorator.getTop()
        return self

    def focus(self):
        for comp in self.components:
            comp.dirty()

        if self.sublayer:
            self.sublayer.focus()

    def findComponentAtCoordinates(self,x,y):
        for comp in reversed(self.components):
            if positionInRectangle((x-self.x,y-self.y),comp.box()):
                return comp

        if self.sublayer:
            return self.sublayer.findComponentAtCoordinates(x,y)

        return None

    def processResize(self,component,innext):
        if component.minw:
            if not component.name in innext[0]:
                self.resizer[0].append(component)
        if component.minh:
            if not component.name in innext[1]:
                self.resizer[1].append(component)
        newfollowers = [[],[],[]]
        for dimension in component.followers:
            for name in dimension:
                fcomp = self.findComponent(name)
                if fcomp:
                    newfollowers[i].append(fcomp)
                    try:
                        self.resizer[i].remove(name)
                    except:
                        pass
        component.followers = newfollowers

        newnext = []
        for name in component.next:
            fcomp = self.findComponent(name)
            fcomp.previous = component
            if fcomp:
                newnext.append(fcomp)
        component.next = newnext

    def setresizedata(self):
        innext = [[],[]]

        for component in self.components:
            self.processResize(component,innext)

        self.minw = self.width

        for i,resizer in enumerate(self.xresizer):
            localminsize = resizer.minw
            ratiosum = resizer.ratio[0]
            nresizer = resizer.next
            while nresizer:
                localminsize+=nresizer.minw
                ratiosum+= nresizer.ratio
                nresizer = nresizer.next
            self.minw = min(self.minw,localminsize)
            self.xresizer[i] = (resizer,ratiosum)

        self.minh = self.height

        for i,resizer in enumerate(self.yresizer):
            localminsize = resizer.minh
            ratiosum = resizer.ratio
            nresizer = resizer.next
            while resizer:
                localminsize+=nresizer.minh
                ratiosum+= nresizer.ratio
                nresizer = nresizer.next
            self.minh = min(self.minh,localminsize)
            self.yresizer[i] = (resizer,ratiosum)

    def resizeComps(self,relmov,horizontal):
        if self.minw == -1:
            self.setresizedata()

        if relmov < 0:
            relmov = max(self.minw-self.width,relmov) if horizontal else max(self.minh-self.height,relmov)

        if relmov != 0:
            for component,ratiosum in self.xresizer if horizontal else self.yresizer:
                #do the math
                tores = relmov / ratiosum
                mod = relmov % ratiosum

                resizer = component
                if relmov > 0:
                    #increase in size
                    #increase size from last to beginning
                    while (resizer.next):
                        resizer = resizer.next

                    while resizer:
                        total = tores*resizer.ratio
                        minres = min(resizer.ratio,mod)
                        total+= minres
                        mod -= minres
                        if horizonal:
                            for follower in component.followers[0]:
                                follower.move(total,0)
                            resizer.resize(total,0)
                        else:
                            for follower in component.followers[1]:
                                follower.move(0,total)
                            resizer.resize(0,total)
                        resizer = resizer.previous
                else:
                    #decrease in size from first to last
                    while resizer:
                        total = tores*resizer.ratio
                        minres = min(resizer.ratio,-mod)
                        total-= minres
                        mod += minres
                        if horizonal:
                            for follower in component.followers[0]:
                                follower.move(total,0)
                            resizer.resize(total,0)
                        else:
                            for follower in component.followers[1]:
                                follower.move(0,total)
                            resizer.resize(0,total)
                        resizer = resizer.next

    def resize(self,relx,rely):
        #resize sub-layer
        for sublayer in self.sublayers:
            self.sublayer.resize(relx,rely)

        if relx != 0:
            self.resizeComps(relx,True)
            self.width += relx
        if rely != 0:
            self.resizeComps(rely,False)
            self.height += rely

        if relx or rely:
            self.surface = None

        return relx,rely

    def move(self,relx,rely):
        self.x += relx
        self.y += rely

        #move sub-layer
        if self.sublayer:
            self.sublayer.move(relx,rely)

    def updateRender(self,clean):
        if self.minimized:
            return

        self.module.update(self.device,self.components)

        if not self.surface:
            self.surface = makeSurface(max(self.width,self.minw),max(self.height,self.minh))
            self.dirty = True

        for component in self.components if self.dirty or clean else self.updated:
            self.dirty = True
            prepareComponent(component,self.surface)
        self.updated = []

        if self.sublayer:
            surf = self.sublayer.updateRender(clean)
            if surf:
                blitSurface(surf,self.surface,(self.sublayer.x-self.x,self.sublayer.y-self.y))
                self.sublayer.dirty = False
                if not self.dirty:
                    return surf

        return self.surface if self.dirty or clean else None
