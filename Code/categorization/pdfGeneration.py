import numpy as np
from matplotlib.gridspec import GridSpec
from matplotlib.font_manager import FontProperties
import categorization.data as catData
import matplotlib.pyplot as plt


def generatePdfsForDataset(data: catData.CategorizationFile):
    """ Generate the pdfs for a dataset. """
    for sequenceIndex, sequence in enumerate(data.sequences):
        print("Generating pdf reports for",
              data.fileName, "Sequence", sequenceIndex)
        generateSummaryPdf(sequenceIndex, sequence, data)
        #generateBlockInfoPdf(sequenceIndex, sequence, data)


def resolveFrequencyValueToDescriptiveString(value):
    """ Resolve a frequency value to a more descriptive string. """
    if value <= 0.25:
        return "Niederfrequent"
    if value > 0.25 and value < 0.75:
        return "Mittelfrequent"
    if value >= 0.75:
        return "Hochfrequent"
    return "Unbekannt"


def resolveBalanceValueToDescriptiveString(value):
    """ Resolve a balance value to a more descriptive string. """
    if value >= 0.4 and value <= 0.6:
        return "Ausgeglichen"
    if value < 0.4 or value > 0.6:
        return "Unausgeglichen"
    return "Unbekannt"


def generateSummaryPdf(sequenceIndex, sequence,
                       data: catData.CategorizationFile):
    """ Generate a summary pdf for a sequnce in a given data file. """

    figure = plt.figure(constrained_layout=True)
    gs = GridSpec(3, 1, figure=figure)
    # plot sequence
    ax = figure.add_subplot(gs[0])
    ax.plot(sequence, 'ro')
    ax.set_title("Sequenz")
    ax.set_xlabel('Index')
    ax.set_ylabel('Wert')

    # The middle row is empty and used as a separator between the subfigures.

    # plot summary
    ax = figure.add_subplot(gs[2])
    ax.axis('off')
    ax.axis('tight')
    ax.set_title("Sequenzeigenschaften")
    columns = ('Eigenschaft', 'Wert')
    tableData = []
    # Write Length into the table
    tableData.append(["Länge", len(sequence)])
    frequencyString = str(data.frequencyResults[sequenceIndex]) + ' - ' + \
        resolveFrequencyValueToDescriptiveString(
            data.frequencyResults[sequenceIndex])

    # Write Frequency into the table
    tableData.append(["Frequenz", frequencyString])
    balanceString = str(data.balances[sequenceIndex]) + " - " + \
        resolveBalanceValueToDescriptiveString(data.balances[sequenceIndex])

    # Write Balance into the table
    tableData.append(["Balance", balanceString])
    table = ax.table(cellText=tableData, colLabels=columns,
                     loc='center', cellLoc="left", colLoc="left")

    # Set first row (header) text to bold
    for (row, col), cell in table.get_celld().items():
        if (row == 0) or (col == -1):
            cell.set_text_props(fontproperties=FontProperties(weight='bold'))

    # Export the pdf
    exportPath = data.fileName.replace(
        ".csv",  "_Sequence_" + str(sequenceIndex) + ".pdf")
    figure.savefig(exportPath, bbox_inches='tight')
    plt.close(figure)


def generateBlockInfoPdf(sequenceIndex, sequence,
                         data: catData.CategorizationFile):
    """ Generate a block info pdf. """

    figure = plt.figure(constrained_layout=True)
    gs = GridSpec(3, 1, figure=figure)
    '''
    ax = figure.add_subplot(gs[0])
    ax.axis('off')
    ax.axis('tight')
    ax.set_title("Blockeigenschaften")
    columns = ('BlockSize', 'Count', 'Indizes')

    # Plot the blocks descending by the block size:
    sequenceBlockInfo = data.blockInfos[sequenceIndex]
    sortedBlockInfos = sorted(sequenceBlockInfo.items(
    ), key=lambda kv: kv[1].blockSize, reverse=True)
    tableData = []
    for i in range(0, len(sequenceBlockInfo)):
        blockInfo = sortedBlockInfos[i][1]
        indizes = ",".join(map(str, blockInfo.indizes))
        tableData.append(
            [blockInfo.blockSize, len(blockInfo.indizes), indizes])

    table = ax.table(cellText=tableData, colLabels=columns, colWidths=[
                     0.3, 0.3, 0.9], loc='center', colLoc="left")

    # Set first row (header) text to bold
    for (row, col), cell in table.get_celld().items():
        if (row == 0) or (col == -1):
            cell.set_text_props(fontproperties=FontProperties(weight='bold'))

'''
    # Plot block size diagram
    blockSizeIndices = data.getBlockSizesSortedByIndex(sequenceIndex)
    ax = figure.add_subplot(gs[1])
    ax.set_title("Blöcke über die Zeit")
    ax.set_xlabel('Index')
    ax.set_ylabel('Blockgröße')
    # Only the blocksizes are needed:
    yValues = []
    xValues = []
    for entry in blockSizeIndices:
       # xValues.append(entry[0])
        yValues.append(entry[1])

    #plt.xticks(np.arange(len(xValues)), xValues)
    #ax.bar(np.arange(len(xValues)), yValues)
    ax.bar(np.arange(len(yValues)), yValues)

    '''
    # Plot block size counts
    ax = figure.add_subplot(gs[2])
    ax.axis('off')
    ax.axis('tight')
    ax.set_title("Blockanzahl")
    columns = ('Count', 'BlockSize')
    sequenceBlockInfo = data.blockInfos[sequenceIndex]
    sortedBlockInfos = sorted(sequenceBlockInfo.items(
    ), key=lambda kv: len(kv[1].indizes), reverse=True)
    tableData = []

    for i in range(0, len(sequenceBlockInfo)):
        blockInfo = sortedBlockInfos[i][1]
        tableData.append([len(blockInfo.indizes), blockInfo.blockSize])

    table = ax.table(cellText=tableData, colLabels=columns,
                     colWidths=[0.25, 0.75], loc='center')
    # Set first row (header) text to bold
    for (row, col), cell in table.get_celld().items():
        if (row == 0) or (col == -1):
            cell.set_text_props(fontproperties=FontProperties(weight='bold'))

    '''
    exportPath = data.fileName.replace(
        ".csv",  "_Blocks_Sequence_" + str(sequenceIndex) + ".pdf")
    figure.savefig(exportPath, bbox_inches='tight')
    plt.close(figure)
