import numpy as np
import matplotlib.pyplot as plt
import func_cross_correlation as fcc
import func_cross_correlation_patternsearch as ps

#  pip install numpy scipy matplotlib ipython jupyter pandas sympy nose

seq1 = np.full((1, 10000), 0)
seq2 = np.full((1, 10000), 0)


seq1[0][[1005,2005,6005,8005,9005,1505,3505,5505,6505,8505]] = 10
seq2[0][[1000,2000,6000,8000,9000,1500,3500,5500,6500,8500]] = 3


seq1 = seq1[0]
seq2 = seq2[0]

fcc.crossCorrelation(seq1, seq2)


seq3 = np.full((1, 10000), 0)
seq3[0][[1005,1007,1010, 6005,6007,6010]] = 10
seq3 = seq3[0]

pattern = np.asarray([1,0,1,0,0,1,0])

correlatedSearch = ps.searchForPattern(seq3, pattern)
indices = ps.extractIndicesFromCorrelationData(correlatedSearch, threshold= 0.3)

print(indices)

plt.show()
placeholder = 2