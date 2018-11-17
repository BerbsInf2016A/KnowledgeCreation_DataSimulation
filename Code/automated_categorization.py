from os import listdir, path
from os.path import isfile, join
import os
import data_categorization as data
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

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

def readRawDataFile(sourceFile):
    print("Reading data from ", sourceFile ,"...")
    source = data.CategorizationFile(sourceFile)
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
            source.sequences.append(sequence)

    print("Found sequences: " , str(len(source.sequences)))
    return source

def expandRawData(data):
    for sequenceIndex, sequence in enumerate(data.sequences):
        print("Expanding data for", data.fileName,"Sequence", sequenceIndex)
        expandedSequence = []
        for entry in enumerate(sequence):
            counter = entry[1][0]
            value = entry[1][1]
            extendedData = [value] * counter
            expandedSequence.extend(extendedData) 
        data.sequences[sequenceIndex] = expandedSequence
        
    return data

            
            

def analyzeFrequency(data):    
    data.frequencyResults = np.ndarray(len(data.sequences),float)    
    for sequenceIndex, sequence in enumerate(data.sequences):
        print("Calculating frequency for", data.fileName,"Sequence", sequenceIndex)
        oldValue = 0
        changeCounter = 0
        for index, value in enumerate(sequence):
            if index == 0:
                oldValue = index
                continue
            if oldValue != value:
                changeCounter += 1
                oldValue = value
        
        if changeCounter == 0 or len(sequence) == 0:
            data.frequencyResults[sequenceIndex] = 1
        else:
            data.frequencyResults[sequenceIndex] = changeCounter / len(sequence)

    return data

def generatePdfs(data):
    for sequenceIndex, sequence in enumerate(data.sequences):
        print("Generating pdf report for", data.fileName,"Sequence", sequenceIndex)
        figure = plt.figure(constrained_layout=True)
        gs = GridSpec(2, 1, figure=figure) 
        # plot sequence
        ax = figure.add_subplot(gs[0])
        ax.plot(sequence, 'ro')
        #ax.set_title(data.fileName + ': Sequence ' + str(sequenceIndex))
        
        if  (len(data.frequencyResults) - 1) >= sequenceIndex:
            ax = figure.add_subplot(gs[1]) 
            ax.axis('off')
            ax.axis('tight')
            columns = ('Length','FrequencyIndex')
            tableData = []
            tableData.append([len(sequence), data.frequencyResults[sequenceIndex]])
            ax.table(cellText=tableData,colLabels=columns,loc='bottom')        
        
        exportPath = data.fileName.replace(".csv",  "_Sequence_" + str(sequenceIndex) + ".pdf")
        figure.savefig(exportPath, bbox_inches='tight')

    
            

def executeCategorization(sourceDirectoryPath):
    print('Executing categorization: source path:')
    print(sourceDirectoryPath)
    files = getAllFilePathsFromDiretoryPath(sourceDirectoryPath)
    print("Found"+ str(len(files)), "source files")
    for sourceFile in files:
        data = readRawDataFile(sourceFile)
        data = expandRawData(data)
        data = analyzeFrequency(data)
        generatePdfs(data)
