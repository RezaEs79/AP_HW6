import matplotlib.pyplot as plt
import numpy as np
h=10        # y-intercept
c=20        # Density
v=100        # Speed
lwidth=2    # thickness of line matplotlib
fig, ax = plt.subplots(figsize=(6, 6))
ax.set(ylim=[0,h],xlim=[0,h],
       yticks=np.linspace(0,h, h+1),
       xticks=np.linspace(0,h, h+1),
       aspect="equal"
       )
plt.xticks([])  # Disable xticks.
plt.yticks([])  # Disable xticks.
x= np.linspace(0, h, c+1)
for i in x[0:-1]:
    m=(-h+i)/(i+1)
    y=m*x+h-i
    plt.plot(x,y,'k',linewidth=lwidth)
    plt.pause(1/v)
plt.show()    
plt.close()
