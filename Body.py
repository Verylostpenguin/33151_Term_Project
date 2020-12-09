from tkinter import *
import math
import numpy as np

from Quadtree import *


class Body:
  def __init__(self, canvas, pos, vel, mass, radius, num, color, charge, space = None):
    self.num = num
    self.canvas = canvas
    self.color = color
    self.id = canvas.create_oval(pos[0] - radius, pos[1] - radius, pos[0] + radius, pos[1] + radius, fill=color)
    self.lineID = self.canvas.create_line(pos[0], pos[1], pos[0] + 10 * vel[0], pos[1] + 10 * vel[1])
    self.charge = charge # Can add later
    self.selected = False
    
    self.position = pos
    self.velocity = vel
    self.force = np.array([0.0, 0.0])
    
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

  @staticmethod
  def pair_Eforce(body_pair, space):
    body1, body2 = body_pair
    dpos = (body2.position - body1.position)
    force = (dpos/np.linalg.norm(dpos)**3)*space.k*body1.mass*body2.mass
    sign = body1.charge * body2.charge
    body1.force -= force * sign
    body2.force += force * sign

  def contains(self, pos):
    return np.linalg.norm(self.position - pos) < self.radius/2

  def move(self, dt):
    momentum = self.force * dt * 1e-10**2 # scale back down to render
    self.velocity += momentum / self.mass
    self.position += self.velocity * dt
    print(self.velocity, self.position)
    
    self.canvas.move(self.id, self.velocity[0], self.velocity[1])
    self.force = np.array([0.0, 0.0])
  
  def updateVector(self):
    self.canvas.delete(self.lineID)
    self.lineID = self.canvas.create_line(self.position[0],self.position[1],self.position[0]+10*self.velocity[0],
                                          self.position[1]+10*self.velocity[1], fill = "white")

  def updateShape(self, flipCharge=False, mass=None):
    if flipCharge:
      self.charge *= -1
    if mass != None:
      self.mass = mass
      self.deleteBody
    color = "red" if self.charge == 1 else "blue"
    self.canvas.itemconfig(self.id, outline = color)

  def deleteBody(self):
    self.canvas.delete(self.id) 
