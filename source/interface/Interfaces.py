#!/usr/bin/env python
from app.Data import RESIZE
from lib.gameEngine.RendererHelper import prepareComponent,makeSurface,blitSurface
from Kerogen import kerogen
import interface.Interpreter as IT
from interface.widget.Widget import resizetup

class Interface(object):
    """ abstract class for interfaces """

    def __init__(self):
        self.shortcuts = {}

    def setName(self,name):
        self.name = name

    def resize(self,width,height):
        self.width = width
        self.height = height

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

class ConsoleInterface(Interface):

    def __init__(self,module):
        super(ConsoleInterface,self).__init__(module)

        self.module = module

    def resize(self,width,height):
        super(Rectangle,self).resize(width,height)
        IT.setsize(width,height)

    def setColor(self,background = '0',foreground = '0'):
        IT.setcolor(background,foreground)

    def updateRender(self,refresh):
        if hasattr(self.module,'update'):
            self.module.update()

        if hasattr(self.module,'render'):
            self.module.render()

class GUI(Interface):

    def __init__(self,iman):

        super(GUI,self).__init__()
        self.iman = iman

        self.widget = None

        self.olddimensions = None
        self.minimized = False

        self.title,self.icon = None,None

        self.surface = None

    def minimize(self):
        self.minimize = True

    def maximize(self):
        width,height = kerogen.ren.width,kerogen.ren.height
        self.olddimensions = (self.widget.x,self.widget.y,self.widget.width,self.widget.height)
        self.widget.x = self.widget.y = 0
        self.widget.resize(width-self.widget.width,height-self.widget.height)

    def restore(self):
        if self.minimize:
            self.minimize = False
        elif self.olddimensions:
            self.widget.x,self.widget.y = self.olddimensions[0],self.olddimensions[1]
            self.widget.resize(self.olddimensions[2]-self.widget.width,self.olddimensions[3]-self.widget.height)
            self.olddimensions = None

    def setTitle(self,name):
        if self.title:
            self.title.setText(name)

    def setIcon(self,name):
        if self.icon:
            self.icon.setPictures(name)

    def findWidget(self,name):
        return self.widget.findWidget(name)

    def findWidgetAtCoordinates(self,x,y):
        return self.widget.findWidgetAtCoordinates(x,y)

    def move(self,relx,rely):
        self.widget.move(relx,rely)

    def resize(self,relx,rely):
        self.widget.resize(relx,rely)

    def update(self,clean):
        if self.minimized:
            return

        self.widget.update(clean)

        return self.widget.isdirty
