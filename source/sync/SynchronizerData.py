#!/usr/bin/env python

import threading
from Kerogen import kill

def OBJECT_SYNCHRONIZE():
    return 1

def makeLink(to,linkname):
    return (to,linkname)

class SynchronizedObject(object):

    def __init__(self):
        self.oid = self.delme = self.fulldeletion = 0
        self.dosynchronize = 1

        if OBJECT_SYNCHRONIZE():
            self.dirty = self.references = 0

        self.key = self.parent = None
        self.autoupdatekey = 0

    def setCollectionData(self,parent,key,database = -1,autoupdate = 0):
        if not parent:
            kill('Trying to set a collection without parent')

        self.lock()
        self.autoupdatekey = autoupdate
        self.key = key
        self.parent = parent
        self.release(database)

    def synchronize(self,database):
        pass


	void Synchronize(size_t database);

	void Deleteme(bool _fulldeletion = true,size_t database = -1);
	void Clean();

	virtual LList<DataLink *> *getLinks();

	virtual void Load(SynchronizedData *elem);
	virtual SynchronizedData *Save();

#ifdef OBJECT_SYNCHRONIZE
	void lock();
	void release(size_t database = -1);
	virtual CrissCross::System::Mutex *getMutex();
#endif

	virtual const char *getSaveName() const = 0;
};
