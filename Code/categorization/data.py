import numpy as np

class BlockInfo:
    def __init__(self, blockSize):
        self.blockSize = blockSize
        self.indizes = []        
    
    def addStartIndexEntry(self, startIndex):
        self.indizes.append(startIndex)

class CategorizationFile:
    def __init__(self, fileName):
        self.fileName = fileName
        self.rawSequences = []
        self.sequences = []
        self.frequencyResults = []
        self.blockInfos = []
        self.balances =[]

    def updateBlockInfo(self, sequenceIndex, blockSize, index):
        targetBlockInfoDictionary = self.blockInfos[sequenceIndex]
        if not blockSize in targetBlockInfoDictionary:
            blockInfo = BlockInfo(blockSize)
            blockInfo.addStartIndexEntry(index)
            targetBlockInfoDictionary[blockSize] = blockInfo
        else:
            info = targetBlockInfoDictionary[blockSize]
            info.addStartIndexEntry(index)
            targetBlockInfoDictionary[blockSize] = info
    
    def getBlockSizesSortedByIndex(self, sequenceIndex):
        if sequenceIndex < len(self.blockInfos):
            blockInfos = self.blockInfos[sequenceIndex]
            sortedByIndex = list()
            for blocksize, value in blockInfos.items():
                for index in value.indizes:
                    sortedByIndex.append([index, blocksize])
            
            
            return sorted(sortedByIndex, key=lambda x: x[0])
        else:
            return []

