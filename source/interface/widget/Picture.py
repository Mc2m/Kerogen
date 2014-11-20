from Widget import Widget,WIDGET

class Picture(Widget):

    #default_picture = options.getOption("picture_default")

    def __init__(self):
        super(Picture, self).__init__()

        self.index = 0
        self.status = 0

        self.widthset = self.heightset = 0

    def changePicSet(self,index):
        if type(self.data) is list and self.index != index:
            self.index = index
            self.surface = None
            self.dirty()

    def getCurrentImg(self):
        if type(self.data) is list:
            return self.data[self.index][self.status]
        elif type(self.data) is tuple:
            return self.data[self.status]
        else:
            return self.data

    def setPictures(self,pics):
        if type(pics) in [unicode,str]:
            pic = external.getPicture(pics)
            if not pic:
                print("failed to load picture %s" % (pics))
                if default_picture != pics:
                    setPictures(default_picture)
                else:
                    raise "default picture not found."
            self.data = pic
        elif type(pics) is list and type(self.getCurrentImg()) in [unicode,str]:
            self.data = []
            for imgset in pics:
                piclist = []
                for i,name in enumerate(imgset):
                    if name in [unicode,str]:
                        pic = external.getPicture(name)
                        if not pic:
                            print "failed to load picture %s" % (pics)
                            pic = external.getPicture(default_picture)
                            if not pic:
                                raise "default picture not found."
                        piclist.append(pic)
                    else:
                        raise "wrong string format"
                self.data.append(piclist)
        else:
            raise "failed to load pictures %s" % (pics)

        #get the size if needed
        size = self.getCurrentImg().get_size()
        if not self.widthset:
            self.width = size[0]
        if not self.heightset:
            self.height = size[1]

    def load(self,schema):
        super(Picture, self).load(schema)

        self.widthset = int(self.width != 1)
        self.heightset = int(self.height != 1)

        data = default_picture
        if hasattr(schema,'img'):
            data = schema.img

        #load the pictures
        self.setPictures(data)

    def setStatus(self,highlighted,clicked):
        changed = False
        if clicked:
            changed = self.status != 2
            self.status = 2
        elif highlighted:
            changed = self.status != 1
            self.status = 1
        else:
            changed = self.status != 0
            self.status = 0
        if changed and type(self.data) is list:
            self.surface = None
            self.dirty()

    def type(self):
        return WIDGET.PICTURE
