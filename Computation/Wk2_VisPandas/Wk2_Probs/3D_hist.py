import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

data = pd.read_csv('../lipids.csv', header=4)

diseased_data = data[data['diseased'] == 1]

weights = (1 / len(diseased_data['chol'])) * np.ones_like(diseased_data['chol'])

n, bin_cuts, patches = plt.hist(diseased_data['chol'], 25, weights=weights)

plt.xlabel('concentration of plasma cholesterol (mg/dl)')
plt.ylabel('frequency')

plt.show()

left_cut = np.argmax(n)

midpoint = (bin_cuts[left_cut + 1] + bin_cuts[left_cut]) / 2

print(midpoint)

#3D plot

fig = plt.figure()
ax = fig.add_subplot(111, projection ='3d')
bin_num = 25
hist, xedges, yedges = np.histogram2d(diseased_data['chol'], diseased_data['trig'], bins=bin_num)
hist = hist / hist.sum()
x_midp = xedges[:-1] + 0.5 * (xedges[1] - xedges[0])
y_midp = yedges[:-1] + 0.5 * (yedges[1] - yedges[0])
elements = (len(xedges) - 1) * (len(yedges) - 1)
ypos, xpos = np.meshgrid(y_midp, x_midp)
xpos = xpos.flatten()
ypos = ypos.flatten()
zpos = np.zeros(elements)
dx = (xedges[1] - xedges[0]) * np.ones_like(bin_num)
dy = (yedges[1] - yedges[0]) * np.ones_like(bin_num)
dz = hist.flatten()
ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='b', zsort='average')
ax.set_xlabel('concentration of plasma cholesterol (mg/dl)')
ax.set_ylabel('concentration of plasma triglicerides (mg/dl)')
ax.set_zlabel('frequency')

plt.show()