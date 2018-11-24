import csv
import numpy as np

from os import listdir
from os.path import isfile, join

import categorization.functions as catFunc
import categorization.data as catData
from categorization.pdfGeneration import generatePdfsForDataset


def isInteger(s: str):
    """ Check if the given string is a integer value.
        Returns true if integer, false if not. """
    try:
        int(s)
        return True
    except ValueError:
        return False


def getAllFilePathsFromDiretoryPath(path):
    """ Get all file paths in the given folder path. """
    files = [f for f in listdir(path) if isfile(join(path, f))]
    files = [k for k in files if k.endswith(".csv")]
    files = [join(path, f) for f in files]
    return files


def readRawDataFile(sourceFile: str):
    """ Read raw data files. Will only read csv files.
        The values will be parsed. """
    print("Reading data from ", sourceFile, "...")
    source = catData.CategorizationFile(sourceFile)
    with open(sourceFile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        rowIndex = -1
        # Iterate the rows, each row is a sequence:
        for row in csv_reader:
            rowIndex += 1
            sequence = []
            for entry in row:
                # Split the entry
                splitted = entry.split("|")
                if len(splitted) != 2:
                    raise ValueError('Error during parsing of file: ',
                                     sourceFile,
                                     " in row ",
                                     rowIndex)
                # Parse the values
                # Check if the values are valid: isDigit only returns true,
                # when the value is an integer and positive.
                count = splitted[0]
                countIsValid = count.isdigit()
                if countIsValid is False:
                    raise ValueError('Error during parsing of file: ',
                                     sourceFile,
                                     " in row ",
                                     rowIndex,
                                     " entry ",
                                     entry,
                                     " count is invalid")
                value = splitted[1]
                valueValid = isInteger(value)
                if valueValid is False:
                    raise ValueError('Error during parsing of file: ',
                                     sourceFile,
                                     " in row ", rowIndex, " entry ", entry,
                                     " value is invalid")
                # Count and value are valid. Cast the to int and save them.
                sequence.append([int(count), int(value)])
            # Sequence is finished, store it:
            source.rawSequences.append(sequence)

    print("Found sequences: ", str(len(source.rawSequences)))
    return source


def expandRawData(data: catData.CategorizationFile):
    """ Expand the compressed sequences in a data file to full sequences. """
    data.sequences = np.empty(len(data.rawSequences), dtype=object)
    for sequenceIndex, sequence in enumerate(data.rawSequences):
        print("Expanding data for", data.fileName, "Sequence", sequenceIndex)
        expandedSequence = []
        for entry in sequence:
            counter = entry[0]
            value = entry[1]
            extendedData = [value] * counter
            expandedSequence.extend(extendedData)
        data.sequences[sequenceIndex] = expandedSequence

    return data


def executeCategorization(sourceDirectoryPath: str):
    """ Execute the categorization for all csv files in the
        given source directory. """
    print('Executing categorization: source path:')
    print(sourceDirectoryPath)
    files = getAllFilePathsFromDiretoryPath(sourceDirectoryPath)
    print("Found", str(len(files)), "source files")
    datasets = []
    for sourceFile in files:
        print("")
        data = readRawDataFile(sourceFile)
        data = expandRawData(data)
        data = catFunc.analyzeFrequency(data)
        data = catFunc.analyzeBalance(data)
        print("Calculating block size information for", data.fileName)
        data = catFunc.calculateBlockInfos(data)
        datasets.append(data)

    print("\nGenerating pdfs...")
    for dataset in datasets:
        generatePdfsForDataset(dataset)
    return datasets
