import numpy as np
import matplotlib.pyplot as plt
from development.extractpoint import calMatrix
# distanceMatrix=calMatrix()
distanceMatrix=np.array(calMatrix())
# print(len(distanceMatrix))
plt.matshow(distanceMatrix, cmap=plt.cm.gray_r)


# plt.colorbar(ax.colorbar, fraction=0.025)1
plt.title("Gray Graph of Protein Distance Matrix")
plt.show()