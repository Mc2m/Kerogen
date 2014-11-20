from Widget import Widget,WIDGET

class Text(Widget):

    default_color = options.getOption("text_color")
    default_typeface = options.getOption("text_typeface")
    default_size = options.getOption("text_size")

    def __init__(self):
        super(Text, self).__init__()

        self.editable = 0
        self.clear = 1

        self.size = self.default_size
        self.typeface = self.default_typeface
        self.font = None

        self.color = self.default_color
        self.offset = 0
        self.center = 1
        self.verticalspacing = 5

    def setText(self, text):
        self.data = text
        self.surface = None
        self.dirty()

    def save(self):
        pass


    def load(self,schema):
        super(Text, self).load(schema)

        if hasattr(schema,"text"):
            self.data = schema.text

        if hasattr(schema,"editable"):
            self.editable = int(schema.editable)

        if hasattr(schema,"clear"):
            self.clear = int(schema.clear)

        if hasattr(schema,"color"):
            self.color = (schema.color[0],schema.color[1],schema.color[2])

        if hasattr(schema,"size"):
            self.size = schema.size

        if hasattr(schema,"typeface"):
            self.typeface = schema.typeface
        self.font = external.getFont(self.typeface)

        if hasattr(schema,"center"):
            self.center = int(schema.center)

        if hasattr(schema,"verticalspacing"):
            self.verticalspacing = schema.verticalspacing

    def type(self):
        return WIDGET.TEXT
