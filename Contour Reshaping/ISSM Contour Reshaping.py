# Contour Reshaping
#
# Given a triplot, this script will plot a draggable contour of velocity for the triangulation
#
# Wesley Wu

import numpy as np
from ContourEditor import ContourInteractor
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import math
import time




'''---------------Load Inputs------------------------'''

# Put your inputs here
velocity = 1000 # Draw contour of this velocity

x,y,vx,vy=np.loadtxt('issmplotdat.txt',delimiter=',',unpack=True)
elements=np.loadtxt('issmplotdatelements.txt',delimiter=',')
vel=np.sqrt(vx**2+vy**2)

fig = plt.figure()



'''---------------Initialize Variables---------------'''

# Establish bounds of the graph
# Complexity of O( n )
print('Establishing bounds...')
maxX = -99999999999
maxY = -99999999999
minX = 99999999999
minY = 99999999999
for i in range(len(x)):
    if x[i] > maxX:
        maxX = x[i]
    if x[i] < minX:
        minX = x[i]
    if y[i] > maxY:
        maxY = y[i]
    if y[i] < minY:
        minY = y[i]
print('Done!\n')


# allTriangles:
# A dictionary where the keys are centroids - tuple(x,y) - and values are the triangle coordinates & velocity stored as a tuple of tuples - tuple( tuple(x1,y1,v1),tuple(x2,y2,v2),tuple(x3,y3,v3) )
# Complexity of O( n )
print('Initializing hash for triangles...')
allTriangles = dict()
for i in range(len(elements)):
    index = elements[i]
    x1, x2, x3 = x[index[0]], x[index[1]], x[index[2]]
    y1, y2, y3 = y[index[0]], y[index[1]], y[index[2]]
    v1, v2, v3 = vel[index[0]], vel[index[1]], vel[index[2]]
    
    centroid = tuple(((x1+x2+x3)/3,(y1+y2+y3)/3))
    allTriangles[centroid] = tuple((tuple((x1,y1)), tuple((x2,y2)), tuple((x3,y3)), tuple((v1,v2,v3)),i))
print('Done!\n')


# orderedCentroids:
# An ordered list - list(tuple(x,y)) - of centroid tuples for allTriangles
# Complexity of O( n*log(n) )
print('Putting centroids in order...')
orderedCentroids = sorted(allTriangles.keys())
print('Done!\n')


# visible:
# A dictionary with keys being centroids of triangles are currently active and values being their plt.text object
visible = dict()
#print(vx)

'''---------------Initialize Functions---------------'''

# redraw will create the triplot
def draw():
    plt.gca().set_aspect('equal')
    plt.tricontour(x,y,elements,vel)
    plt.title('Contour Reshaping')
    plt.xlabel('Distance X (units)')
    plt.ylabel('Distance Y (units)')

def contourList(contourAmount:float):
    contourPoints = set()
    for i in range(0, len(orderedCentroids)):
        for j in [[0,1],[1,0],[1,2],[2,1],[2,0],[0,2]]:
            vtup = allTriangles[orderedCentroids[i]][3]
            if vtup[j[0]] < contourAmount < vtup[j[1]]:
                lowV, highV = vtup[j[0]], vtup[j[1]]
                ratio = (contourAmount-lowV)/(highV-lowV)
                lowX, highX = allTriangles[orderedCentroids[i]][j[0]][0], allTriangles[orderedCentroids[i]][j[1]][0]
                lowY, highY = allTriangles[orderedCentroids[i]][j[0]][1], allTriangles[orderedCentroids[i]][j[1]][1]
                contourX, contourY = lowX + ratio * (highX - lowX), lowY + ratio * (highY - lowY)
                contourPoints.add(tuple((contourX, contourY)))
    return radialSort(list(contourPoints))

def radialSort(contourPoints):
    if (len(contourPoints) == 0): return list()
    size = len(contourPoints)
    newPoints = list()
    newPoints.append(contourPoints[0])
    
    while len(newPoints) < size:
        point = None
        for i in range(0, len(contourPoints)):
            if point == None or distance(newPoints[-1], point) > distance(newPoints[-1], contourPoints[i]):
                point = contourPoints[i]
        newPoints.append(point)
        contourPoints.remove(point)
    return newPoints

def distance(p1, p2): # returns the distance between two points
    return math.fabs(math.sqrt( (p2[0]-p1[0])**2 + (p2[1]-p1[1])**2 ))



draw()

poly1 = Polygon(contourList(velocity), animated=True)
ax = fig.add_subplot(111)
ax.add_patch(poly1)
p = ContourInteractor(ax, poly1)

plt.show()
