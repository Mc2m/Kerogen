import threading

class SynchronizedFile(object):

    def __init__(self,path,plugin):
        self.plugin



class Synchronizer(threading.Thread):
    self.lock = threading.Lock()

    """default Constructor"""
    def __init__(self, dbfile):
        threading.Thread.__init__(self)
        self.dirty = []

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
