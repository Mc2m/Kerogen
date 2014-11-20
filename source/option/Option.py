####
#    Option
#
#    contains the parameters for Kite
####

from app.Data import LANGUAGE

class Options:
    def __init__(self):
        self.options = {}
        self.setDefaultOptions()

    def setOption(self,name,value):
        self.options[name] = value

    def getOption(self,name):
        return self.options.get(name,None)

    def setDefaultOptions(self):
        self.setOption("screen_width",800)
        self.setOption("screen_height",600)
        self.setOption("screen_fps", 60)
        self.setOption("screen_show_fps", 1)

        self.setOption("text_size", 11)
        self.setOption("text_typeface", "freesansbold")
        self.setOption("text_color", (255,182,0))
        self.setOption("graphic_bg", (0,0,0))

        self.setOption("shape_color", (0,0,255))
        self.setOption("shape_endcolor", (255,0,0))     #for gradients

        self.setOption("picture_default", "none.png")

        self.setOption("interface_language", LANGUAGE.ENGLISH)

        self.setOption("dev_interpreter_tools", True)
        self.setOption("dev_package_test", False)

    def load(self,optpath):
        #TODO load options
        pass
