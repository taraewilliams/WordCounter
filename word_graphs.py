import matplotlib.pyplot as plt

def create_pie_chart_words(words, colors = []):

    labels = []
    sizes = []
    for word in words:
        labels.append(word[0])
        sizes.append(word[1])

    create_pie_chart(labels, sizes, colors)


def create_pie_chart_word_groups(words, colors = []):

    labels = []
    sizes = []
    for word in words:
        labels.append(word["words"][0])
        sizes.append(word["count"])

    create_pie_chart(labels, sizes, colors)


def create_pie_chart(labels, sizes, colors = []):
    if (len(colors) > 0):
        patches, texts = plt.pie(sizes, colors = colors, shadow=True, startangle=90)
    else:
        patches, texts = plt.pie(sizes, shadow=True, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.axis('equal')
    plt.show()
