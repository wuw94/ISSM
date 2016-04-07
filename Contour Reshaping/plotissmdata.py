import matplotlib.pyplot as plt
import numpy as npy

x,y,vx,vy=npy.loadtxt('issmplotdat.txt',delimiter=',',unpack=True)
elements=npy.loadtxt('issmplotdatelements.txt',delimiter=',')

vel=npy.sqrt(vx**2+vy**2)

fig=plt.figure()
ax=fig.add_subplot(111)
ax.tricontour(x,y,elements,vel)

plt.show()

# Variant 1: initialize and plot an arbitrary circular contour within the plot
# limits, as in poly_editor.py.  Enable the same toggling, "t" to toggle the
# markers on and off, "d" to delete the point under the cursor (within some
# alpha of the cursor), and "i" to insert a point under the cursor.

# Variant 2: enable a pre-existing contour, defined by vectors x and y from a
# separate file, to be loaded by the user.  For now, just save a file
# containing two columns x and y defining the points of an arbitrary contour.
# Load this contour from the file, plot it over the tricontour plot called
# above, and then enable the same editing of the contour.

# Variant 3: enable saving an edited contour to a new file with column vectors
# x and y.

# Extra credit: enable multiple contours to be created, edited, and even
# deleted over the tricontourf plot, as if multiple independent features were
# being traced on the figure.  Then save the multiple contours to a single
# file, in the following format (without the comment markers...):

#contour1
#x1 y1
#x2 y2
#xend yend
#
#contour2
#x1 y2
#x2 y2
#x3 y3
#xend yend
