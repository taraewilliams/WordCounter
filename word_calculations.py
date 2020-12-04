
def get_word_counts(words: list, input_words: list = [], include_words: bool = False):
    """ 
    Get word counts  

    Parameters
    ----------
    words: list[str]
        The full word list.
    input_words: list[str]
        Words to include or exclude from the word counts.
    include_words: bool
        True for include words, False for exclude words

    Returns
    -------
    sorted_words: list[[str, int]]
  
    """
    # Convert input words to lowercase
    if input_words:
        input_words = [word.lower() for word in input_words]

    word_counts = {}
    for word in words:
        if should_add_word_to_word_count(word, input_words, include_words):
            word_counts = add_word_to_count(word_counts, word.lower())

    sorted_words = sort_word_counts(word_counts)
    return sorted_words


def get_word_counts_word_groups(words: list, include_words: list):
    """ 
    Get word counts for word groups. 

    Parameters
    ----------
    words: list[str]
        The full word list.
    include_words: list[list[str]]
        The word groups to count.

    Returns
    -------
    sorted_words: list[ { words: list[str], count: int } ]
  
    """
    word_groups = make_word_group_counts(include_words)

    for word in words:
        for group in word_groups:
            if word in group["words"]:
                group["count"] += 1

    sorted_words = sort_word_counts_with_groups(word_groups)
    return sorted_words


#####################################################
### Private Functions ###
#####################################################


def should_add_word_to_word_count(word: str, input_words: list = [], include_words: bool = False):
    """ 
    Check if a word should be added to the word count. 

    Parameters
    ----------
    word: str
        The word.
    input_words: list[str]
        Words to include or exclude from the word counts.
    include_words: bool
        True for include words, False for exclude words

    Returns
    -------
    bool: Whether or not a word should be added to the word count.
    """
    # Check that the word is not empty
    if word_not_empty(word):
        # If there are input words, add words if they are include words
        add_input_include_words = (input_words and include_words and (word.lower() in input_words))
        # If there are input words, do not add words if they are exclude words
        add_input_exclude_words = (input_words and (not include_words) and (word.lower() not in input_words))
        # If there are no input words count all words
        add_all_words = (not input_words)

        return add_input_include_words or add_input_exclude_words or add_all_words
    else:
        return False


def add_word_to_count(word_counts: dict, word: str):
    """ 
    Add a word to the total word counts.

    Parameters
    ----------
    word_counts: dict
        The current word counts.
    word: str
        The word to add to the counts.

    Returns
    -------
    word_counts: dict
        The current word counts with the added word.
    """
    if word in word_counts:
        word_counts[word] += 1
    else:
        word_counts[word] = 1
    return word_counts


def sort_word_counts(word_counts: dict):
    """
    Sort the word counts by the least to most frequently-occurring words.

    Parameters
    ----------
    word_counts: dict
        The word counts.

    Returns
    -------
    Sorted word counts: list[[str, int]]
        The sorted word counts.
    """
    return sorted(word_counts.items(), key=lambda x:x[1])


def make_word_group_counts(word_groups: list):
    """
    Make word group counts for word groups.

    Parameters
    ----------
    word_groups: list[list[str]]

    Returns
    -------
    groups: list of dict { words:list[str], count:int }
        The word groups
    """
    groups = []
    for word_group in word_groups:
        group = { "words":word_group, "count":0 }
        groups.append(group)

    return groups


def sort_word_counts_with_groups(word_groups: list):
    """
    Sort word counts by groups by the least to most frequently-occurring words.

    Parameters
    ----------
    word_groups: list of dict { words:list[str], count:int }

    Returns
    -------
    Sorted word group counts: list of dict { words:list[str], count:int }
    """
    return sorted(word_groups, key=lambda group:group['count'])


def word_not_empty(word: str):
    """
    Check that a word is not empty.

    Parameters
    ----------
    word: str
        The word to check.

    Returns
    -------
    if a word is empty: bool
    """
    return (word != '' and word != ' ' and word != '"')
