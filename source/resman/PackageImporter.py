## Package Importer
# import the content of a package

import os,imp,traceback,tarfile,zipfile
from kge import options

pkg_path = options.getOption("package_path")

def loadModule(resman,package,subpath,functions = None):
    modulename = os.path.splitext(os.path.split(subpath)[1])

    packagepath = os.path.join(pkgpath,package)
    subpath = os.path.join(packagepath,subpath)

    module = None

    if os.path.isdir(packagepath):
        module = loadExtractedModule(subpath)
    else:
        archive = self.getArchive(packagepath,package)
        if not archive:
            return None

    #test function presence
    if not hasFunctions(module,functions):
        print("Missing functions from module. Required functions are %s" % str(functions))
        return None

    #return the content of module importer if exists
    if hasattr(module,'importer'):
        print("Importer function detected. Replacing module with importer return value.")
        module = module.importer()

    return module

def loadArchive(resman,path):



def getArchive(self,path,name):
    archive = self.archives.get(name)
    if archive:
        return archive
    elif zipfile.is_zipfile(path):
        zf = zipfile.ZipFile(path)
        archive = {fname:zf.read(fname) for fname in zf.namelist()}
        self.archives[name] = archive
    elif tarfile.is_tarfile(path):
        tf = tarfile.TarFile(path)
        archive = {}
        for member in tf.getmembers():
            f = tf.extractfile(member)
            archive[member.name] = f.read()
            f.close()
        self.archives[name] = archive
    else:
        print("WARNING : Unrecognized package %s",path)

    return archive

"""reload Python Module"""
def reload(module):
    imp.reload(module)

"""test specific functions presence"""
def hasFunctions(module, functions):
    if functions == None:
        return True
    elif len(functions) == 0:
        return True
    return len(filter((lambda x: x in functions), dir(module))) == len(functions)

"""load Python Module"""
def loadExtractedModule(modulefile):
    try:
        path,modulename = os.path.split(modulefile)
        modulename = os.path.splitext(modulename)[0]
        f, filename,desc = imp.find_module(modulename, [path])
        module = imp.load_module(modulename, f, filename, desc)
        f.close()

        return module
    except:
        errorfile = os.path.join(path,'%s.err' %(modulename))
        print("WARNING: cannot import module. Stack trace printed in %s" % (errorfile))
        with open(errorfile, 'w') as file:
            traceback.print_exc(file=file)
        pass

    return None
