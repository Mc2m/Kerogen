#!/usr/bin/env python

from app.Data import WIDGET
from Widget import Widget
from Rectangle import Rectangle

class Composite(Widget):
    """widget used for proper resize"""

    def __init__(self):
        super(Composite,self).__init__()

        self.module = None

        self.widgetslines = ([],[])
        self.lastaccess = ([],[])

        self.redrawnwidgets = []

        self.widgets = []

    def notify(self,widget):
        self.redrawnwidgets.append(widget)
        self.dirty()

    def addWidget(self, widget):
        self.widgets.append(widget)
        self.merge(widget)
        widget.parent = self

    def computeResizeData(self,followers = None):
        lines = ([],[])
        merge = ([],[])
        for widget in self.widgets:
            findline(widget,lines[0],0)
            findline(widget,lines[1],1)

        if followers:
            for follower in followers:
                findline(follower,lines[0],0)
                findline(follower,lines[1],1)

        minwidth = processLines(self.widgetslines,lines,0)
        self.widgetslines[0].extend(firstofline)

        minheight = processLines(self.widgetslines,lines,1)
        self.widgetslines[1].extend(firstofline)

        if minwidth == -1 or minheight == -1:
            return False

        self.minwidth = width-minwidth
        self.minheight = height-minheight

        return True

    def findWidget(self,name):
        for wid in self.widgets:
            if wid.name is name:
                return wid
        return None

    def findWidgetAtCoordinates(self,x,y):
        for widget in reversed(self.widgets):
            # the widget position is relative to the interface
            if InRectangle(x-self.x,y-self.y):
                if widget.type() == WIDGET.GROUP:
                    return widget.findWidgetAtCoordinates(x,y)
                else:
                    return widget

        return None

    def move(self,relx,rely):
        for widget in self.widgets:
            widget.move(relx,rely)

    def resize(self,relx,rely):
        super(Composite,self).resize(relx,rely)

        if relx == 0 and self.minwidth != -1:
            self.dimensionResize(relx,0)

        if rely == 0 and self.minheight != -1:
            self.dimensionResize(rely,1)

    def dimensionResize(self,rel,dimension):
        for i,line,last in enumerate(zip(self.widgetslines[dimension],self.lastaccess[dimension])):
            local = rel

            #continue from last
            if previous:
                local,last = resizeLast(last,resizeamount,dimension)
                self.lastaccess[dimension][i] = last

                if local == 0:
                    continue

            self.lastaccess[dimension][i] = resizeLine(line,local,dimension)

    def update(self,clean):
        if self.module:
            if hasattr(self.module,"update"):
                self.module.update(self.widget)

        if clean:
            self.clean()

        for widget in reversed(self.widgets):
            widget.update(self.redrawnwidgets)
            if clean:
                widget.clean()

    def save(self):
        pass

    def load(self):
        pass

    def type(self):
        return WIDGET.GROUP

    def __str__(self):
        return "Group widget:\nwidgets: %s\n" % str(self.widgets)


def resizeLast(last,resizeamount,dimension):
    resdata = last.resizedata[dimension]
    remaining = resdata.remaining%resdata.ratio

    #resize last
    rel = min(resdata.ratio-remaining,resizeamount) if resizeamount > 0 else -min(remaining,-resizeamount)
    last.resize(rel,0) if dimension == 0 else last.resize(0,rel)
    resizeamount -= rel

    #resize next widgets
    last = resdata.previous if resizeamount > 0 else resdata.next
    while last and resizeamount != 0:
        resdata = last.resizedata[0]

        rel = min(resdata.ratio,resizeamount) if resizeamount > 0 else -min(resdata.ratio,-resizeamount)
        last.resize(rel,0) if dimension == 0 else last.resize(0,rel)
        resizeamount -= rel

        last = resdata.previous if resizeamount > 0 else resdata.next

    return resizeamount,last

def resizeLine(line,localamount,dimension):
    ratiosum,first,last = line

    loops = localamount/ratiosum #number of complete loops for resize
    remaining = localamount%ratiosum #remaining amount
    setremaining = remaining != 0
    lastmodified = None

    current = first if localamount < 0 else last
    while current and (loops > 0 or remaining > 0):
        resdata = current.resizedata[dimension]

        #amount taken from remaining
        resizeamount = min(resdata.ratio,remaining) if remaining > 0 else -min(resdata.ratio,-remaining)
        remaining -= resizeamount

        #detect last
        if remaining == 0 and setremaining:
            lastmodified = current
            setremaining = False

        #amount given by the loops
        resizeamount += loops*resdata.ratio

        current.resize(resizeamount,0)
        current = resdata.previous if localamount < 0 else resdata.next

    return lastmodified


def findline(widget,lines,dimension):
    firstline = None
    for i,line in enumerate(reversed(lines)):
        rect = line[0]
        if ((not dimension and widget.yOverlay(rect)) or
            (dimension and widget.xOverlay(rect))):
            if widget.minwidth == -1:
                #follower
                line[2].append(widget)
                break
            else:
                #update rectangle
                rect.merge(widget)

                if firstline:
                    del lines[len(mlist)-1-i]

                    firstline[1].extend(line[1])
                    firstline[0].merge(line[0])
                    firstline[2].extend(line[2]) #add followers
                else:
                    line[1].append(widget)
                    firstline = line

    #create new line
    line = (Rectangle(widget.x,widget.y,widget.width,widget.height),[],[])
    line[0].minwidth = 0
    if widget.minwidth == -1:
        line[2].append(widget)
    else:
        line[1].append(widget)
    lines.append(line)

def processGroup(group,followers,dimension,widgets):
    counter = 0
    followersingroup = []
    rezdata = group.resizedata[dimension]
    for follower in followers:
        if (
            (follower.x < group.x and not dimension) or
            (follower.y < group.y and dimension)
            ):
            counter +=1
        elif group.type() == WIDGET.GROUP and group.intersect(follower):
            followersingroup.append(follower)
        else:
            rezdata.followers.append(follower)

    for widget in widgets:
        if ((dimension == 0 and group.yOverlay(widget)) or
            (dimension == 1 and group.xOverlay(widget))):
            rezdata.followers.append(follower)


    if group.type() == WIDGET.GROUP:
        if not group.computeResizeData(followersingroup):
            return 0,-1

    return counter,group.minheight if dimension else group.minwidth,group.height if dimension else group.width

def processRatio(groups,dimension):
    localminsize = 0
    ratiosum = 0
    if dimension:
        groups.sort(key=lambda widget: widget.height)
        localminsize = groups[0].height - groups[0].minheight
    else:
        groups.sort(key=lambda widget: widget.width)
        localminsize = groups[0].width - groups[0].minwidth

    for i,group in enumerate(groups):
        resizedata = group.resizedata[dimension]
        resizedata.remaining = group.height-group.minheight if dimension else group.width-group.minwidth
        resizedata.ratio = resizedata.remaining/localminsize
        ratiosum += resizedata.ratio

        if i+1 < len(groups):
            resizedata.previous = groups[i+1]
            groups[i+1].next = group

    return ratiosum,groups[-1],groups[0]

def groupWidgets(widgets,followers,groupid,dimension):
    groups = []
    group = None
    lineminsize = linesize = 0

    for i,widget in enumerate(widgets):
        if group and (
            (not dimension and group.xOverlay(widget)) or
            (dimension and group.yOverlay(widget))): #belong in group
            if group.type() != WIDGET.GROUP:
                #create new group
                groupid +=1
                newgroup = Composite()
                newgroup.addWidget(group)
                group.resizedata[dimension].group = newgroup
                group = newgroup
                group.name = 'group %d' % groupid

            group.addWidget(widget)
        else:
            if group:
                groups.append(group)

                #process group
                counter,localminsize,currentsize = processGroup(group,followers,dimension,widgets[i:])
                if localminsize == -1:
                    return [],-1

                followers = followers[counter:]
                lineminsize += localminsize
                linesize += currentsize

            group = widget

    return groups,group,groupid,lineminsize,linesize


def processLines(widgetslines,lines,dimension):
    minsize = -1
    groupid = 0
    for line in lines[dimension]:
        if len(line[1]) == 0:
            continue

        widgets = followers = None

        if dimension:
            widgets = sorted(line[1],key=lambda widget: widget.y)
            followers = sorted(line[2],key=lambda widget: widget.y)
        else:
            widgets = sorted(line[1],key=lambda widget: widget.x)
            followers = sorted(line[2],key=lambda widget: widget.x)

        groups,group,groupid,lineminsize,linesize = groupWidgets(widgets,followers,groupid,dimension)

        if len(groups) == 0 and len(line[1]) != 1:
            print("Error: resize line cannot be processed. Fix the line or manually set the resize parameters.")
            print("\tconcerned widgets are : %s" % str(line[1]))
            return [],-1

        #process last group
        counter,localminsize,currentsize = processGroup(group,followers,dimension)
        if localminsize == -1:
            return [],-1

        lineminsize += localminsize
        linesize += currentsize
        minsize = linesize-lineminsize if minsize == -1 else min(minsize,linesize-lineminsize)

        groups.append(group)

        #process ratio and resize order
        widgetslines.append(processRatio(groups,dimension))

    return minsize

