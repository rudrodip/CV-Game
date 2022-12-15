import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

xpoints=[]
ypoints=[]

with open('config.txt', 'r') as f:
    d = f.read().split('\n')
    for i in d:
        x = i.split(' ')
        xpoints.append(int(x[-1]))
        ypoints.append(int(x[-2]))
    
xpoints = np.array(xpoints)
ypoints = np.array(ypoints)

peaks, _ = find_peaks(ypoints)
mins, _ = find_peaks(ypoints*-1)

for frame, area in zip(mins, ypoints[mins]):
    print(frame, area)

plt.plot(xpoints, ypoints, color='black');
plt.plot(xpoints[mins], ypoints[mins], 'x', label='mins')
plt.plot(xpoints[peaks], ypoints[peaks], '*', label='peaks')
plt.show()
