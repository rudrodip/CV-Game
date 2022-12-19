import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

xpoints=[]
ypoints=[]
collisions = np.array([4, 19, 31, 43, 54, 69, 84, 95, 107, 118, 133, 148, 164, 183])

with open('config.txt', 'r') as f:
    d = f.read().split('\n')
    for i in d:
        x = i.split(' ')
        xpoints.append(int(x[-1]))
        ypoints.append(int(x[-2]))
    
xpoints = np.array(xpoints)
ypoints = np.array(ypoints)

mins, _ = find_peaks(ypoints*-1)

for frame, area in zip(collisions, ypoints[collisions]):
    print(frame, area)

plt.plot(xpoints, ypoints, color='black');
plt.plot(xpoints[collisions], ypoints[collisions], 'x', label='actual collisions')
plt.plot(xpoints[mins], ypoints[mins], '*', label='estimed local minima')
plt.plot(xpoints[collisions], ypoints[collisions], color='blue')
plt.show()
