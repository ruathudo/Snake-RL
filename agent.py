import torch
import random
import numpy as np
from collections import deque
from game import Snake, Direction, Point


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Mario:
    def __init__(self):
        pass

    def act(self, state):
        """Given a state, choose an epsilon-greedy action"""
        pass

    def cache(self, experience):
        """Add the experience to memory"""
        pass

    def recall(self):
        """Sample experiences from memory"""
        pass

    def learn(self):
        """Update online action value (Q) function with a batch of experiences"""
        pass
