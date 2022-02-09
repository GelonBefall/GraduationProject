import numpy as np
def colormapInit():
    colorFile="./materials/gray.rgb"
    colormapMatrix = []
    with open(colorFile) as f:
        for line in f:
            # colormapMatrix.insert(0,list(map(int,line.split())))
            colormapMatrix.append(list(map(int,line.split(","))))
    
    colormapMatrix = np.array(colormapMatrix)
    print(colormapMatrix)

if __name__=='__main__':
    colormapInit()