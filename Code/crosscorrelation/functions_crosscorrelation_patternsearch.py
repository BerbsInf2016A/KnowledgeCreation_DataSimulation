import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# Execute the following command to install the python dependencies
# pip install numpy scipy matplotlib ipython jupyter pandas sympy nose


def normalized(a, axis=-1, order=2):
    # See:
    # https://stackoverflow.com/questions/21030391/how-to-normalize-an-array-in-numpy
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2 == 0] = 1
    return a / np.expand_dims(l2, axis)


def getCorrelationDataForPatternSearch(seqA: [],
                                       pattern: [],
                                       plotCorrelation=False):
    seqA = seqA.astype(float)
    pattern = pattern.astype(float)

    seqANorm = normalized(seqA)[0]
    patternNorm = normalized(pattern)[0]

    correlated = np.correlate(seqANorm, patternNorm)
    if plotCorrelation:
        fig = plt.figure(constrained_layout=True)
        gs = GridSpec(1, 1, figure=fig)
        ax = fig.add_subplot(gs[0, 0])
        ax.plot(correlated, 'ro')
        ax.set_title('Correlation: Sequence A and Pattern')
        plt.draw()
    return correlated


def extractIndicesFromCorrelationData(correlationData, threshold=0.3):
    # Suppres scientific notation when printing floats:
    np.set_printoptions(suppress=True)
    sorted = np.argsort(correlationData)
    sorted = sorted[::-1]
    # Filter with threshold
    valuesList = []
    for index in sorted:
        value = correlationData[index]
        if value >= threshold:
            valuesList.append([int(index), value])

    # Define the return value, first entry is index, which is an integer
    return np.asarray(valuesList)
