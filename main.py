from pprint import pprint
from termcolor import colored

import word_calculations as wordcalc
import word_graphs as wordgraph
import read_files as readf
import os
import glob
import sys


docx_dir = 'docs/full'
csv_dir = 'docs/groups'

def main():

    ### Get Word documents ###
    documents = get_documents(docx_dir, 'docx')

    ### Choose a document ###
    file_name = get_file_name(documents)

    ### Choose a word counting option ###
    choose_option(file_name)


### Get documents for path and extension (docx, csv, etc.) ###
def get_documents(path, extension):
    owd = os.getcwd()
    os.chdir(path)
    documents = [i for i in glob.glob('*.{}'.format(extension))]
    os.chdir(owd)
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
            option = int(input("\n (1) All \n (2) Character Names \n (3) Male/Female \n (4) Colors \n (5) Common Words \n (6) Custom Words \n (7) All without Common Words \n (8) Quit \n"))
            if (option >= 1 and option <= 7):
                valid_input = True
                pretty_text = readf.get_file_as_word_array(docx_dir + "/" + file_name)

                ### Word Counts ###
                if(option == 1):
                    get_word_counts(pretty_text)

                ## Character Name Counts ###
                elif(option == 2):
                    get_names(pretty_text)

                ### Male/Female Word Counts ###
                elif(option == 3):
                    get_words_counts_male_female(pretty_text)

                ### Color Counts ###
                elif(option == 4):
                    get_colors(pretty_text)

                ### Common Word Counts ###
                elif(option == 5):
                    get_common_words(pretty_text)

                ### Custom Word Counts ###
                elif(option == 6):
                    get_custom_words(pretty_text)

                ### Word Counts without Common Words ###
                elif(option == 7):
                    get_uncommon_words(pretty_text)
            else:
                print("Quitting")
                sys.exit(0)
        except ValueError:
            print(colored('\nYou must enter a number.', 'red'))


### Option 1 ###
### Complete Word Counts ###
def get_word_counts(pretty_text):
    word_counts = wordcalc.get_word_counts(pretty_text)
    pprint(word_counts)


### Option 2 ###
### Character Name Counts ###
def get_names(pretty_text):

    documents = get_documents(csv_dir, 'csv')

    valid_input = False
    while (not valid_input):

        print(colored("\nChoose an option: \n ", 'blue'))

        try:
            option = int(input("\n (1) Choose existing CSV \n (2) Enter character names \n"))

            if (option == 1):
                file_name = get_file_name(documents)
                names = readf.read_csv(csv_dir + "/" + file_name, True)
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


### Option 3 ###
### Male/Female Word Counts ###
def get_words_counts_male_female(pretty_text):
    female_words = readf.read_csv(csv_dir + "/female_words.csv")
    male_words = readf.read_csv(csv_dir + "/male_words.csv")
    group_words = [female_words, male_words]
    print_items_grouped(pretty_text, group_words)


### Option 4 ###
### Color Word Counts ###
def get_colors(pretty_text):
    colors = readf.read_csv(csv_dir + "/colors.csv")
    sorted_colors = wordcalc.get_word_counts_include_words(pretty_text, colors)
    pprint(sorted_colors)

    labels = []
    for sorted_color in sorted_colors:
        labels.append(sorted_color[0])

    wordgraph.create_pie_chart_words(sorted_colors, labels)


### Option 5 ###
### Common Word Counts ###
def get_common_words(pretty_text):
    common_words = readf.read_csv(csv_dir + "/common_words.csv")
    sorted_words = wordcalc.get_word_counts_include_words(pretty_text, common_words)
    pprint(sorted_words)


### Option 6 ###
### Custom Word Counts ###
def get_custom_words(pretty_text):

    grouped = True
    valid_input = False
    while (not valid_input):

        print(colored("\nChoose an option: \n ", 'blue'))

        try:
            option = int(input("\n (1) Enter ungrouped words \n (2) Enter grouped words \n"))

            if (option == 1):
                grouped = False
                custom_words = input_custom_words(grouped)
                valid_input = True
            elif (option == 2):
                custom_words = input_custom_words(grouped)
                valid_input = True
            else:
                print("Quitting")
                sys.exit(0)

        except ValueError:
            print(colored('\nYou must enter a number.', 'red'))

    if (grouped):
        print_items_grouped(pretty_text, custom_words)
    else:
        sorted_words = wordcalc.get_word_counts_include_words(pretty_text, custom_words)
        pprint(sorted_words)


### Write in custom words in the terminal ###
def input_custom_words(grouped):
    items = []

    if (grouped):
        print(colored("\nEnter words (group of words on one row, separated by commas)", 'blue'))
        print(colored("\nExample: \"mother, father, parents\" on one row, enter for new row, Q to quit \n", 'blue'))

        while (True):

            names = input()

            if (names == "Q" or names == "q"):
                print("Quitting")
                return items
            else:
                row = names.split(',')
                items.append(row)
    else:
        print(colored("\nEnter words (separated by commas), Q on separate line to quit \n", 'blue'))

        while (True):

            names = input()

            if (names == "Q" or names == "q"):
                print("Quitting")
                return items
            else:
                row = names.split(',')
                items = items + row

    return items


### Option 7 ###
### All Word Counts without Common Words ###
def get_uncommon_words(pretty_text):
    common_words = readf.read_csv(csv_dir + "/common_words.csv")
    sorted_words = wordcalc.get_word_counts_exclude_words(pretty_text, common_words)
    pprint(sorted_words)


### Print Grouped Items with Pie Chart ###
def print_items_grouped(pretty_text, items, chart=False):
    sorted_items = wordcalc.get_word_counts_include_word_groups(pretty_text, items)
    pprint(sorted_items)
    if (chart):
        wordgraph.create_pie_chart_word_groups(sorted_items)


main()
