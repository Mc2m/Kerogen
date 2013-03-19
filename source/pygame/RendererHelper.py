#!/usr/bin/env python
from lib.gameEngine.GE import pygame
from game.Data import COMPONENT,GRADIENT
from contrib.gradients.gradients import draw_gradient,vertical,horizontal

def genTextSurface(component):
    if component.text == None:
        component.text = ""

    if not component.font:
        component.font = pygame.font.Font(typeface,size)
    fontheight = component.font.get_linesize()

    if fontheight >= component.height:
        print("Warning : height too low to render anything.")
        print("Font height : %d", fontheight)
        print("Text : %s", text)
        return None

    surface = pygame.Surface((component.width,component.height),pygame.HWSURFACE | pygame.SRCALPHA)
    i = 0
    lines = text.split('\n')

    for i,line in enumerate(lines):
        if i > offset and offset + i < component.height/fontheight:
            fontwidth = font.size(line)[0]
            if fontwidth > component.width:
                currentwidth = 0
                lnsplit = line.split(" ")
                line = None
                spare = None
                for word in lnsplit:
                    if currentwidth < component.width:
                        wordsize = font.size(word)[0]
                        if wordsize >= component.width:
                            print("Warning : width too low to render word %s.", word)
                            print("Font width : %d", fontwidth)
                            return None

                        currentwidth += wordsize

                    if currentwidth >= component.width:
                        spare = "%s %s" % (spare,word) if spare else word
                    else:
                        line = "%s %s" % (line,word) if line else word

                if spare:
                    if i+1 == len(lines):
                        lines.append(spare)
                    else:
                        lines[i+1] = "%s %s" % (spare,lines[i+1])

                fontwidth = currentwidth

            tempsurf = font.render(line, False, component.color)
            rect = (0,0)
            if component.center:
                rect = ((component.width-fontwidth)/2,(i*fontheight) - component.offset)
            else:
                rect = (0,(i*fontheight) - component.offset)
            surface.blit(tempsurf,rect)

    return surface

def genPictureSurface(component):
    return pygame.transform.scale(component.getCurrentImg(), (component.width,component.height))

def renderShape(component):
    surface = None
    alpha = component.alpha
    scol = (component.color[0],component.color[1],component.color[2],alpha)
    if component.gradient:
        ecol = (component.endcolor[0],component.endcolor[1],component.endcolor[2],alpha)
        if component.gradient == GRADIENT.HORIZONTAL:
            surface = horizontal((component.width,component.height),scol,ecol)
        elif component.gradient == GRADIENT.VERTICAL:
            surface = vertical((component.width,component.height),scol,ecol)
        elif component.gradient == GRADIENT.COORDINATES:
            surface = pygame.Surface((component.width,component.height))
            draw_gradient(surface,(0,0),(component.x+component.width-1,component.y+component.height-1), scol, ecol)
        else:
            print("gradient type not recognised")

    else:
        surface = pygame.Surface((component.width,component.height))
        if component.subtype == 1:     #rectangle
            pygame.draw.rect(surface,scol,(0,0,component.width,component.height),component.thicknessorblend)
        elif component.subtype == 2:   #polygon
            pygame.draw.polygon(surface,scol,component.data,component.thicknessorblend)
        elif component.subtype == 3:   #circle
            pygame.draw.circle(surface,scol,(0,0),component.width/2,component.thicknessorblend)
        elif component.subtype == 4:   #ellipse
            pygame.draw.ellipse(surface,scol,(0,0,component.width,component.height),component.thicknessorblend)
        elif component.subtype == 5:   #arc
            pygame.draw.arc(surface,scol,(0,0,component.width,component.height),component.data[0],component.data[1],component.thicknessorblend)
        elif component.subtype == 6:   #line
            pygame.draw.line(surface,scol,component.data[0],component.data[1],component.thicknessorblend)
        elif component.subtype == 7:   #lines
            pygame.draw.lines(surface,scol,component.data[0],component.data[1],component.thicknessorblend)
        elif component.subtype == 8:   #antialiased line
            pygame.draw.aaline(surface,scol,component.data[0],component.data[1],component.thicknessorblend)
        elif component.subtype == 9:   #antialiased lines
            pygame.draw.aaline(surface,scol,component.data[0],component.data[1],component.thicknessorblend)

    return surface

def loadPicture(path):
    return pygame.image.load(path)

def prepareComponent(component,surface):
    if not component.visible:
        return
    elif component.surface:
        surface.blit(component.surface,(component.x,component.y))
        return

    if component.type() == COMPONENT.TEXT:
        if component.background:
            prepareComponent(component.background,surface)
        surf = genTextSurface(component)
    elif component.type() == COMPONENT.SHAPE:
        surf = renderShape(component)
    elif component.type() == COMPONENT.PICTURE:
        surf = genPictureSurface(component)
    surf.set_alpha(component.alpha)
    component.surface = surf
    surface.blit(surf,(component.x,component.y))

def blitSurface(surf,blitonsurf,(x,y)):
    blitonsurf.blit(surf,(x,y),special_flags=(pygame.BLEND_RGBA_ADD))

def makeSurface(width,height):
    return pygame.Surface((width,height),pygame.HWSURFACE | pygame.SRCALPHA)
