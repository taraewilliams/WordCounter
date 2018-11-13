from pprint import pprint
from termcolor import colored

import word_calculations as wordcalc
import word_graphs as wordgraph
import read_files as readf
import os
import glob
import sys


def main():

    ### Get Word documents ###
    documents = get_documents('docs/full', 'docx')

    ### Choose a document ###
    file_name = get_file_name(documents)

    ### Choose a word counting option ###
    choose_option(file_name)


### Get documents for path and extension (docx, csv, etc.) ###
def get_documents(path, extension):
    os.chdir(path)
    documents = [i for i in glob.glob('*.{}'.format(extension))]
    return documents


### Get file name from terminal input ###
def get_file_name(documents):
    valid_input = False
    while (not valid_input):

        print(colored("\nChoose file number from the list: \n ", 'blue'))
        j = 1
        for document in documents:
            print("(",j,")",document)
            j += 1
        print("(", len(documents) + 1, ") Quit \n")

        file_num = input(colored("File number: \n ", 'blue'))

        try:
            file_index = int(file_num) - 1
            if (file_index == len(documents)):
                print("Quitting")
                sys.exit(0)
            elif (file_index < len(documents) and file_index >= 0):
                valid_input = True
            else:
                print(colored("\nInvalid file name", 'red'))
        except ValueError:
            print(colored('\nYou must enter a number.', 'red'))

    file_name = documents[file_index]
    return file_name


### Choose word counting option ###
def choose_option(file_name):
    valid_input = False
    while (not valid_input):

        print(colored("\nChoose Count Option:", 'blue'))

        try:
            option = int(input("\n (1) Character Names \n (2) Male/Female \n (3) Colors \n (4) All \n (5) Common Words \n (6) Quit \n"))
            if (option >= 1 and option <= 5):
                valid_input = True
                pretty_text = readf.get_file_as_word_array(file_name)

                ## Character Name Counts ###
                if(option == 1):
                    get_names(pretty_text)

                ### Male/Female Word Counts ###
                elif(option == 2):
                    get_words_counts_male_female(pretty_text)

                ### Color Counts ###
                elif(option == 3):
                    get_colors(pretty_text)

                ### Word Counts ###
                elif(option == 4):
                    get_word_counts(pretty_text)

                ### Common Word Counts ###
                elif(option == 5):
                    get_common_words(pretty_text)
            else:
                print("Quitting")
                sys.exit(0)
        except ValueError:
            print(colored('\nYou must enter a number.', 'red'))


### Character Name Counts ###
def get_names(pretty_text):

    documents = get_documents('../../docs/groups', 'csv')

    valid_input = False
    while (not valid_input):

        print(colored("\nChoose an option: \n ", 'blue'))

        try:
            option = int(input("\n (1) Choose existing CSV \n (2) Enter character names \n"))

            if (option == 1):
                file_name = get_file_name(documents)
                names = readf.read_csv(file_name, True)
                valid_input = True
            elif (option == 2):
                names = input_character_names()
                valid_input = True
            else:
                print("Quitting")
                sys.exit(0)

        except ValueError:
            print(colored('\nYou must enter a number.', 'red'))

    print_items_grouped(pretty_text, names)


### Write in your own character names in the terminal ###
def input_character_names():
    items = []

    print(colored("\nEnter names (related names on one row, separated by commas)", 'blue'))
    print(colored("\nExample: \"Jenna, Jenna's\" on one row, enter for new row, Q to quit \n", 'blue'))

    while (True):

        names = input()

        if (names == "Q" or names == "q"):
            print("Quitting")
            return items
        else:
            row = names.split(',')
            items.append(row)

    return items


### Male/Female Word Counts ###
def get_words_counts_male_female(pretty_text):
    female_words = readf.read_csv("female_words.csv")
    male_words = readf.read_csv("male_words.csv")
    group_words = [female_words, male_words]
    print_items_grouped(pretty_text, group_words)


### Color Word Counts ###
def get_colors(pretty_text):
    colors = readf.read_csv("colors.csv")
    sorted_colors = wordcalc.get_word_counts_include_words(pretty_text, colors)
    pprint(sorted_colors)

    labels = []
    for sorted_color in sorted_colors:
        labels.append(sorted_color[0])

    wordgraph.create_pie_chart_words(sorted_colors, labels)


### Complete Word Counts ###
def get_word_counts(pretty_text):
    word_counts = wordcalc.get_word_counts(pretty_text)
    pprint(word_counts)


### Common Word Counts ###
def get_common_words(pretty_text):
    common_words = readf.read_csv("common_words.csv")
    sorted_words = wordcalc.get_word_counts_include_words(pretty_text, common_words)
    pprint(sorted_words)


### Print Grouped Items with Pie Chart ###
def print_items_grouped(pretty_text, items):
    sorted_items = wordcalc.get_word_counts_include_word_groups(pretty_text, items)
    pprint(sorted_items)
    wordgraph.create_pie_chart_word_groups(sorted_items)


main()
