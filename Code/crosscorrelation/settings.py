class Settings:
    def __init__(self, plotNormalizedData=False,
                 plotCorrelations=False, plotNonNormalizedResults=False,
                 plotNormalizedResults=True, subtractMeanFromResult=True,
                 drawResults=False, exportToPdf=False,
                 exportFilePath=""):
        self.plotNormalizedData = plotNormalizedData
        self.plotCorrelations = plotCorrelations
        self.plotNonNormalizedResults = plotNonNormalizedResults
        self.plotNormalizedResults = plotNormalizedResults
        self.subtractMeanFromResult = subtractMeanFromResult
        self.drawResults = drawResults
        self.exportToPdf = exportToPdf
        self.exportFilePath = exportFilePath
