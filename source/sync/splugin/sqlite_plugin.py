#!/usr/bin/env python

import sqlite3
import os
from collections import namedtuple

class SQLite_Plugin(object):

    Table = namedtuple('Table', ['name', 'size', 'checked'])

    def __init__(self):
        super(SQLite_Plugin,self).__init__()
        self.db = None
        self.c = None
        self.tables = {}

    def open(filename,create):
        if not create and not os.path.isfile(filename):
            return False

        self.db = sqlite3.connect(filename)

        if self.db:
            self.c = self.db.cursor()

            if self.c:

                self.c.execute("PRAGMA foreign_keys = ON")
                self.c.execute("PRAGMA journal_mode = MEMORY")
                self.c.execute("PRAGMA synchronous = OFF")
                self.c.execute("SQLITE_ENABLE_STAT3")
                self.loadTableData()

                return True

        return False


    def isopen():
        return self.db != None

    def close():
        raise "Must be defined"

    def patch(f):
        raise "Must be defined"

    def prepare():
        pass

    def insert(data,options):
        raise "Must be defined"

    def finalize():
        pass

    def load(name,iid):
        raise "Must be defined"

    def load(name,oname,iid):
        raise "Must be defined"

    def clearload():
        raise "Must be defined"

    def fileExtension():
        raise "Must be defined"
