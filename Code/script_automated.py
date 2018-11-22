import os
from categorization.automated_categorization import executeCategorization
import crosscorrelation.automated_crosscorrelation as crosscorrFunctions


dirname = os.path.dirname(__file__)
directoryPath = os.path.join(dirname, 'sourceFiles')
categorizedDatasets = executeCategorization(directoryPath)
crosscorrFunctions.executeCrossCorrelationForDatasets(categorizedDatasets)
