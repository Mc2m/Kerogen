####
#    Option
#
#    contains the parameters for Kite
####

import sys
from app.Data import LANGUAGE

class Options:

    def __init__(self):
        self.options = {}

    def setOption(self,name,value):
        self.options[name] = value

    def getOption(self,name):
        return self.options[name]

    def setDefaultOptions(self):
        self.setOption("package_server",None)
        self.setOption("package_path","../packages")

        self.setOption("screen_width",800)
        self.setOption("screen_height",600)
        self.setOption("screen_fps", 60)

        self.setOption("text_size", 11)
        self.setOption("text_typeface", "freesansbold")
        self.setOption("text_color", (255,182,0))
        self.setOption("graphic_bg", (0,0,0))

        self.setOption("shape_color", (0,0,255))
        self.setOption("shape_endcolor", (255,0,0))     #for gradients

        self.setOption("interface_language", LANGUAGE.english)

        self.setOption("dev_interpreter_tools", True)
        self.setOption("dev_package_test", False)

    def load(self):
        #TODO load options
        self.setDefaultOptions()

options = Options()
options.load()
sys.path.append(options.getOption("package_path"))
