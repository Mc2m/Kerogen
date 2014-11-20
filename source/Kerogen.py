#!/usr/bin/env python

from option.Option import Options
from interface.InterfaceManager import iman
from renderer.Renderer import Renderer
from ResourceManager import resman
from Clock import clock
from interface.Interpreter import Interpreter
from sync.Synchronizer import Synchronizer

VERSION = '0.0.1'

class Kerogen(object):

    def __init__(self):
        self.app = None
        self.options = Options()
        self.iman = self.ren = self.interpreter = None
        self.resman = self.clock = None

    def setOptions(self,optpath):
        self.options.load(optpath)

    def getOptions(self):
        return self.options

    def start(self,application):
        self.app = application
        self.ren = Renderer()

        self.interpreter = Interpreter(self)
        self.interpreter.start()

kerogen = Kerogen()

def start(application,optpath):
    global app
    app = application

    options.load(optpath)

    ren = Renderer()
    ren.setScreenSize(options.getOption('screen_width'),options.getOption('screen_height'))

    iman.setResourceManager(resman)
    iman.setRenderer(ren)

    clock.fps = options.getOption("screen_fps")
    clock.addNotification(ren,0)
    clock.start()

    it.start()

def kill(msg = None):
    pass #TODO

def Print():
    print("Kerogen")
    print("Version: %f" % (VERSION))
