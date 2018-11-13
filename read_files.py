import docx
import unidecode
import re
import csv

def get_file_as_word_array(file_name):
    document = docx.Document(file_name)
    text = '\n'.join([paragraph.text for paragraph in document.paragraphs])
    text = text.replace('\n', ' ')
    text = text.replace("\u2026", ' ')

    split_string = get_split_string()
    text_array = re.split(split_string, text)

    pretty_text = []
    for text_item in text_array:
        pretty_text.append(unidecode.unidecode(text_item))

    return pretty_text


def read_csv(file_name, grouped = False):
    items = []

    with open(file_name) as data:
        reader = csv.reader(data, delimiter=",", quotechar="|")
        for row in reader:
            if (grouped):
                items.append(row)
            else:
                items = items + row

    return items


##### Private Functions #####

def get_split_string():
    quotations = "\u201c|\u201d"
    periods = "\.| \.| \. |\. "
    spaces = " |  "
    commas = "\,| \,| \, |\, "
    question_marks = "\?| \?| \? |\? "
    exclamation_points = "\!| \!| \! |\! "
    other = "\;|\; |\:|\: |\.\.\."
    split_string = quotations + "|" + periods + "|" + spaces + "|" + commas + "|" + question_marks + "|" + exclamation_points + "|" + other
    return split_string
