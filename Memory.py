#coding: "utf-8"
from collections import deque
import numpy.random as rand

class ReplayMemory:
    def __init__(self, size):
        self.buffer = []
    
    def AppendMemory(self, memory):
        self.buffer.append(memory)
    
    def getMemory(self, batchSize):
        return [self.buffer[rand.randint(0, len(self.buffer))] for i in range(batchSize) ]


