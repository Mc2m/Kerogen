import sqlite3
import threading
from app.MiscUtils import enum

P = enum(KEY=0,FKEY=1,LEN=2,NULL=3,INDEX=4)
STATUS = enum(INSERT=0,DELETE=1)

class Synchronizer(threading.Thread):

    """default Constructor"""
    def __init__(self, dbfile, syncThreshold = 1000):
        threading.Thread.__init__(self)
        self.db = sqlite3.connect(dbfile)
        self.syncThreshold = syncThreshold
        self.dirty = []

        self.lock = threading.Lock()

        self.event = threading.Event()
        self.event.clear()

    def __del__(self):
        self.synchronize()
        self.db.close()

    """Put an item to be synchronized"""
    def addDirty(self, object, status):
        self.lock.aquire()
        self.dirty.append([object,status])
        self.lock.release()

        if len(self.dirty) >= self.syncThreshold:
            self.event.set()

    """run thread, run"""
    def run(self):
        while True:
            self.event.wait()
            self.event.clear()
            self.synchronize()

    """force the synchronization"""
    def forceSynchronize(self):
        self.event.set()

    """do the synchronization"""
    def synchronize(self):
        """copy the dirty list"""
        self.lock.aquire()
        newlist = [dirty for dirty in self.dirty]
        self.dirty = []
        self.lock.release()
        for item in newlist:
            return None

