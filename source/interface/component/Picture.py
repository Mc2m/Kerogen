from interface.component.Component import Component,COMPONENT,external
from lib.gameEngine.RendererHelper import loadPicture

class Picture(Component):

    def __init__(self):
        super(Picture, self).__init__()

        self.status = 0
        self.index = 0

        self.widthset = self.heightset = False

    def changePicSet(self,index):
        self.index = index
        if type(self.data) is list:
            self.surface = None
            self.dirty()

    def getCurrentImg(self):
        if type(self.data) is list:
            return self.data[self.index][self.status]
        else:
            return self.data

    def setPictures(self,pics):
        if type(pics) in [unicode,str]:
            pic = external.getPicture(pics)
            if type(pic) is str:
                #generate the picture surface
                pic = loadPicture(pic)
                external.loadPicture(pics, pic)
            self.data = pic
            schema.img = pic
        elif type(pics) is list and type(self.getCurrentImg()) in [unicode,str]:
            for imgset in pics:
                for i,name in enumerate(imgset):
                    pic = external.getPicture(name)
                    if type(pic) is str:
                        #generate the picture surface
                        pic = loadPicture(pic)
                        external.loadPicture(name, pic)
                    imgset[i] = pic

        #get the size if needed
        size = self.getCurrentImg().get_size()
        if not self.widthset:
            self.width = size[0]
        if not self.heightset:
            self.height = size[1]

    def load(self,schema):
        super(Picture, self).load(schema)

        self.widthset = self.width != 1
        self.heightset = self.height != 1
        if hasattr(schema,'img'):
            self.data = schema.img
        if not self.data:
            self.data = "none.png"

        #load the pictures
        self.setPictures(self.data)

    def setStatus(self,highlighted,clicked):
        if clicked:
            self.status = 2
        elif highlighted:
            self.status = 1
        else:
            self.status = 0
        if type(self.data) is list:
            self.surface = None
        self.dirty()

    def type(self):
        return COMPONENT.PICTURE
