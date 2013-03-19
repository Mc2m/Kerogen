import code
import sys
from threading import Thread
from external.External import external
from world.World import world

class Interpreter(Thread):
    """interpret the commands given by a user"""

    def __init__(self, app):
        super(Interpreter,self).__init__()
        self.app = app
        self.external = external
        self.start()

    def refresh(self):
        self.app.refresh()

    def reload(self, modulename):
        external.reload(modulename)

    def debugPrint(self):
        print(self.app)

    def getWorld(self):
        return world

    def run(self):
        # use exception trick to pick up the current frame
        try:
            raise None
        except:
            frame = sys.exc_info()[2].tb_frame.f_back

        # evaluate commands in current namespace
        namespace = frame.f_globals.copy()
        namespace.update(frame.f_locals)

        self.console = code.InteractiveConsole(locals=namespace)
        self.console.interact()

        print("exited")

    def killself(self):
        self._Thread__stop()

    def __str__():
        return ""
