import imp
import PackageImporter as PI

def getObjectOrModule(list, index):
    func = list[index]
    return func() if type(func) is type else func

class External(object):

    def __init__(self):
        self.interfaces = {} #name:(path,module)
        self.pictures = {} #name:(path,surface)
        self.conflict = {} #name:[files]
        self.fonts = {} #name:(path,rendererfont)
        self.world = None

    def loadWorld(self,pkgpath):
        f, filename,desc = imp.find_module("World", [path])
        w = imp.load_module("World", f, filename, desc)
        f.close()
        self.world = w.world

    def reload(self, names):
        print("Attempting to reload %s ..." % (names))
        if type(names) is str:
            names = [names]

        #load modules individually
        for name in names:
            content = self.interfaces.get(name)
            if content:
                self.interfaces[name] = (content[0],PI.load(content[0]))
                continue
            content = self.pictures.get(name)
            if content:
                self.pictures[name] = (content[0],PI.load(content[0]))
                continue
            self.world.reload(name)

    def getInterface(self, name):
        interface = self.interfaces.get(name)
        if not interface:
            print("WARNING: no interface %s found" % (name))
            return None

        if not interface[1]:
            interface
        interface = interface[1]

        return interface() if type(interface) is type else interface,self.interfaces[index][1]

    def getPicture(self, name):
        pic = self.pictures.get(name.upper())
        if not pic :
            print("WARNING: no picture named %s found" % (name))

        return pic

    def loadPicture(self, name, sdlsurface):
        self.pictures[name.upper()] = sdlsurface

    def getfontpath(self,fontname):
        fontpath = self.fonts.get(fontname)
        if not fontpath :
            print("WARNING: no font named %s found" % (fontname))

        return fontpath

    def __str__(self):
        return "Functionalities: %s\nInterfaces: %s\n" % (str(self.functionalities),str(self.interfaces))

external = External()
