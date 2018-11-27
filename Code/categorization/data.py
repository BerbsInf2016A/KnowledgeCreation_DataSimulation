class BlockInfo:
    """ The BlockInfo class stroes the size of the block
        and the indices for the  block. """

    def __init__(self, blockSize):
        self.blockSize = blockSize
        self.indizes = []

    def addStartIndexEntry(self, startIndex):
        """ Add a index for a block. """
        if startIndex not in self.indizes:
            self.indizes.append(startIndex)


class CategorizationFile:
    """ A CategorzationFile contains the data which should be analyzed. """

    def __init__(self, fileName):
        self.fileName = fileName
        self.rawSequences = []
        self.sequences = []
        self.frequencyResults = []
        self.subSequenceFrequencyResults = []
        self.blockInfos = []
        self.balances = []
        self.subSequenceBalances = []

    def updateBlockInfo(self, sequenceIndex, blockSize, index):
        """ Update the stored BlockInfos for a a given sequence,
            identified by the index. """
        targetBlockInfoDictionary = self.blockInfos[sequenceIndex]
        if blockSize not in targetBlockInfoDictionary:
            blockInfo = BlockInfo(blockSize)
            blockInfo.addStartIndexEntry(index)
            targetBlockInfoDictionary[blockSize] = blockInfo
        else:
            info = targetBlockInfoDictionary[blockSize]
            info.addStartIndexEntry(index)
            targetBlockInfoDictionary[blockSize] = info

    def getBlockSizesSortedByIndex(self, sequenceIndex):
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
