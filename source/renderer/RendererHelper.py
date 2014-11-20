#!/usr/bin/env python
from app.Data import WIDGET,GRADIENT
from contrib.gradients.gradients import draw_gradient,vertical,horizontal
from Kerogen import kerogen

def splitLine(widget,line):
    currentwidth = 0
    lnsplit = line.split(" ")

    for i,word in enumerate(lnsplit):
        wordsize = widget.font.size(word)[0]

        if wordsize >= widget.width:
                print("Warning : width too low to render word %s.", word)
                print("Word size : %d,Widget Width: %d", wordsize,widget.width)
                return 0,None,None

        currentwidth += wordsize

        if currentwidth >= widget.width:
            return currentwidth,' '.join(lnsplit[:i]),' '.join(lnsplit[i:])

    return 0,None,None

def splitSpare(widget,spare):
    currentwidth = 0
    lnsplit = spare.split(" ")
    spares = []
    lastsplit = 0

    for i,word in enumerate(lnsplit):
        wordsize = widget.font.size(word)[0]

        if wordsize >= widget.width:
                print("Warning : width too low to render word %s.", word)
                print("Word size : %d,Widget Width: %d", wordsize,widget.width)
                return None

        currentwidth += wordsize

        if currentwidth >= widget.width:
            spares.append(' '.join(lnsplit[lastsplit:i]))
            currentwidth = 0
            lastsplit = i

    return spares

def renderLines(widget,surface,lines):
    spare = None
    counter = 0
    fontheight = widget.font.get_linesize()

    for line in lines:
        if spare:
            line = "%s %s" % (spare,line)
            spare = None

        fontwidth = widget.font.size(line)[0]
        if fontwidth > widget.width:
            fontwidth,line,spare = splitLine(widget,line)
            if fontwidth == 0:
                return 1

        tempsurf = widget.font.render(line, False, widget.color)
        rectx = (widget.width-fontwidth)/2 if widget.center else 0
        rect = (rectx,counter*fontheight + widget.verticalspacing)
        surface.blit(tempsurf,rect)
        counter +=1

    if spare:
        maxnumlines = widget.height/fontheight
        if maxnumlines-counter > 0:
            fontwidth = widget.font.size(spare)[0]

            if fontwidth > widget.width:
                spare = splitSpare(widget,spare)
                if not spare:
                    return 1

            spare = spare[:maxnumlines-counter]
            renderLines(widget,surface,spare)

    return 0

def genTextSurface(widget):
    if widget.text == None:
        widget.text = ""

    renderer = kerogen.resman

    if not widget.font:
        widget.font = renderer.getfont(typeface,size)
    fontheight = widget.font.get_linesize()

    if fontheight >= widget.height:
        print("Warning : height too low to render anything.")
        print("Font height : %d, Widget Height : %d", fontheight, widget.height)
        print("Text : %s", text)
        return None

    offset = widget.offset
    maxnumlines = widget.height/fontheight
    lines = text.split('\n')[offset:offset + maxnumlines]

    surface = renderer.makeSurface(widget.width,widget.height)
    success = renderLines(widget,surface,lines)

    if success != 0:
        surface = None

    return surface

def genPictureSurface(widget):
    renderer = kerogen.resman

    surf = renderer.drawImage(widget)
    surf.set_alpha(widget.alpha)
    return surf

def renderShape(widget):
    renderer = kerogen.resman
    surface = None
    scol = (widget.color[0],widget.color[1],widget.color[2],widget.alpha)

    if widget.gradient:
        ecol = (widget.endcolor[0],widget.endcolor[1],widget.endcolor[2],widget.alpha)
        if widget.gradient == GRADIENT.HORIZONTAL:
            surface = horizontal((widget.width,widget.height),scol,ecol)
        elif widget.gradient == GRADIENT.VERTICAL:
            surface = vertical((widget.width,widget.height),scol,ecol)
        elif widget.gradient == GRADIENT.COORDINATES:
            surface = renderer.makeSurface(widget.width,widget.height)
            draw_gradient(surface,(0,0),(widget.x+widget.width-1,widget.y+widget.height-1), scol, ecol)
        else:
            print("gradient type not recognised")
    else:
        surface = renderer.drawShape(widget)

    return surface

def prepareWidget(widget):
    if not (isdirty and widget.visible) or w.surface:
        return

    if widget.drawfunc:
        surf = widget.drawfunc(widget)
    elif widget.type() == WIDGET.TEXT:
        surf = genTextSurface(widget)
    elif widget.type() == WIDGET.SHAPE:
        surf = renderShape(widget)
    elif widget.type() == WIDGET.PICTURE:
        surf = genPictureSurface(widget)

    widget.surface = surf

def renderWidget(widget):
    if widget == None:
        return

    renderer = kerogen.resman

    if widget.surface == None:
        widget.surface = renderer.makeSurface(widget.width,widget.height)
        widget.surface.fill(renderer.background_color)
    else:
        for w in widget.redrawnwidgets:
            dimensions = (w.x,w.y,w.width,w.height)
            pygame.draw.rect(widget.surface,renderer.background_color,dimensions)
    widget.redrawnwidgets = []

    for w in reversed(widget.widgets):
        if w.isdirty:
            if w.type() == WIDGET.GROUP:
                renderWidget(w)
            else:
                prepareWidget(w)

            if w.visible:
                renderer.blitSurface(w.surface,widget.surface,w.x,w.y)
            w.isdirty = 0
