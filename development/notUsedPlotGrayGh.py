import numpy as np
import matplotlib.pyplot as plt
from development.matrixMaker import calMatrix
# distanceMatrix=calMatrix()
newMatrix= calMatrix()
# distanceMatrix=np.array(newMatrix.trueMatrix())
distanceMatrix=np.array(newMatrix.maskMatrix())
# print(len(distanceMatrix))
plt.matshow(distanceMatrix, cmap=plt.cm.gray_r)


# plt.colorbar(ax.colorbar, fraction=0.025)1
plt.title("Gray Graph of Protein Distance Matrix")
plt.show()