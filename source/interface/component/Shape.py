from interface.component.Component import Component,options
from game.Data import SHAPE,GRADIENT,COMPONENT

class Shape(Component):
    """rendering of the shapes available in pygame"""
    def __init__(self):
        super(Shape,self).__init__()

        self.subtype = 0

        self.color = (0,0,255)
        self.thicknessorblend =  0

        self.gradient = None
        self.endcolor = (255,0,0)

    def refresh(self):
        self.surface = None
        self.dirty()

    def load(self,schema):
        super(Shape, self).load(schema)

        self.subtype = eval("SHAPE.%s" % (schema.subtype))

        if hasattr(schema,'gradient'):
            self.gradient = eval("GRADIENT.%s" % (schema.gradient))
            self.endcolor = (schema.endcolor[0],schema.endcolor[1],schema.endcolor[2])

        if hasattr(schema,'color'):
            self.color = (schema.color[0],schema.color[1],schema.color[2])

        if hasattr(schema,'blend') or hasattr(schema,'thickness'):
            self.thicknessorblend = schema.thickness if schema.thickness else schema.blend

        if self.subtype == 2:   #polygon
            data = []
            for coord in schema.coordlist:
                self.width = max(coord[0],self.width)
                self.height = max(coord[1],self.height)
                self.data.append(coord[0]-self.x,coord[1]-self.y)
        elif self.subtype == 3:   #circle
            self.width = self.height = schema.radius*2
        elif self.subtype == 5:   #arc
            self.width,self.height = schema.width,schema.height
            self.data = (schema.startangle,schema.endangle)
        elif self.subtype == 6 or self.subtype == 8:   #line or antialiased line
            self.width = max(schema.startpos[0],schema.endpos[0])
            self.height = max(schema.startpos[1],schema.endpos[1])
            self.data = ((schema.startpos[0]-self.x,schema.startpos[1]-self.y),(schema.endpos[0]-self.x,schema.endpos[1]-self.y))
        elif self.subtype == 7 or self.subtype == 9:   #lines or antialiased lines
            data = []
            for coord in schema.coordlist:
                self.width = max(coord[0],self.width)
                self.height = max(coord[1],self.height)
                data.append(coord[0]-self.x,coord[1]-self.y)
            self.data = (schema.closed,data)

    def type(self):
        return COMPONENT.SHAPE
