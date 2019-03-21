class BlockInfo:
    """ The BlockInfo class stores the size of the block
        and the indices for the  block. """

    def __init__(self, blockSize):
        self.blockSize = blockSize
        self.indizes = []

    def addStartIndexEntry(self, startIndex: int):
        """ Add a index for a block. """
        if startIndex not in self.indizes:
            self.indizes.append(startIndex)


class AnalysationRequest:
    """ A AnalysationFile contains the data which should be analyzed. """

    def __init__(self, fileName):
        self.fileName = fileName
        self.rawSequences = []
        self.sequences = []
        self.frequencyResults = []
        self.subSequenceFrequencyResults = []
        self.blockInfos = []
        self.balances = []
        self.subSequenceBalances = []

    def updateBlockInfoForSequence(self, sequenceIndex: int, blockSize: int, blockIndex: int):
        """ Update the stored BlockInfos for a a given sequence,
            identified by the blockindex. """
        targetBlockInfoDictionary = self.blockInfos[sequenceIndex]
        if blockSize not in targetBlockInfoDictionary:
            blockInfo = BlockInfo(blockSize)
            blockInfo.addStartIndexEntry(blockIndex)
            targetBlockInfoDictionary[blockSize] = blockInfo
        else:
            info = targetBlockInfoDictionary[blockSize]
            info.addStartIndexEntry(blockIndex)
            targetBlockInfoDictionary[blockSize] = info

    def getBlockSizesForSequenceSortedByIndex(self, sequenceIndex: int):
        """ Get the BlockInfos, sorted by the indices of their occurrences. """
        if sequenceIndex < len(self.blockInfos):
            blockInfos = self.blockInfos[sequenceIndex]
            sortedByIndex = list()
            for blocksize, value in blockInfos.items():
                for index in value.indizes:
                    sortedByIndex.append([index, blocksize])

            return sorted(sortedByIndex, key=lambda x: x[0])
        else:
            return []
