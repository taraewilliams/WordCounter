
##### Ungrouped Word Counts #####

def get_word_counts(words, input_words=[], include_words=False):

    # Convert input words to lowercase
    if input_words:
        input_words = [word.lower() for word in input_words]

    word_counts = {}

    for word in words:
        # Check that the word is not empty
        if word_not_empty(word):

            # Check if there are input words; if not, count all words
            if input_words:
                # Add words if they are include words
                if include_words:
                    if word.lower() in input_words:
                        word_counts = add_word_to_count(word_counts, word.lower())
                # Do not add words if they are exclude words
                else:
                    if word.lower() not in input_words:
                        word_counts = add_word_to_count(word_counts, word.lower())
            else:
                word_counts = add_word_to_count(word_counts, word.lower())

    sorted_words = sort_word_counts(word_counts)
    return sorted_words


def add_word_to_count(word_counts, word):
    if word in word_counts:
        word_counts[word] += 1
    else:
        word_counts[word] = 1
    return word_counts


def sort_word_counts(word_counts):
    return sorted(word_counts.items(), key=lambda x:x[1])


##### Grouped Word Counts #####

def get_word_counts_word_groups(words, include_words):
    word_groups = make_word_groups(include_words)
    for word in words:
        for group in word_groups:
            if word in group["words"]:
                group["count"] += 1

    sorted_words = sort_word_counts_with_groups(word_groups)
    return sorted_words


def make_word_groups(word_groups):
    groups = [];
    for word_group in word_groups:
        group = {};
        group["words"] = word_group
        group["count"] = 0
        groups.append(group)

    return groups


def sort_word_counts_with_groups(word_groups):
    return sorted(word_groups, key=lambda group:group['count'])


##### Other Functions #####

def word_not_empty(word):
    return (word != '' and word != ' ' and word != '"')
