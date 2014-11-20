from app.Data import WIDGET
from kge import options,external
from interface.Rectangle import Rectangle

class ResizeData(object):

    def __init__(self):
        self.group = None
        self.next = None
        self.previous = None
        self.followers = []

        self.ratio = 0
        self.remaining = 0

    def save(self):
        return {
            'group'    : self.group.name if self.group else None,
            'next'     : self.next.name if self.next else None,
            'previous' : self.previous.name if self.previous else None,
            'followers': str([item.name for item in self.followers]),
            'ratio'    : self.ratio,
        }


    def load(self,schema):
        self.group = schema.group
        self.next = schema.next
        self.previous = schema.previous
        self.followers = schema.followers
        self.ratio = schema.ratio

    def moveFollowers(self,relx,rely):
        for follower in self.followers:
            follower.move(relx,rely)

class Widget(Rectangle):
    """graphical object for an interface"""

    def __init__(self):
        super(Widget,self).__init__(0,0,1,1)
        self.name = ""

        self.parent = None
        self.isdirty = 1

        self.visible = 1

        self.tooltip = ""

        self.actionmapping = {}

        self.alpha = 255  #for alpha transparency

        self.data = None   #store pre-rendering data

        self.resizedata = (None,None)

        self.surface = None
        self.drawfunc = None

    def hide(self):
        self.visible = 0
        self.surface = None
        self.dirty()

    def show(self):
        self.visible = 1
        self.surface = None
        self.dirty()

    def dirty(self, notify = 1):
        if not self.isdirty:
            self.isdirty = 1
            if notify and self.parent:
                self.parent.notify(self)

    def clean(self):
        self.isdirty = 1
        self.surface = None

    def addAction(self, action, function, data, restriction = None):
        flist = self.actionmapping.get(action)
        if flist:
            flist.append((function,data,restriction))
        else:
            self.actionmapping[action] = [(function,data,restriction)]

    def move(self,relx,rely):
        changed = relx or rely

        self.x += relx
        self.y += rely

        if changed:
            self.dirty()

    def resize(self,relx,rely):
        changed = False
        if relx and self.minwidth != -1:
            oldwidth,rezdata = self.width,self.resizedata[0]

            if rezdata.remaining < 0:
                rezdata.remaining += relx
                self.width = max(self.width+rezdata.remaining,self.minwidth)
            else:
                self.width = max(self.width+relx,self.minwidth)
                rezdata.remaining += relx

            rezdata.moveFollowers(relx,0)

            changed = oldwidth != self.width

        if rely and self.minheight != -1:
            oldheight,rezdata = self.height,self.resizedata[1]

            if rezdata.remaining < 0:
                rezdata.remaining += rely
                self.height = max(self.height+rezdata.remaining,self.minheight)
            else:
                self.height = max(self.height+rely,self.minheight)
                rezdata.remaining += rely

            rezdata.moveFollowers(0,rely)

            changed = changed or oldheight != self.height

        if changed:
            self.surface = None
            self.dirty()

    def update(self,redrawnareas):
        if not self.isdirty:
            for i,area in enumerate(redrawnareas):
                if area.overlay(self):
                    intersect = self.intersect(area)
                    if area.intersect(self):
                        redrawnareas[i] = self
                        intersect = 1
                    self.dirty(not intersect)

                    break

    def saveActions(self):
        data = {}
        for key,value in self.actionmapping.items():
            data[key] = [(item[0].func_name,item[1],item[2]) for item in value]

        return str(data)

    def save(self):
        data = {
            'name'    : self.name,
            'tooltip' : self.tooltip,
            'x'       : self.x,
            'y'       : self.y,
            'width'   : self.width,
            'height'  : self.height,
            'hidden'  : not self.visible,
            'alpha'   : self.alpha,
            'actions' : self.saveActions(),
        }

        if self.minwidth:
            data['minw'] = self.minwidth
            data['resizedatax'] = self.resizedata[0].save()

        if self.minheight:
            data['minh'] = self.minheight
            data['resizedatay'] = self.resizedata[1].save()

    def load(self,schema):

        self.name = schema.name
        self.tooltip = schema.tooltip

        self.x = schema.x
        self.y = schema.y

        self.width = schema.width
        self.height = schema.height

        self.visible = not schema.hidden

        self.alpha = schema.alpha

        if hasattr(schema,'minw'):
            self.minwidth = schema.minw
            self.resizedata = (ResizeData(),None)
            self.resizedata[0].load(schema.resizedatax)

        if hasattr(schema,'minh'):
            self.minheight = schema.minh
            self.resizedata = (self.resizedata[0],ResizeData())
            self.resizedata[1].load(schema.resizedatay)

    def type(self):
        return -1

    def __str__(self):
        return "Component:\nname: %s\nx:%d y: %d width: %d height: %d\n" % (self.name,self.x,self.y,self.width,self.height)
