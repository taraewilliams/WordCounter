import docx
import unidecode
import re
import csv

ellipses_char = "\u2026"
left_quote = "\u201c"
right_quote = "\u201d"


def get_file_as_word_list(file_name: str):
    """
    Get all the words in the file as a word list.

    Parameters
    ----------
    file_name: str
        The file name to get the words from.

    Returns
    -------
    word_list: list[str]
        A list of all the words in the file.
    """
    # Get the text as a string from the docx file
    document = docx.Document(file_name)
    text = '\n'.join([paragraph.text for paragraph in document.paragraphs])
    text = text.replace('\n', ' ')
    text = text.replace(ellipses_char, ' ')

    # Split the text string into a list of words
    split_string = get_split_string()
    text_array = re.split(split_string, text)
    word_list = map(lambda x: unidecode.unidecode(x), text_array) 
    return word_list


def read_csv(file_name: str, grouped: bool = False):
    """
    Get all the words in the file as a word list.

    Parameters
    ----------
    file_name: str
        The file name to get the words from.
    grouped: bool
        Whether or not the words in the file are in groups.

    Returns
    -------
    words: list[str] (ungrouped) or list[list[str]] (grouped)
        A list of all the words in the file.
    """
    words = []

    with open(file_name) as data:
        reader = csv.reader(data, delimiter=",", quotechar="|")
        for row in reader:
            if (grouped): words.append(row)
            else: words = words + row

    return words


#####################################################
### Private Functions ###
#####################################################


def get_split_string():
    """
    Get the split string by which to split the text string into an array of words.

    Parameters
    ----------
    None

    Returns
    -------
    split_string: str
    """
    quotations = left_quote + "|" + right_quote
    periods = "\.| \.| \. |\. "
    spaces = " |  "
    commas = "\,| \,| \, |\, "
    question_marks = "\?| \?| \? |\? "
    exclamation_points = "\!| \!| \! |\! "
    other = "\;|\; |\:|\: |\.\.\."
    split_string = quotations + "|" + periods + "|" + spaces + "|" + commas + "|" + question_marks + "|" + exclamation_points + "|" + other
    return split_string
