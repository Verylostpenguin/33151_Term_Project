# This code is pulled and modified from 
# https://mikegrudic.wordpress.com/2017/07/11/a-simple-and-pythonic-barnes-hut-treecode/
# This code should encode the tree required for the Barnes-Hut Algorithm in 2d
from tkinter import *
import math
import numpy as np

class QuadNode:
  def __init__(self, center, size, masses, points, ids, leaves=[]):
    self.center = center
    self.size = size
    self.children = []

    bodies = len(points)

    if bodies == 1:
      leaves.append(self)
      self.COM = points[0]
      self.mass = masses[0]
      self.id = ids[0]
      self.g = np.zeros(2)
    else:
      self.GenerateChildren(points, masses, ids, leaves)
      com_total = np.zeros(2)
      m_total = 0.
      for c in self.children:
        m, com = c.mass, c.COM
        m_total += m
        com_total += com * m
      self.mass = m_total
      self.COM = com_total / self.mass  
 
  def GenerateChildren(self, points, masses, ids, leaves):
    quadrant_index = (points > self.center)
    for x in range(2): 
      for y in range(2):
        in_quad = np.all(quadrant_index == np.bool_([x, y]), axis=1)
        if not np.any(in_quad): continue
        dx = 0.5*self.size*(np.array([x, y]) - 0.5)
        self.children.append(QuadNode(self.center + dx,
                                     self.size / 2,
                                     masses[in_quad],
                                     points[in_quad],
                                     ids[in_quad],
                                     leaves))
