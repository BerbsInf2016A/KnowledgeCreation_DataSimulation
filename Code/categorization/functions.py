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

def analyzeBlockInfos(data: CategorizationFile):
    data.blockInfos = np.empty(len(data.sequences), dtype=object)
    for i in range(0, len(data.sequences)):   
        data.blockInfos[i] = {}
    for sequenceIndex, sequence in enumerate(data.sequences):
        print("Calculating block infos for", data.fileName,"Sequence", sequenceIndex)
        calculatedBlockInfos = calculateBlockInfosForSequence(sequence)
        for blockInfo in calculatedBlockInfos:
            data.updateBlockInfo(sequenceIndex, blockInfo[1], blockInfo[0])
        
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

def calculateBlockInfosForSequence(sequence):        
    blockinfos = []
    currentValue = 0
    currentValueCounter = 0
    startIndex = 0
    for index, value in enumerate(sequence):
        if index == 0:
            currentValue = value
            currentValueCounter += 1
            continue

        if currentValue == value:
            currentValueCounter += 1                    
        else:
            blockinfos.append([startIndex, currentValueCounter])
            currentValueCounter = 1
            currentValue = value
            startIndex = index
    blockinfos.append([startIndex, currentValueCounter])
    return blockinfos


