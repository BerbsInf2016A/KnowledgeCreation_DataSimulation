
import os
import automated_categorization as ac


dirname = os.path.dirname(__file__)
directoryPath = os.path.join(dirname, 'source')
ac.executeCategorization(directoryPath)