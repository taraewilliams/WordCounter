import matplotlib.pyplot as plt


def create_pie_chart_words(words: list, colors: list = [], grouped: bool = False):
    """
    Create a pie chart for words in a list.

    Parameters
    ----------
    words: list[[str, int]] (ungrouped) OR list[ { words: list[str], count: int } ] (grouped)
        The list of words and word counts to make a pie chart of.
    colors: list[str], optional
        Colors of the pie chart.

    Returns
    -------
    No return value
    """
    labels, sizes = [], []
    for word in words:
        if grouped:
            labels.append(word["words"][0])
            sizes.append(word["count"])
        else:
            labels.append(word[0])
            sizes.append(word[1])

    create_pie_chart(labels, sizes, colors)


#####################################################
### Private Functions ###
#####################################################


def create_pie_chart(labels, sizes: list, colors: list = []):
    """
    Create a pie chart.

    Parameters
    ----------
    labels: list[str]
        The list of words.
    sizes: list[int]
        The list of word counts.
    colors: list[str], optional
        Colors of the pie chart.

    Returns
    -------
    No return value
    """
    if (len(colors) > 0):
        patches, other = plt.pie(sizes, colors=colors, shadow=True, startangle=90)
    else:
        patches, other = plt.pie(sizes, shadow=True, startangle=90)

    plt.legend(patches, labels, loc="best")
    plt.axis('equal')
    plt.show()
