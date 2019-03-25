import numpy as np
import matplotlib.pyplot as plt
import crosscorrelation.functions_crosscorrelation as fcc
import crosscorrelation.functions_crosscorrelation_patternsearch as ps
import crosscorrelation.settings as crossSettings

seq1 = np.full((1, 10000), 0)
seq2 = np.full((1, 10000), 0)


seq1[0][[1005, 2005, 1505, 3505, 5505, 6005, 6505, 8005, 8505, 9005]] = 1
seq2[0][[1000, 2000, 1500, 3500, 5500, 6000, 6500, 8000, 8500, 9000]] = 1


seq1 = seq1[0]
seq2 = seq2[0]

settings = crossSettings.Settings()
settings.drawResults = True
settings.plotNormalizedData = True
settings.plotCorrelations = True
fcc.crossCorrelation(seq1, seq2, settings)
# Show the results in a window. Attention: This will block the execution:
# plt is from matplotlib
if settings.drawResults:
    plt.show()


seq3 = np.full((1, 10000), 0)
seq3[0][[1005, 1007, 1010, 6005, 6007, 6010]] = 1

pattern = np.asarray([1, 0, 1, 0, 0, 1, 0])

correlatedSearch = ps.getCorrelationDataForPatternSearch(seq3, pattern)
indices = ps.extractIndicesFromCorrelationData(correlatedSearch, threshold=0.2)

print(indices)
onlinIndices = []
for entry in indices:
    onlinIndices.append(entry[0])
onlinIndices.sort()
print(onlinIndices)
plt.show()
placeholder = 2
