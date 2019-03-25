import os
from categorization.automated_categorization import executeCategorization
import analysationrequest.functions as fileAccessFuntions

# Get the directory path of where this script is executed:
dirname = os.path.dirname(__file__)
# Build the path for the source folder:
directoryPath = os.path.join(dirname, 'sourceFiles')
# Read the csv source files and expand them:
requests = fileAccessFuntions.readFiles(directoryPath)
# Execute the categorization: Calculating the balance, frequency and
# block-infos:
executeCategorization(requests)