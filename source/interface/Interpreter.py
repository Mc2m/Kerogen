import code,sys,os
from threading import Thread
from packman.External import external

#debug commands

def setTitle(name):
    os.system("TITLE " + name)

def setsize(cols,lines):
    #get current size
    os.system("mode con: cols=%d lines=%d" % (cols,lines))

def setcolor(background,foreground):
    #get current size
    os.system("color %s%s" % (background,foreground))

def setDate(date):
    os.system("date " + date)

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def reload(modulename):
    external.reload(modulename)

def World():
    return external.world

def run(parameters):
    print('running %s...' % (parameters))

class Interpreter(Thread):
    """interpret the commands given by a user"""
    """both game and debug commands are possible"""

    def __init__(self,kge):
        super(Interpreter,self).__init__()
        self.commands = []
        self.commandmap={}
        self.mapCommands()

        self.kge = kge

        self.banner = "Kerogen Version 0.1"
        self.setTitle("Kerogen")

        self.defaultsize = (80,25)
        self.restore() #make sure about the size

        self.nodebug()

        self.console = code.InteractiveConsole(locals=self.debugCommands())
        self.consolepush = self.console.push
        self.console.push = self.push

    def refresh(self):
        self.kge.iman.refresh()

    def Print(self):
        self.kge.Print()

    def debug(self,param):
        self.debugmode = True
        sys.ps1 = ">>> "

    def nodebug(self):
        self.debugmode = False
        sys.ps1 = "Kerogen: "

    def debughelp(self):
        print("help         Display this list of command\n"
              "nodebug      switch to game console\n"
              "print        Print the game engine informations\n"
              "refresh      Refresh the whole graphical interface\n")

    def restore(self):
        self.setsize(self.defaultsize[0],self.defaultsize[1])

    def mapCommands(self):
        self.commandmap['run'] = run
        self.commandmap['print'] = Print
        if kge.options.getOption('dev_interpreter_tools'):
            self.commandmap['debug'] = self.debug
        self.commandmap['cls'] = cls
        self.commandmap['clear'] = cls

    def debugCommands(self):
        return {
            'nodebug':self.nodebug,
            'print':self.Print,
            'refresh':self.refresh,
            'help':self.debughelp,
            }

    def execute(self,command):
        print(command)

    def push(self,command):
        if self.debugmode:
            self.consolepush(command)
        else:
            split = command.split(' ', 1)
            command = split[0]
            parameters = None if len(split) == 1 else split[1]
            command = self.commandmap.get(command)
            if not command:
                print('no such command')
            else:
                command(parameters)
            self.console.resetbuffer()

            #self.commands.append(command)

    def run(self):
        self.console.interact(self.banner)

        #print("exited")

    def __str__():
        return ""
