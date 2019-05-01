import csv
from os import listdir
from os.path import isfile, join
import numpy as np

from analysationrequest.request import AnalysationRequest


def readFiles(sourceDirectoryPath: str) -> []:
    """ Execute the categorization for all csv files in the
        given source directory. """
    print('Reading files from source path:')
    print(sourceDirectoryPath)
    files = getAllFilePathsFromDiretoryPath(sourceDirectoryPath)
    print("Found", str(len(files)), "source files")
    datasets = []
    for sourceFile in files:
        print("")
        data = readRawDataFile(sourceFile)
        data = expandRawData(data)
        datasets.append(data)

    return datasets


def getAllFilePathsFromDiretoryPath(path: str):
    """ Get all file paths in the given folder path. """
    files = [f for f in listdir(path) if isfile(join(path, f))]
    # Only use CSV-Files
    files = [k for k in files if k.endswith(".csv")]
    files = [join(path, f) for f in files]
    return files


def containsMetaData(value: []) -> bool:
    """ Check if the array contains meta data. """
    if(len(value) < 2):
        return False
    firstElementInList = value[0]
    lastElementInList = value[-1]
    # Meta data must start and end with a $ sign:
    return firstElementInList.startswith('$') \
        and lastElementInList.endswith('$')


def buildMetadataDictionary(values: []):
    """ Build a dictionary containing the meta data. """
    metaDataDictionary = {}
    currentKey = ''
    for index in range(len(values)):
        # Since the meta data is basically a list of key-value pairs,
        # every second entry is a new key. Additionally remove the
        # $ signs, which are indicators for the meta data.
        if(index % 2 == 0):
            currentKey = values[index].replace('$', '')
        else:
            metaDataDictionary[currentKey] = values[index].replace('$', '')
    
    return metaDataDictionary


def extractMetadataInformation(data, rowIndex):
    """ Extracts the meta data for a given row index. """
    if(rowIndex < 0 or (len(data) - 1) < rowIndex):
        return dict()
    # Check if the target row contains meta data:
    isMetaDataRow = containsMetaData(data[rowIndex])
    if(isMetaDataRow):
        return buildMetadataDictionary(data[rowIndex])
    else:
        return dict()
        

def readRawDataFile(sourceFile: str) -> AnalysationRequest:
    """ Read raw data files. Will only read csv files.
        The values will be parsed. """
    print("Reading data from ", sourceFile, "...")
    source = AnalysationRequest(sourceFile)
    with open(sourceFile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        cachedData = []

        # We need to read all data, since we need to lookup previous rows to
        # get the meta data:
        for row in csv_reader:
            cachedData.append(row)

        rowIndex = -1

        # Iterate the rows, each row is a sequence:
        for row in cachedData:
            rowIndex += 1

            # Handle meta-data row:
            # Basically ignoring it. The next sequence row will read the
            # the meta data from the previous row.
            isMetaDataRow = containsMetaData(row)
            if(isMetaDataRow):
                continue

            # Handle value row:
            sequence = parseValueRow(row, sourceFile, rowIndex)
            # Sequence is finished, store it:
            source.rawSequences.append(sequence)
            # Extract the meta data from the previous row.
            # This will return a empty dictionary when there is no meta data.
            source.metadataDictionaries.append(
                extractMetadataInformation(cachedData, rowIndex - 1))

    print("Found sequences: ", str(len(source.rawSequences)))
    return source


def parseValueRow(row, sourceFile, rowIndex) -> []:
    """ Parsing a value row. """
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
    return sequence


def expandRawData(data: AnalysationRequest) -> AnalysationRequest:
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


def isInteger(s: str) -> bool:
    """ Check if the given string is a integer value.
        Returns true if integer, false if not. """
    try:
        int(s)
        return True
    except ValueError:
        return False
