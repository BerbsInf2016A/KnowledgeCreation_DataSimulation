import numpy as np
import matplotlib.pyplot as plt
import func_cross_correlation as fcc

#  pip install numpy scipy matplotlib ipython jupyter pandas sympy nose

seq1 = np.full((1, 10000), 0)
seq2 = np.full((1, 10000), 10)


seq1[0][[1005,2005,6005,8005,9005,1505,3505,5505,6505,8505]] = 10
seq2[0][[1000,2000,6000,8000,9000,1500,3500,5500,6500,8500]] = 2


seq1 = seq1[0]
seq2 = seq2[0]

fcc.crossCorrelation(seq1, seq2, subtractMeanFromResult= True, plotResults= False )

plt.show()

placeholder = 2