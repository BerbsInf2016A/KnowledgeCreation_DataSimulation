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
        generateSubSequenceFrequencyInfoPdf(sequenceIndex, data)
        generateSubSequenceBalanceInfoPdf(sequenceIndex, data)


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


def generateSubSequenceBalanceInfoPdf(sequenceIndex,
                                      data: catData.CategorizationFile):
    """ Generate a pdf containing the balances for the sub sequences. """

    subSequenceBalances = data.subSequenceBalances[sequenceIndex]

    figure = plt.figure(constrained_layout=True)
    gs = GridSpec(3, 1, figure=figure)

    # plot buckets with size of 10
    ax = figure.add_subplot(gs[0])
    ax.plot(subSequenceBalances[0], '-')
    ax.set_title("10er SubSequenz")
    ax.set_xlabel('SubSequenz')
    ax.set_ylabel('Balance')

    # plot buckets with size of 100
    ax = figure.add_subplot(gs[1])
    ax.plot(subSequenceBalances[1], '-')
    ax.set_title("100er SubSequenz")
    ax.set_xlabel('SubSequenz')
    ax.set_ylabel('Balance')

    # plot buckets with size of 1000
    ax = figure.add_subplot(gs[2])
    ax.plot(subSequenceBalances[2], '-')
    ax.set_title("1000er SubSequenz")
    ax.set_xlabel('SubSequenz')
    ax.set_ylabel('Balance')

    # Export the pdf
    exportPath = data.fileName.replace(
        ".csv", "_SubSequences_Balances_" + str(sequenceIndex) + ".pdf")
    figure.savefig(exportPath, bbox_inches='tight')
    plt.close(figure)


def generateSubSequenceFrequencyInfoPdf(sequenceIndex,
                                        data: catData.CategorizationFile):
    """ Generate a pdf containing the frequencies for the sub sequences. """

    subSequenceFrequencies = data.subSequenceFrequencyResults[sequenceIndex]

    figure = plt.figure(constrained_layout=True)
    gs = GridSpec(3, 1, figure=figure)

    # plot buckets with size of 10
    ax = figure.add_subplot(gs[0])
    ax.plot(subSequenceFrequencies[0], '-')
    ax.set_title("10er SubSequenz")
    ax.set_xlabel('SubSequenz')
    ax.set_ylabel('Frequenz')

    # plot buckets with size of 100
    ax = figure.add_subplot(gs[1])
    ax.plot(subSequenceFrequencies[1], '-')
    ax.set_title("100er SubSequenz")
    ax.set_xlabel('SubSequenz')
    ax.set_ylabel('Frequenz')

    # plot buckets with size of 1000
    ax = figure.add_subplot(gs[2])
    ax.plot(subSequenceFrequencies[2], '-')
    ax.set_title("1000er SubSequenz")
    ax.set_xlabel('SubSequenz')
    ax.set_ylabel('Frequenz')

    # Export the pdf
    exportPath = data.fileName.replace(
        ".csv", "_SubSequences_Frequency_" + str(sequenceIndex) + ".pdf")
    figure.savefig(exportPath, bbox_inches='tight')
    plt.close(figure)


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
