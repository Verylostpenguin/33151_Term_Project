from tkinter import *
import math
import numpy as np

from Quadtree import *


class Body:
  def __init__(self, canvas, pos, vel, mass, radius, num, color, charge, name, space = None):
    self.num = num
    self.canvas = canvas
    self.color = color
    self.name = name
    self.charge = charge # Can add later
    self.selected = False

    self.mom = mass * vel
    self.velocity = vel
    self.position = pos + np.array([1280/2, 960/2], dtype="float64")
    self.force = np.array([0.0, 0.0])

    self.id = canvas.create_oval(self.position[0] - radius, self.position[1] - radius, self.position[0] + radius, 
                                 self.position[1] + radius, fill=color)
    self.lineID = self.canvas.create_line(self.position[0], self.position[1], self.position[0] + 10 * self.velocity[0],
                                          self.position[1] + 10 * self.velocity[1])
    
    self.radius = radius
    self.mass = mass
    self.space = space

  def __repr__(self):
    return str(self.num)

  @staticmethod
  def pair_Gforce(body_pair, space):
    body1, body2 = body_pair
    dpos = (body2.position - body1.position)
    force = (dpos/np.linalg.norm(dpos)**3)*space.G*body1.mass*body2.mass
    body1.force += force
    body2.force -= force

  # @staticmethod
  # def pair_Eforce(body_pair, space):
  #   body1, body2 = body_pair
  #   dpos = (body2.realPos - body1.realPos)
  #   force = (dpos/np.linalg.norm(dpos)**3)*space.k*body1.mass*body2.mass
  #   sign = body1.charge * body2.charge
  #   body1.force -= force * sign
  #   body2.force += force * sign

  def contains(self, pos):
    return np.linalg.norm(self.position - pos) < self.radius/2

  def move(self, dt):
    self.mom += self.force * dt
    self.velocity = self.mom / self.mass
    self.position += self.velocity * dt

    self.canvas.coords(self.id, int(self.position[0] - self.radius), int(self.position[1] - self.radius),
                       int(self.position[0] + self.radius), int(self.position[1] + self.radius))
    self.force = np.zeros(2)
      
  def updateVector(self):
    self.canvas.delete(self.lineID)
    self.lineID = self.canvas.create_line(self.position[0],self.position[1],self.position[0]+self.velocity[0],
                                          self.position[1]+self.velocity[1], fill = "white")

  def updateShape(self, delete=False, mass=None):
    if delete:
      self.deleteBody
    if mass != None:
      self.mass += mass

  def deleteBody(self):
    self.canvas.delete(self.id) 
