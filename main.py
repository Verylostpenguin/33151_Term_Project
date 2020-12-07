from math import *
from vpython import *

##Iris

## Constants
G = 6.6741e-11

## force function, 1 on 2
def force(body1, body2): 
    force = -G*(body1.mass*body2.mass)/(mag2(body2.pos - body1.pos))*norm(body2.pos - body1.pos)
    return force

## net force on part1 (is there a simpler way to do this?)
def netForce(source, *argv):
    netForce = 0
    for body in argv:
      netForce += force(source, body)
    return netForce

## Updates forces of all celestials
def updateForces(celestials):
    for celestial in celestials:
        otherBodies = [celestials[a] for a in celestials if a != celestial]
        celestials[celestial].force = netForce(celestial, otherBodies)

def updateMomenta(celestials, dt):
    for celestial in celestials:
        celestial.mom = celestial.force * dt

def updatePosition(celestials, dt):
    for celestial in celestials:
        celestial.pos = (celestial.mom * dt)/celestial.mass

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

    ## There might be some finicky syntax with .mom and .pos for the sphere objects,
    ## I'm not sure

    ## update each body's momentum
    updateMomenta(celestials, dt)
    ## update each body's position
    updatePositions(celestials, dt)
