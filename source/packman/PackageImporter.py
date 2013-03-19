## Package Importer
# import the content of a package and stores it into the external object

import os,imp,traceback,tarfile
from schemaLoader import loadSchema

## loadPackage
# Load a package
# param package the package to load
# param external the handler of external data
def loadPackage(package,external):
    if os.path.isdir(package):
        loadFolderPackage(package,external)
    elif tarfile.is_tarfile(package):
        loadTarPackage(package,external)
    else:
        print("Unrecognized package %s" %(package))

"""
    Bzip2 package importer
"""

## Load a tar package
# param package the path with the package folder
# param external the handler of external data
def loadTarPackage(package,external):
    with tarfile.open(package) as tfile:
        pass


"""
    Folder package importer
"""

## Load an extracted package
# param package the path with the package folder
# param external the handler of external data
def loadFolderPackage(package,external):
    #load the files to skip
    skipping = ['__init__']
    skippath = os.path.join(package,'skip')
    if os.path.isfile(skippath):
        with open(skippath,'r') as skipfile:
            skipping = skipfile.readlines()

    #get the functionalities
    path = os.path.join(package,'functionalities')
    if os.path.isdir(path):
        loadFunctionalitites(path, external.functionalities,skipping)

    #get the companies
    path = os.path.join(package,'company')
    if os.path.isdir(path):
        loadCompanies(path,external.companies,skipping)

    #get the interfaces
    path = os.path.join(package,'gui','interface')
    if os.path.isdir(path):
        loadInterfaces(path, external.interfaces, external.interfacetype,skipping)

    #get the pictures
    path = os.path.join(package,'gui','graphics')
    if os.path.isdir(path):
        loadGraphics(path, external.pictures,skipping)

    #get the common
    path = os.path.join(package,'data')
    if os.path.isdir(path):
        loadData(path,external.names,external.nametype,skipping)

    #get the generator that will be used in the core
    path = os.path.join(package,'generator')
    if os.path.isdir(path):
        loadGenerator(path,external.generators)

    #get the fonts
    path = os.path.join(package,'fonts')
    if os.path.isdir(path):
        loadFonts(path,external.fonts,skipping)

""" load the content of the functionalities folder of a package """
def loadFunctionalitites(path,modulelist,skipfiles):
    for root,subfolders,files in os.walk(path):
        for name in files:
            modulename,ext = os.path.splitext(name)
            if ext == '.py':
                if name not in skipfiles and modulename not in skipfiles:
                    print("Attempting to import module %s" % (name))
                    upmname = modulename.upper()

                    if not functionalities.has_key(upmname):
                        print("Error : functionality type not found")
                        continue

                    module = loadModule(modulename,root)

                    if module:
                        functionalities[upmname] = (functionalities[upmname][0],len(modulelist))
                        modulelist.append(module)

                        print("Success")

def loadCompanies(path,modulelist,skipfiles):
    for root,subfolders,files in os.walk(path):
        for name in files:
            modulename,ext = os.path.splitext(name)
            if ext == '.py':
                if name not in skipfiles and modulename not in skipfiles:
                    print("Attempting to import module %s" % (name))
                    upmname = modulename.upper()

                    if not companies.has_key(upmname):
                        print("Error : functionality type not found")
                        continue

                    module = loadModule(modulename,root)

                    if module:
                        companies[upmname] = (companies[upmname][0],len(modulelist))
                        modulelist.append(module)

                        print("Success")

""" load the content of the interface folder of a package """
def loadInterfaces(path,modulelist,nametype,skipfiles):
    for root,subfolders,files in os.walk(path):
        for name in files:
            modulename,ext = os.path.splitext(name)
            if ext == '.py':
                if name not in skipfiles and modulename not in skipfiles:
                    print("Attempting to import module %s" % (name))

                    module = loadModule(modulename,root)

                    if module:
                        #load corresponding json
                        schema = loadSchema(os.path.join(root,'%s.json' % modulename))

                        if schema:
                            modulelist.append((module,schema))

                            thistype = len(nametype)
                            nametype[modulename.upper()] = thistype

                            print("Success")

""" Load the pictures from packages"""
def loadGraphics(path,pictures,skipfiles):
    for root,subfolders,files in os.walk(path):
        for name in files:
            filename,ext = os.path.splitext(name)
            if ext in [".jpg",".png",".gif",".bmp",".pcx",".tga",".tif",".lbm",".pbm",".pgm",".ppm",".xpm"]:
                if name not in skipfiles and filename not in skipfiles:

                    print("Storing picture %s path" % (name))

                    ppath = os.path.join(root,name)
                    upname = name.upper()
                    if not pictures.get(upname):
                        #TODO set theme options
                        pictures[upname] = ppath

""" load the content of the data folder of a package """
def loadData(path,namedict,nametype,skipfiles):
    for root,subfolders,files in os.walk(path):
        for name in files:
            modulename,ext = os.path.splitext(name)
            if ext == '.txt':
                if name not in skipfiles and modulename not in skipfiles:
                    print("Attempting to read file %s" % (name))
                    try:
                        uppername = modulename.upper()

                        thistype,namelist = nametype.get(uppername),None
                        if not thistype:
                            thistype = len(nametype)
                            nametype[uppername] = thistype
                            namelist = []
                            namedict[thistype] = namelist
                        else:
                            namelist = namedict[thistype]

                        loadNames(os.path.join(root,name), namelist)

                        print("Success")
                    except:
                        print("Failed")
                        pass

def loadGenerator(path,generatorslist):
    if os.path.isfile(os.path.join(path,"Generator.py")):

        #print("Attempting to import module %s" % (name))
        module = loadModule("Generator",path)

        if module:
            try:
                module.maingenerator
                generatorslist.append(module)
                #print("Success")
            except:
                pass

def loadFonts(path,fontdict,skipfiles):

    for root,subfolders,files in os.walk(path):
        for name in files:
            fontname,ext = os.path.splitext(name)
            if ext == '.ttf':
                if name not in skipfiles and fontname not in skipfiles:
                    if not fontdict.get(fontname):
                        fontdict[fontname] = os.path.join(root,name)

def reloadFile(filename, external):

    #we need to scan through all package to find it
    print("scanning for file %s" % filename)

    with open(os.path.join(path,"packages"), 'r') as pfile:
        for line in pfile:
            if line[-1] == '\n':
                line = line[:-1]
            packagepath = os.path.join(path,line)
            pathtofile,filename = searchFileIn(filename.upper(),[os.path.join(packagepath,'functionalities'),
                                              os.path.join(packagepath,'gui','interface'),
                                              os.path.join(packagepath,'gui','graphics'),
                                              os.path.join(packagepath,'data')])
            if pathtofile:
                print("reloading file...")
                if 'functionalities' in pathtofile:
                    reloadFunctionality(pathtofile, filename,external)
                elif 'interface' in pathtofile:
                    reloadInterface(pathtofile, filename,external)
                elif 'graphics' in  pathtofile:
                    reloadGraphics(pathtofile,filename,external)
                elif 'names' in filename:
                    reloadNames(pathtofile,filename,external)
                else:
                    print("unrecognised file")

            return

    print("file not found")

def searchFileIn(filename,paths):
    for path in paths:
        for root,subfolders,files in os.walk(path):
            for name in files:
                if os.path.splitext(name)[0].upper() in filename:
                    return (root,name)
    return None

def reloadFunctionality(path,filename,external):
    if ".py" in filename:
        filename,ext = os.path.splitext(filename)

    ufname = filename.upper()

    if not functionalities.has_key[ufname]:
        print("Error : functionality type not found")

    module = loadModule(filename,path)

    if module:
        index = functionalities[ufname][1]
        if index == -1:
            index = len(external.functionalities)
            functionalities[ufname] = (functionalities[ufname][0],index)
        external.functionalities.insert(index, module)
        print("Success")

def reloadInterface(path,filename,external):
    if ".json" in filename:
        filename= "%s.py" % (filename[:-5])

    if ".py" in filename:
        filename,ext = os.path.splitext(filename)

        module = loadModule(filename,path)

        if module:
            #reload corresponding json
            schema = loadSchema(os.path.join(root,'%s.json' % filename))

            if schema:
                ufname = filename.upper()
                index = external.interfacetype.get(ufname)
                if index == None:
                    external.interfacetype[ufname] = len(external.interfaces)
                    index = len(external.functionalities)

                external.interfaces.insert(index, (module,schema))
                print("Success")

def reloadNames(unusedpath,filename,external):
    global path

    if not 'names' in filename:
        return

    if ".txt" in filename:
        partialname,ext = os.path.splitext(filename)

    #clear dictionary
    ufname = partialname.upper()
    id = external.nametype.get(ufname)
    namelist = []
    if id == None:
        id = len(external.nametype)
        external.nametype[ufname] = id

    external.names[id] = namelist

    with open(os.path.join(path,"packages"), 'r') as pfile:
        for line in pfile:
            loadNames(os.path.join(path,line,"data",filename),namelist)

def reloadGraphics(path,filename,external):

    #TODO get theme here instead of path
    external.pictures[filename] = os.path.join(path,filename)

"""test specific functions presence"""
def hasFunctions(module, functions):
    if functions == None:
        return True
    elif len(functions) == 0:
        return True
    return len(filter((lambda x: x in functions), dir(module))) == len(functions)

def loadModule(modulename, path):
    try:
        f, filename,desc = imp.find_module(modulename, [path])
        module = imp.load_module(modulename, f, filename, desc)
        f.close()

        #return the content of module importer if exists
        try:
            module.importer
            print("Importer function detected. Replacing module with importer return value.")
            module = module.importer()
        except:
            pass

        return module
    except:
        errorfile = os.path.join(path,'%s.err' %(modulename))
        print("WARNING: cannot import module. Stack trace printed in %s" % (errorfile))
        with open(errorfile, 'w') as file:
            traceback.print_exc(file=file)
        pass

    return None

"""Load names from txt"""
def loadNames(namefile,namelist):
    with open(namefile,'r') as f:
        for line in f:
            if line[-1] == '\n':
                line = line [:-1]
            namelist.append(line)
