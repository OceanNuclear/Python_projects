#!/home/oceanw/anaconda3/bin/python3
import numpy as np
import matplotlib.pyplot as plt

r = [87 ,152, 217, 281, 346]
d = [-40, -80, -115, -153, -255]
r, d = np.meshgrid(r, d)

counts = np.array([[91401,41859,17363,7052,2632],
[193607,77909,30294,10794,3500],
[243079,99569,36304,12632,4273],
[367465,132203,45761,15225,5017],
[612040,201294,60789,19417,6249]])


plt.scatter(r,d, s=(counts*0.001))
plt.xlabel("Radial distance away from source(mm)")
plt.ylabel("Distance from surface of the tank(mm)")
plt.title("Bubble plot of Thermal Neutron flux")
plt.show()
