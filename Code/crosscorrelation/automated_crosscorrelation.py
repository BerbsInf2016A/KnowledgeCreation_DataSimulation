import crosscorrelation.settings as crossSettings
import crosscorrelation.functions_crosscorrelation as fcc


def executeCrossCorrelationForDatasets(datasets: []):
    for dataset in datasets:
        if len(dataset.sequences) >= 2:
            print("\nCrosscorrelation for file", dataset.fileName)
            for firstIndex, firstSequence in enumerate(dataset.sequences):
                for secondIndex, secondSequence in enumerate(dataset.sequences):
                    if secondIndex <= firstIndex:
                        continue
                    if len(firstSequence) != len(secondSequence):
                        print(dataset.fileName,
                              "Cross-Correlation between sequence",
                              str(firstIndex), "and",
                              str(secondIndex),
                              "ignored. Sequence-Length not equal!")
                        continue
                    print(dataset.fileName,
                          "exporting Cross-Correlation between sequence",
                          str(firstIndex), "and", str(secondIndex))
                    exportPath = dataset.fileName.replace(
                        ".csv",  "_CrossCorrelation_Sequence_" +
                        str(firstIndex)
                        + "_Sequence_" + str(secondIndex) + ".pdf")

                    correlationSettings = crossSettings.Settings()
                    correlationSettings.exportToPdf = True
                    correlationSettings.exportFilePath = exportPath
                    fcc.crossCorrelation(firstSequence, secondSequence,
                                         correlationSettings)
