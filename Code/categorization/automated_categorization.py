import categorization.functions as catFunc
from categorization.pdfGeneration import generatePdfsForDataset
import analysationrequest.request as request
from typing import List


def executeCategorization(requests: List[request.AnalysationRequest]) -> []:
    """ Execute the categorization for all csv files in the
        given source directory. """
  
    for data in requests:
        print("")
        data = catFunc.analyzeFrequency(data)
        data = catFunc.analyzeBalance(data)
        print("Calculating block size information for", data.fileName)
        data = catFunc.calculateBlockInfos(data)

    print("\nGenerating pdfs...")
    for dataset in requests:
        generatePdfsForDataset(dataset)
    return requests
