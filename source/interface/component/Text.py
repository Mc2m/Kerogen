from interface.component.Component import Component,COMPONENT,external

class Text(Component):

    def __init__(self):
        super(Text, self).__init__()

        self.editable = False

        self.size = 11
        self.typeface = None
        self.font = None

        self.color = (255,182,0)
        self.background = None
        self.offset = 0
        self.center = True

    def setText(self, text):
        self.data = text
        self.surface = None
        self.dirty()

    def load(self,schema):
        super(Text, self).load(schema)

        if hasattr(schema,"text"):
            self.data = schema.text

        if hasattr(schema,"editable"):
            self.editable = schema.editable

        if hasattr(schema,"color"):
            self.color = (schema.color[0],schema.color[1],schema.color[2])

        if hasattr(schema,"size"):
            self.size = schema.size

        if hasattr(schema,"typeface"):
            self.typeface = external.getfontpath(schema.typeface)

        if hasattr(schema,"center"):
            self.center = schema.center

    def type(self):
        return COMPONENT.TEXT
