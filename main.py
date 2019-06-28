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


### Choose word counting option ###
def choose_option(file_name):

    valid_input = False
    while (not valid_input):

        print(colored("\nChoose Count Option:", 'blue'))
        options = ['All', 'Character Names', 'Male/Female', 'Colors', 'Common Words', 'Custom Words', 'All Without Common Words']
        print_options(options)

        try:
            option = int(input(colored("Count option: \n ", 'blue')))
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


#####################################################
### Word Count Options ###
#####################################################


### Option 1 ###
### Complete Word Counts ###
def get_word_counts(pretty_text):
    get_word_counts_ungrouped(pretty_text)


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
                get_word_counts_grouped(pretty_text, names, True)
                valid_input = True
            elif (option == 2):
                get_custom_words(pretty_text)
                valid_input = True
            else:
                print("Quitting")
                sys.exit(0)

        except ValueError:
            print(colored('\nYou must enter a number.', 'red'))


### Option 3 ###
### Male/Female Word Counts ###
def get_words_counts_male_female(pretty_text):
    female_words = readf.read_csv(csv_dir + "/female_words.csv")
    male_words = readf.read_csv(csv_dir + "/male_words.csv")
    group_words = [female_words, male_words]
    get_word_counts_grouped(pretty_text, group_words, True)


### Option 4 ###
### Color Word Counts ###
def get_colors(pretty_text):
    sorted_colors = get_word_counts_ungrouped(pretty_text, "/colors.csv", True)
    labels = []
    for sorted_color in sorted_colors:
        labels.append(sorted_color[0])
    wordgraph.create_pie_chart_words(sorted_colors, labels)


### Option 5 ###
### Common Word Counts ###
def get_common_words(pretty_text):
    get_word_counts_ungrouped(pretty_text, "/common_words.csv", True)


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
        get_word_counts_grouped(pretty_text, custom_words)
    else:
        sorted_words = wordcalc.get_word_counts(pretty_text, custom_words, True)
        pprint(sorted_words)


### Option 7 ###
### All Word Counts without Common Words ###
def get_uncommon_words(pretty_text):
    get_word_counts_ungrouped(pretty_text, "/common_words.csv")


#####################################################
### Other Functions ###
#####################################################


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
        print_options(documents)

        try:
            file_index = int(input(colored("File number: \n ", 'blue'))) - 1
            if (file_index >= len(documents) or file_index < 0):
                print("Quitting")
                sys.exit(0)
            else:
                valid_input = True
        except ValueError:
            print(colored('\nYou must enter a number.', 'red'))

    file_name = documents[file_index]
    return file_name


### Print Ungrouped Word Counts ###
def get_word_counts_ungrouped(pretty_text, csv_name=None, include_words=False):
    if (csv_name is not None):
        input_words = readf.read_csv(csv_dir + csv_name)
    else:
        input_words = []
    sorted_words = wordcalc.get_word_counts(pretty_text, input_words, include_words)
    pprint(sorted_words)
    print(colored('\n' + str(len(sorted_words)) + ' unique words \n', 'green'))
    return sorted_words


### Print Grouped Word Counts with Pie Chart ###
def get_word_counts_grouped(pretty_text, items, chart=False):
    sorted_words = wordcalc.get_word_counts_word_groups(pretty_text, items)
    pprint(sorted_words)
    if (chart):
        wordgraph.create_pie_chart_word_groups(sorted_words)

    return sorted_words


### Write in custom words in the terminal ###
def input_custom_words(grouped=False):
    words = []

    if (grouped):
        print(colored("\nEnter words (group of related words on one row, separated by commas)", 'blue'))
        print(colored("\nExample: \"mother, father, parents\" on one row, enter for new row, Q to quit \n", 'blue'))

        while (True):

            grouped_string = input()

            if (grouped_string == "Q" or grouped_string == "q"):
                print("Quitting")
                return words
            else:
                row = grouped_string.split(',')
                words.append(grouped_string)
    else:
        print(colored("\nEnter words (separated by commas), Q on separate line to quit \n", 'blue'))

        while (True):

            ungrouped_string = input()

            if (ungrouped_string == "Q" or ungrouped_string == "q"):
                print("Quitting")
                return words
            else:
                row = ungrouped_string.split(',')
                words = words + row

    return words


### Print Options For a List of Options ###
def print_options(options):
    for i in range(len(options)):
        print("(",i+1,")",options[i])
    print("(", len(options) + 1, ") Quit \n")


#####################################################
### Main Function Call ###
#####################################################


main()
