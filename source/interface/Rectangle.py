#!/usr/bin/env python

#define basis for rectangles

class Rectangle(object):

    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.minwidth = self.minheight = -1

    def setMinSize(self,minwidth,minheight):
        self.minwidth = minwidth
        self.minheight = minheight

    def resize(self,width,height):
        self.width = max(width,self.minwidth)
        self.height = max(height,self.minheight)

    def box(self):
        return (self.x,self.y,self.x+self.width,self.y+self.height)

    def overlay(self,rectangle):
        box = rectangle.box()
        return (
            (box[0] >= self.x and box[2] <= self.x+self.width) and
            (box[1] >= self.y and box[3] <= self.y+self.height)
        )

    def xOverlay(self,rectangle):
        box = rectangle.box()
        return box[2] >= self.x and box[0] <= self.x+self.width

    def yOverlay(self,rectangle):
        box = rectangle.box()
        return box[3] >= self.y and box[1] <= self.y+self.height

    def intersection(self,rectangle):
        box = rectangle.box()
        inter = None

        if (box[2] <= self.x+self.width  and box[0] >= self.x and
            box[3] <= self.y+self.height and box[1] >= self.y):
            x = max(self.x,box[0][0])
            y = max(self.y,box[0][1])
            width  = min(self.x+self.width ,box[2]) - x
            height = min(self.y+self.height,box[3]) - y
            inter = Rectangle(x,y,width,height)

        return inter

    def intersect(self,rectangle):
        box = rectangle.box()

        return (box[2] <= self.x+self.width  and box[0] >= self.x and
                box[3] <= self.y+self.height and box[1] >= self.y)

    def xIntersect(self,rectangle):
        box = rectangle.box()
        return box[2] <= self.x+self.width and box[0] >= self.x

    def yIntersect(self,rectangle):
        box = rectangle.box()
        return box[3] <= self.y+self.height and box[1] >= self.y

    def inRectangle(self,x,y):
        return (
            x >= self.x and
            x <= self.x+self.width and
            y >= self.y and
            y <= self.y+self.height
        )

    def merge(self,rectangle):
        oldy = self.y
        self.y = min(self.y,rectangle.y)
        self.height = max(oldy + self.height,rectangle.y + rectangle.height) - self.y

        oldx = self.x
        self.x = min(self.x,self.x)
        self.width = max(oldx + self.width,rectangle.x + rectangle.width) - self.x

    def __str__(self):
        return 'Rectangle: x: %s, y:%s, width:%s, height:%s, min width:%s, min height: %s' % (self.x,self.y,self.width,self.height,self.minwidth,self.minheight)
