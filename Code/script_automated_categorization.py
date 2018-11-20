import os
from categorization.automated_categorization import executeCategorization


dirname = os.path.dirname(__file__)
directoryPath = os.path.join(dirname, 'sourceFiles')
executeCategorization(directoryPath)
