import docx
import re
import unidecode
from pprint import pprint
import csv
from os import path

import matplotlib.pyplot as plt
import word_calculations as wordcalc
import word_graphs as wordgraph

def main(file_name):

    document = docx.Document(file_name)
    text = '\n'.join([paragraph.text for paragraph in document.paragraphs])
    text = text.replace('\n', ' ')
    text = text.replace("\u2026", ' ')

    quotations = "\u201c|\u201d"
    periods = "\.| \.| \. |\. "
    spaces = " |  "
    commas = "\,| \,| \, |\, "
    question_marks = "\?| \?| \? |\? "
    exclamation_points = "\!| \!| \! |\! "
    other = "\;|\; |\:|\: |\.\.\."
    split_string = quotations + "|" + periods + "|" + spaces + "|" + commas + "|" + question_marks + "|" + exclamation_points + "|" + other

    text_array = re.split(split_string, text)

    pretty_text = []
    for text_item in text_array:
        pretty_text.append(unidecode.unidecode(text_item))

    # get_names(pretty_text)
    # get_colors(pretty_text)
    # get_word_counts(pretty_text)
    get_words_counts_significant_words(pretty_text)


def get_names(pretty_text):
    name_groups = [["Philecta", "Philecta's"], ["Pilar", "Pilar's"], ["Lin", "Lin's"], ["Agatha", "Agatha's", "Aggie", "Aggie's"],
        ["Archibald", "Archibald's", "Archie's", "Archie"], ["Mabel", "Mabel's"], ["Demetri", "Demetri's", "Demetrius", "Demetrius's"],
        ["Ivan", "Ivan's"], ["Mitchie", "Mitchie's", "Michelle", "Michelle's"], ["Sabrina", "Sabrina's"], ["Eris", "Eris'", "Arianna", "Arianna's"],
        ["Teddy", "Teddy's"], ["Oma", "Oma's"], ["Gareth", "Gareth's"], ["Roxie", "Roxie's", "Ethel", "Ethel's"], ["Thaddeus", "Thaddeus'", "Tad"],
        ["Shadow", "Shadow's", "Elijah", "Elijah's"], ["Nathaniel", "Nathaniel's"], ["Rose", "Rose's"], ["Gloria", "Gloria's"], ["Blaise", "Blaise's"],
        ["Sesi", "Sesi's"], ["Leo", "Leo's", "Leonardo", "Leonardo's"], ["Absalom", "Absalom's"], ["Mead", "Olivia"], ["Sophia", "Jones"], ["Boren", "Helga"],
        ["Paula", "Davis"], ["McLellan", "Michael"], ["Jeanie"]]
    name_group_counts = wordcalc.get_word_array_include_word_groups(pretty_text, name_groups)
    sorted_names = wordcalc.sort_word_array_with_groups(name_group_counts)
    pprint(sorted_names)
    wordgraph.create_pie_chart_word_groups(sorted_names)


def get_colors(pretty_text):
    colors = ["blue", "brown", "red", "orange", "yellow", "pink", "green", "black", "violet", "purple", "gray", "indigo", "tan", "beige", "white"]
    color_counts = wordcalc.get_word_array_include_words(pretty_text, colors)
    sorted_colors = wordcalc.sort_word_array(color_counts)
    pprint(sorted_colors)

    labels = []
    for sorted_color in sorted_colors:
        labels.append(sorted_color[0])

    wordgraph.create_pie_chart_words(sorted_colors, labels)


def get_word_counts(pretty_text):
    word_counts = wordcalc.get_word_array(pretty_text)
    sorted_words = wordcalc.sort_word_array(word_counts)
    pprint(sorted_words)


def get_words_counts_significant_words(pretty_text):
    group_words = [["girl", "girls", "woman", "women", "mother", "mom", "mommy", "daughter"],
        ["boy", "boys", "man", "men", "father", "dad", "daddy", "son"],
        ["face", "cheeks", "nose", "eyes", "mouth", "ears", "ear"],
        ["read", "library", "libraries", "book", "books", "journal", "journals"],
        ["is", "was", "are", "were", "be", "wasn't", "isn't"],
        ["smiled", "frowned", "grinned", "smiling", "frowning", "grinning"],
        ["seemed", "appeared"],
        ["very", "many", "few", "lot"]]
    word_counts = wordcalc.get_word_array_include_word_groups(pretty_text, group_words)
    sorted_words = wordcalc.sort_word_array_with_groups(word_counts)
    pprint(sorted_words)
    wordgraph.create_pie_chart_word_groups(sorted_words)

main("bookofsecrets.docx")
