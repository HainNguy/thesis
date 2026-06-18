import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 4, 50)
fig, axes = plt.subplots(1, 2, figsize=(8,3))

axes[0].plot(x, x**2)
axes[0].set_title
axes[0].set_xlabel('x')
axes[0].set_ylabel('x^2')

axes[1].plot(x, np.sqrt(x))
axes[1].set_title('Right')
axes[1].set_xlabel('x')
axes[1].set_ylabel('square root of x')

plt.tight_layout()
plt.show()

