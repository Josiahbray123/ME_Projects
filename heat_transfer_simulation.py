# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 23:55:19 2020

@author: Josiah Bray
"""

import numpy as np
import matplotlib.pyplot as plt

#input the constants

#size of the plate in meters
x = 1
y = 1

#element size desired *keep in mind the memory of your machine*
dx = 0.05

#conduction constant
k = 5

#The boundary conditions

#the top has a constant q (W/m^2)
q_t = 0

#The right has a constant tempurature (K)
T_r = 300

#convection Temp (K) and coefficient (W/m^2)
T_inf = 700
h = 50

#The left side is adiabatic, so q=0


#setting up the matrix
e_size = int((x/dx)*(y/dx))
G = np.zeros([e_size,e_size])
H = np.zeros(e_size)

#lengths of the sides
x_l = int(x/dx)
y_l = int(y/dx)

#side boundaries left and right
left = np.zeros(e_size)
left[x_l:e_size-x_l:x_l] = 1
right = np.zeros(e_size)
right[2*x_l-1:e_size-x_l:x_l] = 1


#this is where the matrix is assembled

for i in range(0, e_size):
        
        #set up the conditions for the corners,sides, and bulk of the plate.
        #corners
        #top left
        if i == 0:
            
            G[i,i] = -2
            G[i,i+1] = 1
            G[i,i+x_l] = 1
            H[i] = -q_t*dx/k
            
        #top right    
        elif i == x_l-1:
            
            G[i,i] = -3
            G[i,i-1] = 1
            G[i,i+x_l] = 1
            H[i] = -q_t*dx/k-T_r
            
        #bottom left    
        elif i == e_size-x_l:
            
            G[i,i] = -2 - h*dx/k
            G[i,i+1] = 1
            G[i,i-x_l] = 1
            H[i] = -h*T_inf*dx/k

            
        #bottom right
        elif i == e_size-1:
            
            G[i,i] = -3 - h*dx/k
            G[i,i-1] = 1
            G[i,i-x_l] = 1
            H[i] = -T_r - h*T_inf*dx/k

        #sides
        #left
        elif left[i] == 1:
            
            G[i,i] = -3
            G[i,i+1] = 1
            G[i,i-x_l] = 1
            G[i,i+x_l] = 1
        #right    
        elif right[i] == 1:
            
            G[i,i] = -4
            G[i,i-1] = 1
            G[i,i-x_l] = 1
            G[i,i+x_l] = 1
            H[i] = -T_r
            
        #top
        elif i > 0 and i < x_l - 1:
            
            G[i,i] = -3
            G[i,i-1] = 1
            G[i,i+1] = 1
            G[i,i+x_l] = 1
            H[i] = -q_t*dx/k
            
        #bottom
        elif i > e_size - x_l and i < e_size - 1:
            
            G[i,i] = -3 - h*dx/k
            G[i,i-1] = 1
            G[i,i+1] = 1
            G[i,i-x_l] = 1
            H[i] = -h*T_inf*dx/k
            
        #bulk
        else:   
            G[i,i] = -4
            G[i,i-1] = 1
            G[i,i+1] = 1
            G[i,i+x_l] = 1
            G[i,i-x_l] = 1

#transposing the matrix
H = H.reshape([-1,1])
#solving the elements
T = np.linalg.solve(G,H)

#rearanging them in a matrix to be shown on a plot
M = T.reshape([y_l,x_l])

heat=plt.imshow(M, cmap='hot',interpolation="spline16")
plt.colorbar(heat)
                     