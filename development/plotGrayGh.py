import numpy as np
import matplotlib.pyplot as plt
from development.matrixMaker import calMatrix

# distanceMatrix=calMatrix()
newMatrix= calMatrix()
# distanceMatrix=np.array(newMatrix.trueMatrix())
distanceMatrix=np.array(newMatrix.grayRGBMatrix())
# print(len(distanceMatrix))

image = np.array(distanceMatrix, dtype=np.uint8)

plt.imshow(image, interpolation='none')
plt.show()