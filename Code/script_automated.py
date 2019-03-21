import os
from categorization.automated_categorization import executeCategorization
import crosscorrelation.automated_crosscorrelation as crosscorrFunctions
import analysationrequest.functions as fileAccessFuntions

# You need the dependencies define in "dependencies.txt" installed to run this
# script.

# Get the directory path of where this script is executed:
dirname = os.path.dirname(__file__)
# Build the path for the source folder:
directoryPath = os.path.join(dirname, 'sourceFiles')
# Read the csv source files and expand them:
requests = fileAccessFuntions.readFiles(directoryPath)
# Execute the categorization: Calculating the balance, frequency and
# block-infos:
categorizedDatasets = executeCategorization(requests)
# This will calculate the cross correlation between sequences in the same
# source file. Additionally, the sequences must have the same length.
crosscorrFunctions.executeCrossCorrelationForDatasets(categorizedDatasets)
