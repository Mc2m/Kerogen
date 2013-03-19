#!/usr/bin/env python

import pygame
from pygame.locals import *
#from threading import RLock

class Clock:

    def __init__(self):
        self.loop = True
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.callbacks = []

    def addNotification(self, object, delay):
        self.callbacks.append((object,delay,0.0))

    def removeNotification(self, object):
        for i,item in enumerate(self.callbacks):
            if item[0] == object:
                self.callbacks.pop(i)

    def kill(self):
        self.loop = False

    def run(self):
        while self.loop:
            for item in self.callbacks:
                item[2] += self.clock.get_time()
                if item[2] >= item[1]:
                    item[2] = 0.0
                    item[0].notify()
            self.clock.tick(self.fps)

        self.callbacks = []

        pygame.quit()

clock = Clock()

class RE:
    """handle pygame"""

    def __init__(self,fps,width,height):
        try:
            # pygame rendering stuff
            pygame.font.init()
            pygame.init()

            self.width = width
            self.height = height

            self.display_surf = pygame.display.set_mode((width, height),pygame.HWSURFACE | pygame.DOUBLEBUF)
            pygame.key.set_repeat(65)

            #interface to render
            self.interface = None

            clock.addNotification(this,1)

        except:
            print("failed to load the game engine")

    def setCaption(self,caption):
        pygame.display.set_caption(caption)

    def setInterface(self, interface):
        self.interface = interface

    def showfps(self):
        surface

    def on_event(self, event):
        #print(event)
        if event.type == QUIT:
            self.interface.kill()
        elif event.type == MOUSEBUTTONUP or event.type == MOUSEBUTTONDOWN:
            self.interface.onClick(event.pos[0],event.pos[1],event.button,event.type == MOUSEBUTTONDOWN)
        elif event.type == MOUSEMOTION:
            self.interface.onMouseMove(event.pos[0],event.pos[1],event.rel[0],event.rel[1])
        elif event.type == KEYDOWN or event.type == KEYUP:
            pass#print(event)

    def on_render(self):
        self.interface.updateAndRender()
        pygame.display.flip()

    def render(self,surface,(x,y)):
        self.display_surf.blit(surface,(x,y))

    def notify(self):
        for event in pygame.event.get():
            #print(event)
            self.on_event(event)
        if self.interface:
            self.on_render()
        pygame.display.set_caption("%d" % self.clock.get_fps())

    def __str__(self):
        return "Game Engine:\nrunning at %d fps.\n" % (self.fps)
