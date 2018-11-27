import numpy as np
from categorization.data import CategorizationFile


def analyzeFrequency(data: CategorizationFile):
    """ Analyze the frequency for all given sequences. """
    data.frequencyResults = np.ndarray(len(data.sequences), float)
    data.subSequenceFrequencyResults = np.ndarray(len(data.sequences), object)
    for sequenceIndex, sequence in enumerate(data.sequences):
        print("Calculating frequency for",
              data.fileName, "Sequence", sequenceIndex)
        data.frequencyResults[sequenceIndex] = calculateFrequencyForSequence(
            sequence)
        data.subSequenceFrequencyResults[sequenceIndex] = calculateFrequenciesForSubSequences(
            sequence)

    return data


def analyzeBalance(data: CategorizationFile):
    """ Analyze the balance for all given sequences. """
    data.balances = np.ndarray(len(data.sequences), float)
    data.subSequenceBalances = np.ndarray(len(data.sequences), object)
    for sequenceIndex, sequence in enumerate(data.sequences):
        print("Calculating balance for",
              data.fileName, "Sequence", sequenceIndex)
        data.balances[sequenceIndex] = calculateBalanceForSequence(sequence)
        data.subSequenceBalances[sequenceIndex] = calculateBalancesForSubSequences(sequence)

    return data


def calculateBlockInfos(data: CategorizationFile):
    """ Calculate the BlockInfos for all given sequences. """
    data.blockInfos = np.empty(len(data.sequences), dtype=object)
    for i in range(0, len(data.sequences)):
        data.blockInfos[i] = {}
    for sequenceIndex, sequence in enumerate(data.sequences):
        print("Calculating block infos for",
              data.fileName, "Sequence", sequenceIndex)
        calculatedBlockInfos = calculateBlockInfosForSequence(sequence)
        for blockInfo in calculatedBlockInfos:
            data.updateBlockInfo(sequenceIndex, blockInfo[1], blockInfo[0])

    return data


def calculateBalancesForSubSequences(sequence):
    """ Calculate the balances for the sub sequences. """
    list10 = np.array_split(sequence, 1000)
    list100 = np.array_split(sequence, 100)
    list1000 = np.array_split(sequence, 10)

    resultList = []
    result10 = []
    for entry in list10:
        result10.append(calculateBalanceForSequence(entry))
    resultList.append(result10)

    result100 = []
    for entry in list100:
        result100.append(calculateBalanceForSequence(entry))
    resultList.append(result100)

    result1000 = []
    for entry in list1000:
        result1000.append(calculateBalanceForSequence(entry))
    resultList.append(result1000)

    return resultList


def calculateFrequenciesForSubSequences(sequence):
    """ Calculate the frequency for the sub sequences. """
    list10 = np.array_split(sequence, 1000)
    list100 = np.array_split(sequence, 100)
    list1000 = np.array_split(sequence, 10)

    resultList = []
    result10 = []
    for entry in list10:
        result10.append(calculateFrequencyForSequence(entry))
    resultList.append(result10)

    result100 = []
    for entry in list100:
        result100.append(calculateFrequencyForSequence(entry))
    resultList.append(result100)

    result1000 = []
    for entry in list1000:
        result1000.append(calculateFrequencyForSequence(entry))
    resultList.append(result1000)

    return resultList


def calculateFrequencyForSequence(sequence):
    """ Calculate the frequency for a given sequence.
        Returns a value between 0 and 1. A value near 0 is a infrequent
        sequence, a value near 1 is highly frequent sequence. """
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
        return 0
    else:
        return np.round((changeCounter / len(sequence)), 2)


def calculateBalanceForSequence(sequence):
    """ Calculate the balance for a sequence.
        The balance is calculated with the following formula:+
        Count of occurences of 1 / length of sequence.
        A squence with a value around 0.5 is balanced, all others
        are unbalanced. """
    counter = 0
    if len(sequence) == 0:
        return 1
    for value in sequence:
        if value == 1:
            counter += 1
    return np.round((counter / len(sequence)), 2)


def calculateBlockInfosForSequence(sequence):
    """ Calculate the BlockInformation for a sequence. """
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
