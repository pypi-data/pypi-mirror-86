"""Hover mouse onto an object
to pop a flag-style label"""
from vedo import *

b = Mesh(datadir+'bunny.obj').flag().color('m')
c = Cube(side=0.1).computeNormals().alpha(0.5).y(-0.02)

# vignette returns a Mesh type object which can be later modified
vig = b.vignette('A vignette descriptor\nfor a rabbit', font='Quikhand')
vig.scale(0.5).color('v').useBounds() # tell camera to take vig bounds into account

# add a pop up flag when hovering mouse
c.flag('my cube\nflag-style label', font="LionelOfParis") # picks filename by default
#c.flag(False) # to later disable it

c.caption('2d caption for a cube\nwith face indices', point=[0.044, 0.03, -0.04],
          size=(0.3,0.06), font="VictorMono", alpha=1)

# create a new object made of polygonal text labels to indicate the cell numbers
labs = c.labels('id', cells=True, font='Theemim', scale=None)

# create an entry to the legend
b.legend('Bugs the bunny')
c.legend('The Cube box',
         pos="bottom-left", size=0.3, font="Bongas") # set options at the last entry

show(b, c, vig, labs, __doc__, axes=11, bg2='linen')
