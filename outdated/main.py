from math import *
from vpython import *

## Constants
G = 6.6741e-11

## force function, 1 on 2
def force(part1,part2): 
    force = -G*(part1.mass*part2.mass)/(mag(part2.pos - part1.pos)**2)*norm(part2.pos - part1.pos)
    return force

## net force on part1 (is there a simpler way to do this?)
def netForce(source, *argv):
    netForce = 0
    for body in argv:
      netForce += force(source, body)
    return netForce

## Updates forces of all celestials
def updateForces (celestials):
    for celestial in celestials:
        otherBodies = [celestials[a] for a in celestials if a != celestial]
        celestials[celestial].force = netForce(celestial, otherBodies)

## Create sphere object
def createSphere (data, planetColor):
    obj = sphere(make_trail = True, interval = 1,
                 trail_color = color.white, pos = vector(data[2], 0, 0),
                 radius = data[1], color = planetColor)
    obj.mass = data[0]
    obj.momentum = obj.mass * vector(0, data[3], 0)
    
    return obj

celestials = {}

# Creates array of sphere objects with relevant data
with open("data.txt", "r") as celestialFile:
    for line in celestialFile.readlines():
        data = line.split(",")
        celestials[data[0]] = createSphere([float(i) for i in data[1:]], color.magenta)

time = 0
end = 0
dt = 36000

while time < end:
    rate(100)
    time += dt
    ## force on each body
    updateForces(celestials)
