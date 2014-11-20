#!/usr/bin/env python

class Plugin(object):

    def open(self,filename,create):
        raise "Must be defined"

    def isopen(self):
        return False

    def close(self):
        raise "Must be defined"

    def patch(self,f):
        raise "Must be defined"

    def createLink(self,parent,child,linkname):
        pass

    def prepare(self):
        pass

    def insert(self,data,flag):
        raise "Must be defined"

    def finalize(self):
        pass

    def load(self,name,iid):
        raise "Must be defined"

    def load(self,name,parentname,parentid):
        raise "Must be defined"

    def clearload(self):
        raise "Must be defined"

    def fileExtension(self):
        raise "Must be defined"
