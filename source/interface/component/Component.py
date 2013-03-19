from game.Data import COMPONENT,ACTIONS,FUNCTIONS,MOUSE
from external.External import external
from option.Option import options

class Component(object):
    """graphical object for an interface"""

    def __init__(self):
        self.name = ""
        self.x = self.y = 0
        self.minw = self.minh = 0
        self.width = self.height = 1

        self.visible = True

        self.tooltip = ""
        self.fixedsize = (False,False)

        self.actionmapping = {}

        self.alpha = 255  #for alpha transparency

        self.data = None   #store pre-rendering data
        self.notify = None

        #resizing data
        self.followers = None
        self.next = None
        self.previous = None
        self.ratio = None

        self.surface = None

    def hide(self):
        self.visible = False
        self.dirty()

    def show(self):
        self.visible = True
        self.dirty()

    def dirty(self):
        self.notify(self)

    def addAction(self, action, function, data, restriction = None):
        if not (hasattr(function, '__call__') or type(function) is int):
            return
        flist = self.actionmapping.get(action)
        if flist:
            flist.append((function,data,restriction))
        else:
            self.actionmapping[action] = [(function,data,restriction)]

    def box(self):
        return (self.x,self.y),(self.x+self.width-1,self.y+self.height-1)

    def load(self,schema):

        if hasattr(schema,"name"):
            self.name = schema.name

        self.x = schema.x
        self.y = schema.y

        if hasattr(schema,"minw"):
            self.minw = schema.minw
        if hasattr(schema,"minh"):
            self.minh = schema.minh

        if hasattr(schema,"width"):
            self.width = schema.width
        if hasattr(schema,"height"):
            self.height = schema.height

        if hasattr(schema,"tooltip"):
            self.tooltip = schema.tooltip

        if hasattr(schema,"fixsizex"):
            self.fixedsize = (schema.fixsizex,False)
        if hasattr(schema,"fixsizey"):
            self.fixedsize = (self.fixedsize[0],schema.fixsizey)

        if hasattr(schema,"action") and hasattr(schema,"function"):
            for i,straction in enumerate(schema.action):
                action = eval("ACTIONS.%s" % (straction))
                function = schema.function[i]
                if hasattr(FUNCTIONS,function):
                    function = eval("FUNCTIONS.%s" % function)

                data,restriction = None,None
                if hasattr(schema,"data") and i < len(schema.data):
                    data = schema.data[i]

                if hasattr(schema,"restriction") and i < len(schema.restriction):
                    restriction = eval("MOUSE.%s" % schema.restriction[i]) if action == ACTIONS.MOUSEUP or action == ACTIONS.MOUSEDOWN else schema.restriction[i]

                self.addAction(action,function,data,restriction)

        if hasattr(schema,"hide"):
            self.visible = not schema.hide

        if hasattr(schema,"alpha"):
            self.alpha = schema.alpha

        if hasattr(schema,"followers"):
            self.followers = schema.followers
            self.next = schema.next
            self.ratio = schema.ratio

        self.dirty()

    def move(self,relx,rely):
        self.x += relx
        self.y += rely
        self.dirty()

    def resize(self,relx,rely):
        changed = False
        if relx and not self.fixedsize[0] and self.width+relx >= self.minw:
            changed = True
            self.width += relx
        if rely and not self.fixedsize[1] and self.height+rely >= self.minh:
            changed = True
            self.height += rely

        if changed:
            self.surface = None
            self.dirty()

    def type(self):
        return -1

    def __str__(self):
        return "Component:\nname: %s\nx:%d y: %d width: %d height: %d\n" % (self.name,self.x,self.y,self.width,self.height)
