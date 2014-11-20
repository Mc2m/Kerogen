import os
from Kerogen import options,ren,app
from interface.widget.WidgetFactory import loadSchema

def getObjectOrModule(mod):
    return mod() if type(mod) is type else mod

class ResourceManager(object):

    def __init__(self):
        self.other = {} #name: (path,content)
        self.interfaces = {} #name:(module,schemafile)
        self.pictures = {} #name:(path,surface)
        self.fonts = {} #name:(file,{sizes})

    def reload(self, names):
        print("Attempting to reload %s ..." % (names))
        if type(names) is str:
            names = [names]

        #load objects individually
        for name in names:
            content = self.interfaces.get(name)
            if content:
                PI.reload(content[1])
                continue
            content = self.pictures.get(name)
            if content:
                if os.path.isfile(content[0]):
                    self.pictures[name] = (content[0],ren.loadPicture(content[0]))
                else:
                    print("Can't reload from package")
                continue
            app.

    def setDefaultInterface(self,modulefile,schemafile):
        name = os.path.splitext(os.path.split(modulefile)[1])[0]
        options.setOption(name,modulefile + ',' + schemafile)

    def loadInterface(self, modulefile,schemafile):
        name = os.path.splitext(os.path.split(modulefile)[1])[0]
        interface = self.interfaces.get(name)
        if not interface:
            #attempt to load it

            #load default if set
            opt = options.getOption(name)
            if opt:
                modulefile,schemafile = opt.split(',')

            if not os.path.isfile(schemafile):
                return None,None

            module = PI.loadModule(modulefile)
            if not module:
                return None,None

            self.interfaces[name] = interface = (modulefile,module,schemafile)

        return (getObjectOrModule(interface[1]),interface[2])

    def setDefaultPicture(self,picfile):
        name = os.path.splitext(os.path.split(picfile)[1])[0]
        options.setOption(name,picfile)

    def getPicture(self, picfile):
        name = os.path.splitext(os.path.split(picfile)[1])[0]
        pic = self.pictures.get(name)
        if not pic :
            #load picture

            #fetch default if any
            opt = options.getOption(name)
            if opt:
                picfile = opt

            if os.path.isfile(picfile):
                pic = ren.loadPicture(picfile)
                self.pictures[name] = (picfile,pic)
            else:
                print("WARNING: no picture named %s found" % (name))
                return None

        return pic[1]

    def getfont(self,typeface,size):
        font = self.fonts.get(typeface)

        if not font :
            print("WARNING: no font named %s found. Using default." % (fontname))
            typeface = options.getOption("text_typeface")
            size = options.getOption("text_size")
            font = self.fonts.get(typeface)
            if not font:
                return None

        readiedfont = font[1].get(size)
        if readiedfont:
            return readiedfont

        readiedfont = ren.loadFont(typeface,size)
        font[1][size] = readiedfont

        return readiedfont

    def addFont(self,path):
        name = os.path.splitext(os.path.split(path)[1])[0]
        self.fonts[name] = path

    def __str__(self):
        return "Interfaces: %s\n" % (str(self.interfaces))
