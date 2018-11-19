import csv
import numpy as np

from os import listdir, path
from os.path import isfile, join

from categorization.functions import analyzeFrequency, analyzeBalance 
import categorization.data as catData
from categorization.pdfGeneration import generatePdfsForDataset

def representsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def getAllFilePathsFromDiretoryPath(path):
    files = [f for f in listdir(path) if isfile(join(path, f))]
    files = [k for k in files if k.endswith(".csv")]
    files = [ join(path,f) for f in files]
    return files

def readRawDataFile(sourceFile: str):
    print("Reading data from ", sourceFile ,"...")
    source = catData.CategorizationFile(sourceFile)
    with open(sourceFile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        rowIndex = -1
        for row in csv_reader:
            rowIndex += 1
            sequence = []
            for entry in row:
                # Split the entry
                splitted = entry.split("|")
                if  len(splitted) != 2:
                    raise ValueError('Error during parsing of file: ', sourceFile, " in row ", rowIndex)
                # Parse the values
                # Check if the values are valid: isDigit only returns true, when the value is an integer and positive.
                countIsValid = splitted[0].isdigit()
                if countIsValid == False :    
                    raise ValueError('Error during parsing of file: ', sourceFile, " in row ", rowIndex, " entry ", entry, " count is invalid")
                valueValid = representsInt(splitted[1])
                if valueValid == False:    
                    raise ValueError('Error during parsing of file: ', sourceFile, " in row ", rowIndex, " entry ", entry, " value is invalid")
                sequence.append([int(splitted[0]),int(splitted[1])])
            source.rawSequences.append(sequence)

    print("Found sequences: " , str(len(source.rawSequences)))
    return source

def expandRawData(data: catData.CategorizationFile):
    data.sequences = np.empty(len(data.rawSequences), dtype=object)
    for sequenceIndex, sequence in enumerate(data.rawSequences):
        print("Expanding data for", data.fileName,"Sequence", sequenceIndex)
        expandedSequence = []
        for entry in enumerate(sequence):
            counter = entry[1][0]
            value = entry[1][1]
            extendedData = [value] * counter
            expandedSequence.extend(extendedData) 
        data.sequences[sequenceIndex] = expandedSequence
        
    return data


def executeCategorization(sourceDirectoryPath: str):
    print('Executing categorization: source path:')
    print(sourceDirectoryPath)
    files = getAllFilePathsFromDiretoryPath(sourceDirectoryPath)
    print("Found", str(len(files)), "source files")
    datasets = []
    for sourceFile in files:
        print("")
        data = readRawDataFile(sourceFile)
        data = expandRawData(data)
        data = analyzeFrequency(data)
        data = analyzeBalance(data)
        print("Calculating block size information for", data.fileName)
        data.calculateBlockInfos()
        datasets.append(data)
        
    print("\nGenerating pdfs...")
    for dataset in datasets:
         generatePdfsForDataset(dataset)
       
