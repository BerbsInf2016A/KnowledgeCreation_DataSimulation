import numpy as np
from categorization.data import CategorizationFile

def analyzeFrequency(data: CategorizationFile):    
    data.frequencyResults = np.ndarray(len(data.sequences),float)    
    for sequenceIndex, sequence in enumerate(data.sequences):
        print("Calculating frequency for", data.fileName,"Sequence", sequenceIndex)
        data.frequencyResults[sequenceIndex] = calculateFrequencyForSequence(sequence)
        
    return data

def analyzeBalance(data: CategorizationFile):
    data.balances = np.ndarray(len(data.sequences),float)    
    for sequenceIndex, sequence in enumerate(data.sequences):
        print("Calculating balance for", data.fileName,"Sequence", sequenceIndex)
        data.balances[sequenceIndex] = calculateBalanceForSequence(sequence)
        
    return data

def calculateFrequencyForSequence(sequence):
    oldValue = 0
    changeCounter = 0
    for index, value in enumerate(sequence):
        if index == 0:
            oldValue = value
            continue
        if oldValue != value:
            changeCounter += 1
            oldValue = value
    
    if changeCounter == 0 or len(sequence) == 0:
        return 1
    else:
        return np.round((changeCounter / len(sequence)), 2)

def calculateBalanceForSequence(sequence):
    counter = 0
    if  len(sequence) == 0:
        return 1
    for value in sequence:
        if value == 1:
            counter += 1
    return np.round((counter / len(sequence)), 2)

