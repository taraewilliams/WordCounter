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
options = ['All', 'Character Names', 'Male/Female', 'Colors', 'Common Words', 'Custom Words', 'All Without Common Words']

def main():
    ### Get Word document file names ###
    file_names = get_file_names(docx_dir, 'docx')
    ### Choose a document ###
    file_name = select_file_name_from_file_list(file_names)
    ### Choose a word counting option ###
    choose_option(file_name)


def choose_option(file_name: str):
    """
    Choose the option for word counting.

    Parameters
    ----------
    file_name: str
        The file name to get the words to be counted from.

    Returns
    -------
    No return value
    """
    valid_input = False
    while (not valid_input):
        print(colored("\nOptions:", 'blue'))
        print_options(options)

        try:
            option = int(input(colored("Enter selected option: \n", 'blue')))
            if (option >= 1 and option <= len(options)):
                valid_input = True
                word_list = readf.get_file_as_word_list(docx_dir + "/" + file_name)

                ### All Word Counts ###
                if(option == 1): get_word_counts(word_list)
                ## Character Name Counts ###
                elif(option == 2): get_word_counts_names(word_list)
                ### Male/Female Word Counts ###
                elif(option == 3): get_word_counts_male_female(word_list)
                ### Color Counts ###
                elif(option == 4): get_word_counts_colors(word_list)
                ### Common Word Counts ###
                elif(option == 5): get_word_counts_common(word_list)
                ### Custom Word Counts ###
                elif(option == 6): get_word_counts_custom(word_list)
                ### Word Counts without Common Words ###
                elif(option == 7): get_word_counts_uncommon(word_list)
            else:
                quit_selection()
        except ValueError:
            print(colored('\nYou must enter a number.', 'red'))


#####################################################
### Word Count Options ###
#####################################################


def get_word_counts(word_list: list):
    """
    Option 1: Get complete word counts. Prints all the words with their counts.

    Parameters
    ----------
    word_list: list[str]
        The list of words to count.

    Returns
    -------
    No return value
    """
    get_word_counts_ungrouped(word_list)


def get_word_counts_names(word_list: list):
    """
    Option 2: Get character name counts. Prints the character names with their counts.
    This may or may not include a pie chart.

    Parameters
    ----------
    word_list: list[str]
        The list of words to count.

    Returns
    -------
    No return value
    """
    valid_input = False
    while (not valid_input):
        print(colored("\nChoose an option: \n ", 'blue'))
        try:
            option = int(input("\n (1) Choose existing CSV \n (2) Enter character name(s) \n (3) Quit \n"))
            ### Choose existing CSV file for character names ###
            if (option == 1):
                file_names = get_file_names(csv_dir, 'csv')
                file_name = select_file_name_from_file_list(file_names)
                names = readf.read_csv(csv_dir + "/" + file_name, True)
                get_word_counts_grouped(word_list, names, True)
                valid_input = True
            ### Enter new character names ###
            elif (option == 2):
                get_word_counts_custom(word_list)
                valid_input = True
            else: quit_selection()

        except ValueError:
            print(colored('\nYou must enter a number.', 'red'))


def get_word_counts_male_female(word_list: list):
    """
    Option 3: Get word counts for male/female words. Prints the male/female words with their counts.
    This includes a pie chart.

    Parameters
    ----------
    word_list: list[str]
        The list of words to count.

    Returns
    -------
    No return value
    """
    female_words = readf.read_csv(csv_dir + "/female_words.csv")
    male_words = readf.read_csv(csv_dir + "/male_words.csv")
    group_words = [female_words, male_words]
    get_word_counts_grouped(word_list, group_words, True)


def get_word_counts_colors(word_list: list):
    """
    Option 4: Get word counts for colors. Prints the colors with their counts.
    This includes a pie chart.

    Parameters
    ----------
    word_list: list[str]
        The list of words to count.

    Returns
    -------
    No return value
    """
    sorted_colors = get_word_counts_ungrouped(word_list, "/colors.csv", True)
    labels = []
    for sorted_color in sorted_colors:
        labels.append(sorted_color[0])
    wordgraph.create_pie_chart_words(sorted_colors, labels)


def get_word_counts_common(word_list: list):
    """
    Option 5: Get common word counts. Prints the common words with their counts.

    Parameters
    ----------
    word_list: list[str]
        The list of words to count.

    Returns
    -------
    No return value
    """
    get_word_counts_ungrouped(word_list, "/common_words.csv", True)


def get_word_counts_custom(word_list: list):
    """
    Option 6: Get custom word counts. Prints the custom words with their counts.

    Parameters
    ----------
    word_list: list[str]
        The list of words to count.

    Returns
    -------
    No return value
    """
    grouped = True
    valid_input = False
    while (not valid_input):

        print(colored("\nChoose an option: \n ", 'blue'))
        try:
            option = int(input("\n (1) Enter ungrouped words \n (2) Enter grouped words \n (3) Quit \n"))
            ### Enter words ###
            if (option == 1 or option == 2):
                grouped = False if (option == 1) else True
                custom_words = input_custom_words(grouped)
                valid_input = True
            else: quit_selection()
        except ValueError:
            print(colored('\nYou must enter a number.', 'red'))

    if (grouped):
        get_word_counts_grouped(word_list, custom_words)
    else:
        sorted_words = wordcalc.get_word_counts(word_list, custom_words, True)
        pprint(sorted_words)
        print(colored('\n' + str(len(sorted_words)) + ' unique words \n', 'green'))


def get_word_counts_uncommon(word_list: list):
    """
    Option 7: Get all word counts without common words. Prints the words with their counts.

    Parameters
    ----------
    word_list: list[str]
        The list of words to count.

    Returns
    -------
    No return value
    """
    get_word_counts_ungrouped(word_list, "/common_words.csv")


#####################################################
### Other Functions ###
#####################################################


def get_file_names(path: str, extension: str):
    """
    Get file names for path and extension (docx, csv, etc.)

    Parameters
    ----------
    path: str
        The path to the folder with the files.
    extension: str
        The file extension of the file names to get.

    Returns
    -------
    file_names: list[str]
        The list of file names.
    """
    owd = os.getcwd()
    os.chdir(path)
    file_names = [i for i in glob.glob('*.{}'.format(extension))]
    os.chdir(owd)
    return file_names


def select_file_name_from_file_list(file_names: list):
    """
    Get file name from file list terminal input.

    Parameters
    ----------
    file_names: list[str]
        A list of the file names to choose from

    Returns
    -------
    file_name: str
        The selected file name
    """
    valid_input = False
    while (not valid_input):
        print(colored("\nChoose file number from the list: \n ", 'blue'))
        print_options(file_names)

        try:
            file_index = int(input(colored("Enter file number: \n ", 'blue'))) - 1
            if (file_index >= len(file_names) or file_index < 0): quit_selection()
            else: valid_input = True
        except ValueError:
            print(colored('\nYou must enter a number.', 'red'))

    file_name = file_names[file_index]
    return file_name


def print_options(options: list):
    """
    Print options for a list of options.

    Parameters
    ----------
    options: list[str]
        The options to print.
    
    Returns
    -------
    No return value
    """
    for i in range(len(options)):
        print("(",i+1,")",options[i])
    print("(", len(options) + 1, ") Quit \n")


def quit_selection():
    """
    Quit the selection and exit the program.
    """
    print(colored('\nQuitting', 'red'))
    sys.exit(0)


def get_word_counts_ungrouped(word_list: list, csv_name: str = None, include_words: bool = False):
    """
    Get word counts of ungrouped words. Prints the ungrouped words with their counts.

    Parameters
    ----------
    word_list: list of type string
        The list of words to count.
    csv_name: str, optional
        The name of the CSV file with include/exclude words.
    include_words: bool, optional
        If true, include only the words in the CSV file. 
        Otherwise, exclude the words in the CSV file from all words.
    
    Returns
    -------
    sorted_words: list[[str, int]]
        The list of sorted words.
    """
    input_words = []
    if (csv_name is not None):
        input_words = readf.read_csv(csv_dir + csv_name)

    sorted_words = wordcalc.get_word_counts(word_list, input_words, include_words)
    pprint(sorted_words)
    print(colored('\n' + str(len(sorted_words)) + ' unique words \n', 'green'))
    return sorted_words


def get_word_counts_grouped(word_list: list, grouped_words: list, chart: bool = False):
    """
    Get word counts of grouped words. Prints the grouped words with their counts.
    It also has the option to display a pie chart.

    Parameters
    ----------
    word_list: list[str]
        The list of words to count.
    grouped_words: list[list[str]]
        The list of grouped word lists.
    chart: bool (optional)
        Whether or not to display a pie chart.
    
    Returns
    -------
    sorted_words: list
        The list of sorted words.
    """
    sorted_words = wordcalc.get_word_counts_word_groups(word_list, grouped_words)
    pprint(sorted_words)
    if (chart):
        wordgraph.create_pie_chart_words(sorted_words, [], True)
    
    return sorted_words


def input_custom_words(grouped: bool = False):
    """
    Write in custom word lists in the terminal.

    Parameters
    ----------
    grouped: bool (optional)
        Whether or not the list of custom words should be grouped.
    
    Returns
    -------
    words: list
        A list[str] (ungrouped) OR list[list[str]] (grouped)
    """
    words = []

    if (grouped):
        print(colored("\nEnter words (group of related words on one row, separated by commas)", 'blue'))
        print(colored("\nExample: \"mother, father, parents\" on one row, enter for new row, Q on separate line to quit \n", 'blue'))
    else:
        print(colored("\nEnter words (separated by commas), Q on separate line to quit \n", 'blue'))

    while (True):
        input_string = input()
        if (input_string == "Q" or input_string == "q"):
            print("Quitting")
            return words
        else:
            row = input_string.split(',')
            if (grouped): words.append(row)
            else: words = words + row

    return words


#####################################################
### Main Function Call ###
#####################################################


main()
