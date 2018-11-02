import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# Execute the following command to install the python dependencies
# pip install numpy scipy matplotlib ipython jupyter pandas sympy nose


def normalized(a, axis=-1, order=2):
    # See: https://stackoverflow.com/questions/21030391/how-to-normalize-an-array-in-numpy
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2==0] = 1
    return a / np.expand_dims(l2, axis)

def plotRawCorrelations(figure, gridSystem, plotRow, seqA, seqB):
    """ Takes a figure, the grid system in the figure, the row to plot to and two sequences
        to calculate and plot the correlations in all three ways ('valid', 'same', 'full). """

    # Calculate the correlations:
    valid = np.correlate(seqA, seqB, 'valid')
    same =  np.correlate(seqA, seqB, 'same')
    full = np.correlate(seqA, seqB, 'full')  

    # Plot the correlations:
    ax = figure.add_subplot(gridSystem[plotRow,:])
    ax.plot(valid, 'ro')
    ax.set_title('Correlation: Valid')
    plotRow += 1

    ax = figure.add_subplot(gridSystem[plotRow,:])
    ax.plot(same, 'ro')
    ax.set_title('Correlation: Same')
    plotRow += 1

    ax = figure.add_subplot(gridSystem[plotRow,:])
    ax.plot(full, 'ro')
    ax.set_title('Correlation: Full')
    plotRow += 1

    return plotRow

def plotNormalizedCorrelations(figure, gridSystem, plotRow, seqANorm, seqBNorm):
    """ Takes a figure, the grid system in the figure, the row to plot to and two normalized sequences
        to calculate and plot the correlations in all three ways ('valid', 'same', 'full). """

    validNormalized = np.correlate(seqANorm, seqBNorm, 'valid')
    sameNormalized =  np.correlate(seqANorm, seqBNorm, 'same')
    fullNormalized = np.correlate(seqANorm, seqBNorm, 'full')  

    ax = figure.add_subplot(gridSystem[plotRow,:])
    ax.plot(validNormalized, 'ro')
    ax.set_title('Correlation Normalized: Valid')
    plotRow += 1

    ax = figure.add_subplot(gridSystem[plotRow,:])
    ax.plot(sameNormalized, 'ro')
    ax.set_title('Correlation Normalized: Same')
    plotRow += 1

    ax = figure.add_subplot(gridSystem[plotRow,:])
    ax.plot(fullNormalized, 'ro')
    ax.set_title('Correlation Normalized: Full')
    plotRow += 1
    return plotRow

def plotCorrelationResults(figure, gridSystem, plotRow, seqA, seqB):
    """ Takes a figure, the grid system in the figure, the row to plot to and two sequences
        to execute the correlation calculation and to plot the result. """

    ax = figure.add_subplot(gridSystem[plotRow,:])
    ax.set_title('Correlation results')   
    # Calculate the correlation, using the xcorr method from the plot librar
    # The function uses numpy.correlate() to calculate the results, see:
    # https://matplotlib.org/api/_as_gen/matplotlib.pyplot.xcorr.html
    ax.xcorr(seqA.astype(float), seqB.astype(float), normed=False, usevlines=False, maxlags=10, linestyle='-' )
    ax.grid(True)
    ax.axhline(0, color='black',  linewidth=1, zorder=1)
    plotRow += 1
    return plotRow

def plotNormalizedCorrelationResults(figure, gridSystem, plotRow, seqA, seqB):
    """ Takes a figure, the grid system in the figure, the row to plot to and two sequences
        to execute the correlation calculation and to plot the result. """
    ax = figure.add_subplot(gridSystem[plotRow,:])

    ax.set_title('Normalized Correlation results')   
    # Calculate the correlation, using the xcorr method from the plot library [Normalizing the data]:
    # The function uses numpy.correlate() to calculate the results, see:
    # https://matplotlib.org/api/_as_gen/matplotlib.pyplot.xcorr.html
    ax.xcorr(seqA.astype(float), seqB.astype(float), normed=True, usevlines=False, maxlags=10, linestyle='-' )
    ax.grid(True)
    ax.axhline(0, color='black',  linewidth=1, zorder=1)
    plotRow += 1
    return plotRow

def crossCorrelation(seqA: [], seqB: [], plotNormalizedData = False, plotCorrelations = False, plotResults = False, plotNormalizedResults = True, subtractMeanFromResult = True):
    seqA = seqA.astype(float)
    seqB = seqB.astype(float)
    numberOfRowsToPlot = 2
    currentPlotRow = 0

    seqANorm = normalized(seqA)[0]
    seqBNorm = normalized(seqB)[0]

    if plotNormalizedData: numberOfRowsToPlot += 1
    if plotCorrelations: numberOfRowsToPlot += 3
    if plotCorrelations and plotNormalizedData:  numberOfRowsToPlot += 3
    if plotResults: numberOfRowsToPlot += 1
    if plotNormalizedResults: numberOfRowsToPlot += 1

    fig = plt.figure(constrained_layout=True)
    gs = GridSpec(numberOfRowsToPlot, 2, figure=fig) 
    ax = fig.add_subplot(gs[currentPlotRow,0])
    ax.plot(seqA, 'ro')
    ax.set_title('Raw data: Sequence A')
    ax = fig.add_subplot(gs[currentPlotRow,1])
    ax.plot(seqB, 'ro')
    ax.set_title('Raw data: Sequence B')
    currentPlotRow += 1

    if plotNormalizedData:
        ax = fig.add_subplot(gs[currentPlotRow,0])
        ax.plot(seqANorm, 'ro')
        ax.set_title('Normalized: Sequence A')
        ax = fig.add_subplot(gs[currentPlotRow,1])
        ax.plot(seqBNorm, 'ro')
        ax.set_title('Normalized: Sequence B')
        currentPlotRow += 1

    if plotCorrelations:
        currentPlotRow = plotRawCorrelations(fig, gs, currentPlotRow, seqA,seqA)  

    if plotCorrelations and plotNormalizedData:
        currentPlotRow = plotNormalizedCorrelations(fig, gs, currentPlotRow, seqANorm, seqBNorm)

    if subtractMeanFromResult:
        seqAMean = np.mean(seqA)
        seqASubtracted = seqA
        seqASubtracted[:] =[x - seqAMean for x in seqASubtracted]
        seqBSubtracted = seqB
        seqBMean = np.mean(seqB)
        seqBSubtracted[:] =[x - seqBMean for x in seqBSubtracted]
        if plotResults: currentPlotRow = plotCorrelationResults(fig, gs, currentPlotRow, seqASubtracted,seqBSubtracted)  
        if plotNormalizedResults : currentPlotRow = plotNormalizedCorrelationResults(fig, gs, currentPlotRow, seqASubtracted,seqBSubtracted)
    else:
        if plotResults: currentPlotRow = plotCorrelationResults(fig, gs, currentPlotRow, seqA,seqB)  
        if plotNormalizedResults : currentPlotRow = plotNormalizedCorrelationResults(fig, gs, currentPlotRow, seqA,seqB)  

   #fig.tight_layout()
    plt.draw()