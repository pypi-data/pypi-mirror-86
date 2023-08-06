"""Contains the Ecosystem class, which is used to grow trees.

Example:
----------
import chartree as ct
w = ct.Ecosystem(size=[50, 50], material='.', background='$')
w.grow()
"""

import numpy as np
from IPython.display import clear_output
from math import pi, log
from time import sleep

def vec_from_angle(from_vec, angle):
    from_vec = np.copy(from_vec)
    angle = angle * pi / 180
    arc = np.arctan(from_vec[1] / from_vec[0])
    if from_vec[0] < 0:
        new_ang = pi + arc + angle
    elif from_vec[1] < 0:
        new_ang = 2*pi + arc + angle
    else:
        new_ang = arc + angle
    return np.array([np.cos(new_ang), np.sin(new_ang)])

def split(br, ang, props, next_split):
    s_center = br.center
    s_width = (props['w'] * br.width**2)**(1/2)
    s_direc = vec_from_angle(br.direction, props['a']*ang)

    br.width = ((1-props['w']) * br.width**2)**(1/2)
    br.direction = vec_from_angle(br.direction, -(1-props['a'])*ang)

    return Branch(center=s_center, width=s_width, direction=s_direc, next_split=next_split)

def to_sun(dir, rndmns, lean):
    off_vert = np.arctan(dir[0]/dir[1]) * 180/pi
    return vec_from_angle(dir, .7*off_vert + (lean/10)*np.random.randint(-rndmns, rndmns))

class Branch:
    def __init__(self, center, width, direction, next_split):
        self.center = np.array(center)
        self.width = width
        self.direction = np.array(direction) / np.linalg.norm(np.array(direction))
        self.next_split = int(next_split)
        self.sign_proba = .5

class Ecosystem:
    """A must for most trees. Initiate your Ecosystem and then use grow() and show() methods to create your tree.
    
Parameters
------------
size : array_like
    The shape of the character grid, equalized to account for characters being taller than they are wide. Default is [50,40].
material : char
    The character used to fill the tree. Must be a single character. Default is '$'
background : char
    The character used to fill the background of the Ecosystem. Default is '`'.

Methods
------------
grow()
    Grows a tree, differently every time.
show()
    Shows current tree, optionally changing materials (tree and background characters).
    
Returns
------------
Ecosystem object.
"""

    def __init__(self, size=[50,40], material='$', background='`'):
        self.w = int(size[0] * 2)
        self.h = int(size[1])
        self.mat = str(material)
        self.bg = str(background)
        self.plot = 'Nothing has grown!'
        
    def make_wood(self, coor):
        coor = np.copy(coor)
        coor[0] = coor[0] * 2
        coor = np.round(coor).astype(int)
        if (coor[1] >= 0 and coor[1] < self.h and 
            coor[0] >= 0 and coor[0] < self.w):
            self.plot[coor[1], coor[0]] = 1

    def show(self, material=None, background=None, save=False):
        """Shows the grown tree. Can be used to experiment with characters without changing the shape of the tree. 
        
Parameters:
-------------
material : char
    Optional. Changes the Ecosystem material.
background : char
    Optional. Changes the Ecosystem background.
save : bool
    Whether or not to save the text output. Default False.

Returns:
------------
Nothing. Simply prints tree.
"""

        if material is not None: 
            self.mat = str(material)
        if background is not None: 
            self.bg = str(background)
        if isinstance(self.plot, str):
            print(self.plot)
        else:
            whole = ''
            for row in self.plot:
                line = ''
                for let in row:
                    if let == 1:
                        line += self.mat
                    else:
                        line += self.bg
                whole += (line + '\n')
            clear_output(wait=True)
            print(whole)
            if save:
                f = open('tree.txt', 'w')
                f.write(whole)
                f.close()
            
    def grow(self, roots=30, lean=4, trunk_w=6, trunk_h=7, density=6, n_iter=50, thinning=1.2, ang_mean=40, ang_range=10, watch=True, speed=25):
        """Grows a tree, starting at the bottom center of the grid.
        
Parameters:
-------------
roots : int
    Vastness of the root system. Default is 30.
lean : int/float
    Overall lean of the tree. Positive leans right, negative left. Lots of randomness here, so don't expect much. Default is 4.
trunk_w : int
    The starting radius of the trunk. Default is 6.
trunk_h : int
    The iteration at which the first branch grows off the trunk. Default is 7.
density : int
    Rate at which new branches form. Lower numbers are denser. Default is 6, which means new branches form about every 6 growth iterations.
n_iter : int
    The number of growth iterations. Default is 40.
thinning : float
    Rate at which the branches decrease in width. Higher numbers lead to thinner trees. Default is 1.2.
ang_mean : int
    The mean angle of branch splits. Default is 40.
ang_range : int
    The range, above and below ang_mean, of angle possibilities. A higher range means a more unpredictable tree. Default is 10.
watch : bool
    Whether or not to watch the tree as it grows. Default True.
speed : int/float
    Speed at which the tree grows (only if watch=True), in iterations per second. Default is 25.
    
Returns:
------------
Nothing. Change the materials of the grown tree with show().
"""

        self.plot = np.full(shape=(self.h, self.w), fill_value=0)

        if lean == 0:
            lean = .001

        branches = [Branch(center=[(self.w-lean)/4, self.h], 
                           width=roots, 
                           direction=[lean,-10],
                           next_split=trunk_h)]
        
        for i in range(1, n_iter+1):
            hard_length = len(branches)
            for br in branches:
                if branches.index(br) == hard_length:
                    break

                for r in np.arange(0, br.width/2, .5):
                    ring = np.array([1., 0.])
                    if br.width < trunk_w:
                        ring -= ring.dot(br.direction) * br.direction
                        ring /= np.linalg.norm(ring)
                    ring *= r
                    self.make_wood(br.center + ring)
                    self.make_wood(br.center - ring)

                if branches.index(br) == 0\
                    and i < .6*n_iter\
                    and i == np.random.randint(i-4, i+5):
                    br.direction = to_sun(br.direction, int(ang_range), lean=lean)

                if i == br.next_split:
                    br.next_split = np.random.randint(i+density-1, i+density+2)
                    ang = np.random.randint(ang_mean-ang_range, ang_mean+ang_range) \
                          * (1 if np.random.random() > br.sign_proba else -1)
                    if ang < 0:
                        br.sign_proba -= .5
                    else:
                        br.sign_proba += .5

                    if branches.index(br) == 0\
                        and i > .4*n_iter\
                        and br.width > (trunk_w/4):
                        props = {'w':.4, 'a':.65}
                    else:
                        props = {'w':.3, 'a':.8}
                    branches.append(split(br=br, 
                                          ang=ang,
                                          props=props,
                                          next_split=i+density))
                br.center = br.center + br.direction
                if br.width > trunk_w:
                    br.width = br.width - .1 - (br.width-trunk_w)*.8
                br.width *= (1 - (thinning/100))
            if watch:
                sleep(1 / speed)
                self.show()

    def __repr__(self):
        return "Ecosystem of size {}x{}, material='{}', background='{}'" \
               .format(int(self.w/2), self.h, self.mat, self.bg)
