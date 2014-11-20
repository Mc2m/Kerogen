#!/usr/bin/env python

import pygame
import threading

class Clock(threading.Thread):

    def __init__(self):
        super(Clock,self).__init__()

        self.loop = True
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.callbacks = []

    def addNotification(self, obj, delay):
        self.callbacks.append((obj,delay,0.0))

    def removeNotification(self, obj):
        for i,item in enumerate(self.callbacks):
            if item[0] == obj:
                self.callbacks.pop(i)

    def kill(self):
        self.loop = False

    def run(self):
        while self.loop:
            for i,item in enumerate(self.callbacks):
                ctime = item[2] + self.clock.get_time()
                if ctime >= item[1]:
                    ctime = 0.0
                    item[0].notify()
                self.callbacks[i] = (item[0],item[1],ctime)

            self.clock.tick(self.fps)

        self.callbacks = []

        pygame.quit()
