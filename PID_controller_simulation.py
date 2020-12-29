# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 15:24:27 2020

@author: Josiah Bray
"""

import numpy as np
import matplotlib.pyplot as plt
import control as co

#PID controller
#constants
C_p = 70
C_I = 50
C_D = 20

#controler
c_prop = C_p
c_inter = C_I * co.tf([1],[1,0])
c_diff = C_D * co.tf([1,0],[1])

PID = c_prop + c_inter + c_diff

print(PID)

#Identify the plant
plant = co.tf([1],[1,5,30])

print(plant)

#feedforward term can be included
feed_forward = 0

#combining the controls into a closed feedback control
sys_ = (PID+feed_forward)*plant
sys_closed = (sys_)/(1 + sys_) 

print(sys_)
print(sys_closed)

#simulation time in seconds
sim_time = 10
x = np.linspace(0,sim_time,1000)

#frequincies for bode plots
freq = np.linspace(0,1000,1000)

#openlooped with bode plot
x_r,y_r = co.step_response(sys_,x)
mag_0,phase_0,freq_0 = co.bode_plot(sys_,freq, Plot = True, dB = True, Hz = True, deg = True)
#closedlooped with bode plot
x_r1,y_r1 = co.step_response(sys_closed,x)
mag_1,phase_1,freq_1 = co.bode_plot(sys_closed,freq, Plot = True, dB = True, Hz = True, deg =True)

#plotting the response
plt.figure("Step Response",figsize=(12,6))
plt.plot(x_r,y_r,'-',c='b',label='open')
plt.plot(x_r1,y_r1,'-',c='r',label='closed')
plt.xlabel("time (s)")
plt.ylabel("Gain")
plt.title("Step Response")
plt.legend(loc=1)

