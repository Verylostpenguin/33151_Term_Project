from tkinter import *
import math
import itertools
import tkinter.font
from PIL import Image, ImageTk

from Quadtree import *
from Body import *

root = Tk()
root.title = "Solar System Simulator"

# distance is scaled by a factor of 1 pixel is 10^10m
# planets and sun will be same size (for clarity)
canvas = Canvas(root, width=1200, height=800, bg = "black") 
canvas.grid(column = 2, row = 0, rowspan=20)

class Space:
  def __init__(self, root, canvas, scale = 1, bodies = []):
    self.G = 6.6741e-11
    self.k = 9e9
    self.canvas = canvas
    self.root = root
    self.scale = scale
    self.bodies = bodies
    self.pause = 1
    self.selectedBody = None
    self.canvas.focus_set()
    self.canvas.bind("<Button-1>", self.canvas_onleftclick)
    self.canvas.bind("<Button-3>", self.canvas_onrightclick)
    self.canvas.bind("<MouseWheel>", self.canvas_onmousewheel)
    self.canvas.bind("<BackSpace>", self.canvas_onbackspace)
    self.centerX = 0
    self.centerY = 0

    self.time = 0
    self.dt = 10000
    
    self.startText = StringVar()
    self.startButton = Button(self.root, textvariable=self.startText, width=10,
                              bg="grey", command=self.canvas_pause)
    self.startText.set("Start")
    self.startButton.grid(column=0, row=9, columnspan=2)

    self.firstText = StringVar()
    self.firstButton = Button(self.root, textvariable=self.firstText, width=10,
                              bg="grey", command=self.preset1)
    self.firstText.set("Solar System")
    self.firstButton.grid(column=0, row=0, columnspan=2)

    self.secondText = StringVar()
    self.secondButton = Button(self.root, textvariable=self.secondText, width=10,
                              bg="grey", command=self.preset2)
    self.secondText.set("Binary System")
    self.secondButton.grid(column=0, row=1, columnspan=2)
  
  def loop(self):
    if self.time < 3.15e8:
      self.time += self.dt
      self.moveBodies()
      self.canvas.after(2, self.loop)

  def moveBodies(self):
    if not self.pause == -1:
      return
    bodies_pairs = list(itertools.combinations(self.bodies, 2))
    for pair in bodies_pairs:
      Body.pair_Gforce(pair, self)
    # Body.pair_EForce(pair, self) (electric force)
    for body in self.bodies:
      body.move(self.dt)
      body.updateVector()
  
  # TODO
  # BARNES-HUT ALGORITHM
  """ def TreeWalk(self, node, node0, thetamax=0.7, G=1.0):
    dx = node.COM - node0.COM
    r = np.sqrt(np.sum(dx**2))
    if r > 0:
      if (len(node.children) == 0) or (node.size/r < thetamax):
        node0.g += G * node.mass * dx/r**3
      else:
        for c in node.children:
          self.TreeWalk(c, node0, thetamax, G)

  def GravAccel(self, points, masses, thetamax=0.7, G=1.):
    center = (np.max(points, axis=0)+np.min(points, axis=0)) / 2
    topsize = np.max(np.max(points, axis=0)-np.min(points, axis=0))
    leaves = []
    topnode = QuadNode(center, topsize, masses, points,
                      np.arange(len(masses)), leaves)
    accel = np.empty_like(points)
    for i, leaf in enumerate(leaves):
      self.TreeWalk(topnode, leaf, thetamax, G)
      accel[leaf.id] = leaf.g
    return accel """  

  def clickOnObject(self, event):
    for body in self.bodies:
        if body.contains(np.array([event.x, event.y])):
            return body
    return None

  def canvas_onleftclick(self, event):
    check = self.clickOnObject(event)
    if self.selectedBody == None:
      if check == None:
        body = Body(self.canvas, np.array([event.x, event.y], dtype ="float64"),
                    np.zeros(2), 5.9724e24, 10, len(self.bodies), "white", 1, self)
        if self.selectedBody != None:
          self.selectedBody = None
        self.bodies.append(body)
      else:
        self.selectedBody = check
        self.selectedBody.selected = True
        self.canvas.itemconfig(self.selectedBody.id,outline = "deep sky blue")
    else:
      if self.selectedBody == check:
        self.canvas.itemconfig(self.selectedBody.id,outline = "")
        self.selectedBody.selected = False
        self.selectedBody = None
      else:
        dx,dy = (event.x - self.selectedBody.position[0]),(event.y - self.selectedBody.position[1])
        self.selectedBody.velocity = [dx/10, dy/10]
        self.selectedBody.updateVector()
        
  def canvas_onrightclick(self, event):
    check = self.clickOnObject(event)
    if self.selectedBody == None:
      if check != None:
        check.updateShape(flipCharge=True)
    else:
      if self.selectedBody == check:
        check.updateShape(flipCharge=True)
      else:
        self.selectedBody.velocity = [0, 0]
        self.selectedBody.updateVector()

  def canvas_onmousewheel(self, event):
    if self.selectedBody != None:
      self.selectedBody.updateShape(mass=1e30)
      self.canvas.itemconfig(self.selectedBody.id,outline = "white")
      self.selectedBody.updateVector()

  def canvas_onbackspace(self, event):
    if self.selectedBody != None:
      self.canvas.delete(self.selectedBody)

  # Standard solar system preset
  # will spawn sun in center and all planets on the x-axis
  def preset1(self):
    for body in self.bodies:
      self.canvas.delete(body)
    self.bodies = []
    with open("data/preset1.txt", "r") as preset1File:
      for line in preset1File.read().splitlines():
        data = line.split(",")
        angle = np.random.ranf() * 2 * math.pi
        posAng = np.array([math.cos(angle), math.sin(angle)], dtype="float64")
        pos = float(data[1]) * posAng * 1e-10 + np.array([600, 400], dtype="float64")
        vecAng = np.array([math.cos(angle + math.pi), math.sin(angle + math.pi)], dtype="float64")
        vel = float(data[2]) * vecAng * 1e-10
        planet = Body(self.canvas, pos, vel, float(data[0]),
                      5, len(self.bodies), data[3], 1, self)
        self.bodies.append(planet)

  def preset2(self):
    # need to find some sort of stable binary system
    # and scale it properly
    pass

  def canvas_pause(self):
    self.pause *= -1
    self.startText.set(["Pause","Start"][int((self.pause+1)/2)])
    
space = Space(root, canvas)
space.loop()
root.mainloop()
