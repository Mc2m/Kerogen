#!/usr/bin/env python

import pygame
from pygame.locals import *
from app.Data import SKEY
from Kerogen import kerogen

class Renderer:
    """handle pygame"""

    background_color

    def __init__(self):
        try:
            # pygame rendering stuff
            pygame.font.init()
            pygame.init()

            self.background_color = kerogen.getOptions().getOption('graphic_bg')
            self.width = kerogen.getOptions().getOption('screen_width')
            self.height = kerogen.getOptions().getOption('screen_height')

            self.display_surf = pygame.display.set_mode((self.width, self.height),pygame.HWSURFACE | pygame.DOUBLEBUF)
            pygame.key.set_repeat(65)

            #interface to render
            self.interfaceman = None

        except:
            print("failed to load the game engine")

    def setCaption(self,caption):
        pygame.display.set_caption(caption)

    def setInterface(self, interfaceman):
        self.interfaceman = interfaceman

    def showfps(self):
        pygame.display.set_caption("%s (%d fps)" % (
            pygame.display.get_caption(),kerogen.clock.clock.get_fps()
            )
        )

    def loadPicture(self,picfile):
        return pygame.image.load(picfile)

    def on_event(self, event):
        #print(event)
        if event.type == QUIT:
            self.interfaceman.kill()
        elif event.type == MOUSEBUTTONUP or event.type == MOUSEBUTTONDOWN:
            self.interfaceman.onClick(event.pos[0],event.pos[1],event.button,event.type == MOUSEBUTTONDOWN)
        elif event.type == MOUSEMOTION:
            self.interfaceman.onMouseMove(event.pos[0],event.pos[1],event.rel[0],event.rel[1])
        elif event.type == KEYDOWN or event.type == KEYUP:
            mod = 0
            #convert mod keys
            mod |= SKEY.SHIFT if event.mod & KMOD_SHIFT else 0
            mod |= SKEY.CTRL if event.mod & KMOD_CTRL else 0
            mod |= SKEY.LEFTALT if event.mod & KMOD_LALT else 0
            mod |= SKEY.RIGHTALT if event.mod & KMOD_RALT else 0
            self.interfaceman.onKeyPressed(event.scancode,mod,event.type == KEYDOWN)

            #print(event)

    def on_render(self):
        self.interfaceman.updateAndRender()
        pygame.display.flip()

    def render(self,surface,(x,y)):
        self.display_surf.blit(surface,(x,y))

    def loadFont(typeface,size):
        return pygame.font.Font(typeface,size)

    def blitSurface(surf,blitonsurf,x,y):
        blitonsurf.blit(surf,(x,y),special_flags=(pygame.BLEND_RGBA_ADD))

    def makeSurface(width,height):
        return pygame.Surface((width,height),pygame.HWSURFACE | pygame.SRCALPHA)

    def drawImage(self,widget):
        return pygame.transform.scale(widget.getCurrentImg(), (widget.width,widget.height))

    def drawShape(self,widget):
        scol = (widget.color[0],widget.color[1],widget.color[2],widget.alpha)
        surface = self.makeSurface(widget.width,widget.height)
        if widget.subtype == 1:     #rectangle
            pygame.draw.rect(surface,scol,(0,0,widget.width,widget.height),widget.thicknessorblend)
        elif widget.subtype == 2:   #polygon
            pygame.draw.polygon(surface,scol,widget.data,widget.thicknessorblend)
        elif widget.subtype == 3:   #circle
            pygame.draw.circle(surface,scol,(0,0),widget.width/2,widget.thicknessorblend)
        elif widget.subtype == 4:   #ellipse
            pygame.draw.ellipse(surface,scol,(0,0,widget.width,widget.height),widget.thicknessorblend)
        elif widget.subtype == 5:   #arc
            pygame.draw.arc(surface,scol,(0,0,widget.width,widget.height),widget.data[0],widget.data[1],widget.thicknessorblend)
        elif widget.subtype == 6:   #line
            pygame.draw.line(surface,scol,widget.data[0],widget.data[1],widget.thicknessorblend)
        elif widget.subtype == 7:   #lines
            pygame.draw.lines(surface,scol,widget.data[0],widget.data[1],widget.thicknessorblend)
        elif widget.subtype == 8:   #antialiased line
            pygame.draw.aaline(surface,scol,widget.data[0],widget.data[1],widget.thicknessorblend)
        elif widget.subtype == 9:   #antialiased lines
            pygame.draw.aaline(surface,scol,widget.data[0],widget.data[1],widget.thicknessorblend)
        return surface


    def notify(self):
        for event in pygame.event.get():
            #print(event)
            if self.interfaceman:
                self.on_event(event)
        if self.interfaceman:
            self.on_render()

    def __str__(self):
        return "Renderer:\nWidth:%d, Height:%d.\n" % (self.width,self.height)
