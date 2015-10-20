import random
import math
import operator
import functools

import numpy as np

__author__ = 'gcolasurdo'

'''
Hokay so this is where we start to make our own functions for our statistical processes
Hopefully I can break it down so that we're doing the processes and it's the data that
gets moved through them.
'''


# Lets start with something simple. We're going to need math stuff
# Apparently the stuff is already in there.


def sumproduct(*lists):
    return sum(functools.reduce(operator.mul, data) for data in zip(*lists))


class Stochastic:
    def __init__(self, bt, s, u, numw=1, k=2):

        # Ok so bt is T lt is t and k is the resolution. since this is a class, the instantiation of different
        # Stochastic classes will have to serve the purpose of separate omegas T is the sample space of T, descretized
        # beforehand so it should be either a list of floats with each element being the observed time OR T can be an
        # integer that will create an index from 0 to T
        # k will be optional and default to the length of T as that is the smallest filtration that we can measure k on

        # defining the T space
        if type(bt) is int:
            self.bt = range(0, bt)
        elif type(bt) is list:
            self.bt = bt
        else:
            raise Exception("Big T needs to be an integer or a range of numbers, The Stochastic init got neither")

        # If the resolution k is bigger than the T space then we shall make an interpolation
        if isinstance(k, int) and k > len(self.bt):
            self.bt = [x * (max(self.bt) - min(self.bt)) - min(self.bt) for x in range(k)]

        self.k = len(self.bt)
        # defining the dT's
        self.dt = np.zeros(self.k - 1)
        for ti in range(self.k - 1):
            self.dt[ti] = self.bt[ti + 1] - self.bt[ti]
        self.U = u
        self.S = s
        self.ut = np.zeros(self.k)
        self.st = np.zeros(self.k)
        self.defsigma()
        self.defmiyu()
        self.dx = np.zeros(self.k - 1)
        self.XCollection = [None] * numw
        self.BCollection = [None] * numw
        for w in range(numw):
            self.BCollection[w] = Brownian(self.bt)
            self.XCollection[w] = self.getxt(w)

    # Setting up the sample space
    def defsigma(self):
        for ti in self.bt:
            self.st[ti] = self.S(ti)

    def defmiyu(self):
        for ti in self.bt:
            self.ut[ti] = self.U(ti)

    # The calls go here

    def getxt(self, w):
        """
        This should return and array that holds the X(t,w)
        """
        xt = np.zeros(self.k)
        self.dx = self.BCollection[w].dw * self.st[:-1] + self.dt * self.ut[:-1]
        for ti in self.bt[:-1]:
            xt[ti + 1] = xt[ti] + self.dx[ti]
        return xt
        # I'll put down the functions here


class Brownian:
    def __init__(self, bt):
        """
        Here be the classic brownian motion. the conditions are that
        1. W(0) = 0 and
        2. W(i+1) - W(i) ~ N(0)
        :param bt: A vector with positive floats as elements. each element along the index should be
        larger than the last. It is meant to represent the partition of the T-space for a given brownian
        motion
        :return: self
        """
        self.dw = np.zeros(len(bt) - 1)
        self.dt = np.zeros(len(bt) - 1)
        for ti in range(len(bt) - 1):
            self.dt[ti] = bt[ti + 1] - bt[ti]
            self.dw[ti] = random.normalvariate(0, math.sqrt(self.dt[ti]))
