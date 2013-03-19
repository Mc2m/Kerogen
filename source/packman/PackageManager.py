import os
from PackageImporter import tarfile,loadPackage
from app.KiteError import KiteError
from external.External import external
from option.Option import options

class PackageManager(object):

    def __init__(self):
        self.pkgpath = options.getOption("package_path")
        external.loadWorld(self.pkgpath)
        self.packages = []

        self.loadPackageList()

        #load packages
        for package in self.packages:
            if package[1]:
                loadPackage(os.path.join(self.pkgpath,package[0]),external)

    def loadPackageList(self):
        path = os.path.join(self.pkgpath,"packages")
        if os.path.isfile(path):
            with open(path) as pfile:
                for line in pfile:
                    if line[-1] == '\n':
                        line = line[:-1]
                    try:
                        self.packages.append((line[1:],int(line[0])))
                    except:
                        raise KiteError("Who messed with my file ?")


    def enablePackage(self, pkgname):
        try:
            self.pkgstatus[pkgname] = True
            self.syncPkgStatus()
        except:
            raise KiteError("Enabling a package that is not on the list is impressive")

    def disablePackage(self, pkgname):
        try:
            self.pkgstatus[pkgname] = False
            self.syncPkgStatus()
        except:
            raise KiteError("Disabling a package that is not on the list is impressive")

    ## install a package
    # param filename a string containing the path to the package to install
    def installPkg(self, filename):
        try:
            basename = os.path.basename(os.path.splitext(filename)[0])
            if self.pkgstatus.has_key(basename):
                print("that package has already been installed")
                return

            if zipfile.is_zipfile(filename) or os.path.isdir(filename):
                #add the name into the list
                self.pkgorder.append(basename)
                self.pkgstatus[basename] = True

                #update package file
                self.syncPkgStatus(False)

                #rewrite the datafile

                #update external
            else:
                print("Invalid file or folder.")

        except:
            print("Couldn't install %s" % (str(filename)))
            pass

    def ripPkg(name):
        with tarfile.open(name) as tfile:
            pass

    def syncPkgStatus(self,full=True):
        if full:
            with open(os.path.join(self.pkgpath,"packages"),'w') as pkgstfile:
                pkgstfile.writelines([str(int(self.pkgstatus[pkg]))+pkg+'\n' for pkg in self.pkgorder])
        else:
            with open(os.path.join(self.pkgpath,"packages"),'a') as pkgstfile:
                pkgstfile.write(str(int(self.pkgstatus[self.pkgorder[-1]]))+self.pkgorder[-1]+'\n')

    def initData():
        global path
        with open(os.path.join(path,"ExtData.py"), 'w') as extdatafile:
            extdatafile.write(
                "functionalities={}\n\n\
                MSGS = type('messages', (), {'LOAD':1,'SAVE':2,'SCREEN':3})\n\n\
                ACTIONS = type('actions', (), {'KEYDOWN':1,'KEYUP':2,'MOUSEDOWN':3,'MOUSEUP':4,'MOUSEMOVE':5})\
                FUNCTIONS = type('functions', (), {'RUNSCREEN':1,'CLOSE':2,'LAUNCH':3,'ANCHOR':4,'RESIZE':5})\
                MOUSE = type('mouse', (), {'LEFT':1,'MIDDLE':2,'RIGHT':3,'WHEELUP':4,'WHEELDOWN':5})\
                COMPONENT = type('comp', (), {'TEXT':0,'PICTURE':1,'SHAPE':2})\
                SHAPE = type('shapes', (), {'RECTANGLE':1,'ELLIPSE':4,'POLYGON':2,'CIRCLE':3,'ARC':5,'LINE':6,'AALINE':8,'LINES':7,'AALINES':9})\
                RESIZE = type('resize', (), {'HORIZONTAL':0,'VERTICAL':1,'DIAGONAL':2})"
            )

pkgman = PackageManager()
