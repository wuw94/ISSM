# Element Numbering
# If you want to programmatically highlight certain triangles, use the 'highlightTriangle' function, with arguments being the index in the list of elements
# Put the prehighlight code near the end, where there will be a lot of hash marks
#
# Wesley Wu, Edward Kim

import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np
import math
import time

'''---------------Load Inputs------------------------'''

x,y,vx,vy=np.loadtxt('issmplotdat.txt',delimiter=',',unpack=True)
elements=np.loadtxt('issmplotdatelements.txt',delimiter=',')
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
# A dictionary where the keys are centroids - tuple(x,y) - and values are the triangle coordinates stored as a tuple of tuples - tuple( tuple(x1,y1),tuple(x2,y2),tuple(x3,y3) )
# Complexity of O( n )
print('Initializing hash for triangles...')
allTriangles = dict()
for i in range(len(elements)):
    index = elements[i]
    x1 = x[index[0]]
    x2 = x[index[1]]
    x3 = x[index[2]]
    y1 = y[index[0]]
    y2 = y[index[1]]
    y3 = y[index[2]]
    centroid = tuple(((x1+x2+x3)/3,(y1+y2+y3)/3))
    allTriangles[centroid] = tuple((tuple((x1,y1)),tuple((x2,y2)),tuple((x3,y3)),i))
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


'''---------------Initialize Functions---------------'''

# redraw will create the triplot
def redraw():
    plt.gca().set_aspect('equal')
    plt.triplot(x,y,elements,'k-')
    plt.title('Element Numbering')
    plt.xlabel('Distance X (units)')
    plt.ylabel('Distance Y (units)')

# inTriangle checks whether point x,y is within triangle - tuple(tuple(int,int))
def inTriangle(x,y,triangle): # ~0.000015s to process
    inside = False
    t1x,t1y = triangle[0]
    for i in range(4):
        t2x,t2y = triangle[i % 3]
        if y > min(t1y,t2y):
            if y <= max(t1y,t2y):
                if x <= max(t1x,t2x):
                    if t1y != t2y:
                        xinters = (y-t1y)*(t2x-t1x)/(t2y-t1y)+t1x
                    if t1x == t2x or x <= xinters:
                        inside = not inside
        t1x,t1y = t2x,t2y
    return inside

def highlightTriangle(index): #give this function the index of element and it will highlight
    clickedTriangleX = [x[elements[index][0]],x[elements[index][1]],x[elements[index][2]]]
    clickedTriangleY = [y[elements[index][0]],y[elements[index][1]],y[elements[index][2]]]
    plt.tripcolor(clickedTriangleX,clickedTriangleY,[0,1,2],cmap=plt.cm.Accent)
    a = elements[index]
    x1 = x[a[0]]
    x2 = x[a[1]]
    x3 = x[a[2]]
    y1 = y[a[0]]
    y2 = y[a[1]]
    y3 = y[a[2]]
    centroid = tuple(((x1+x2+x3)/3,(y1+y2+y3)/3))
    if centroid not in visible:
        visible[centroid] = plt.text(centroid[0], centroid[1], '.' + str(index))

def onclick(event): #print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(event.button, event.x, event.y, event.xdata, event.ydata))
    #print(event.button, event.x, event.y, event.xdata, event.ydata)
    if event.xdata < maxX and event.xdata > minX and event.ydata < maxY and event.ydata > minY:
        if event.key in ['alt+q','q'] or event.key in ['alt+w','w']:
            # TODO: put clicked triangles into an array
            # after a certain number of clicks, we want to remake the plot, to prevent recursion depth error
            if event.xdata < maxX or event.xdata > minX or event.ydata < maxY or event.ydata > minY:
                jump = index = len(orderedCentroids) // 2
                
                # Complexity of log(n) - ordered binary search to get to the nearest X
                while True:
                    jump = jump //2
                    if jump < 1 or event.xdata == orderedCentroids[index][0]:
                        break
                    index += jump * (int(event.xdata > orderedCentroids[index][0]) - int(event.xdata < orderedCentroids[index][0]))
                
                # Bounce outward checking if point is inside triangle who's centroid is centroid of list (to skip Y checking)
                jump = 1
                while True:
                    if inTriangle(event.xdata,event.ydata,allTriangles[orderedCentroids[index]]):
                        break
                    index += jump * (1-2*(jump % 2 == 0))
                    jump += 1

                # Find which 3 points make up the triangle
                clickedTriangle = allTriangles[orderedCentroids[index]]
                clickedTriangleX = [clickedTriangle[0][0],clickedTriangle[1][0],clickedTriangle[2][0]]
                clickedTriangleY = [clickedTriangle[0][1],clickedTriangle[1][1],clickedTriangle[2][1]]

            if event.key in ['alt+q','q']:
                if orderedCentroids[index] not in visible:
                    plt.tripcolor(clickedTriangleX,clickedTriangleY,[0,1,2],cmap=plt.cm.Accent)
                    visible[orderedCentroids[index]] = plt.text(orderedCentroids[index][0], orderedCentroids[index][1], '.' + str(clickedTriangle[3]))
            elif event.key in ['alt+w','w']:
                if orderedCentroids[index] in visible:
                    plt.tripcolor(clickedTriangleX,clickedTriangleY,[0,1,2],cmap=plt.cm.Greys)
                    visible[orderedCentroids[index]].remove()
                    del visible[orderedCentroids[index]]
            
        elif event.key in ['alt+e','e']:
            typedInput = input('Enter triangle index to highlight:  ')
            try:
                typedInput = int(typedInput)
                highlightTriangle(typedInput)
            except:
                print('Invalid Input')

        plt.draw()

redraw()
cid = fig.canvas.mpl_connect('key_press_event', onclick)



'''---------------Prehighlight Here------------------'''
########################################################

########################################################
'''--------------------------------------------------'''
plt.show()
