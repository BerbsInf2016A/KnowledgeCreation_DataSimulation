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


    def calculateBlockInfos(self):
        self.blockInfos = np.empty(len(self.sequences), dtype=object)
        for i in range(0, len(self.sequences)):   
            self.blockInfos[i] = {}
        for sequenceIndex, sequence in  enumerate(self.rawSequences):
            index = 0
            for sequenceEntry in sequence:
                blocksize = sequenceEntry[0]
                self.updateBlockInfo(sequenceIndex, blocksize, index)
                index += blocksize
            

        
