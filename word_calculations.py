
##### Ungrouped Word Counts #####

def get_word_counts_exclude_words(words, exclude_words):
    exclude_words = [x.lower() for x in exclude_words]
    return get_word_counts(words, [], exclude_words)


def get_word_counts_include_words(words, include_words):
    include_words = [x.lower() for x in include_words]
    return get_word_counts(words, include_words, [])


def get_word_counts(words, include_words=[], exclude_words=[]):
    word_counts = {}

    for word in words:
        if word != '' and word != ' ' and word != '"':
            if include_words:
                if word.lower() in include_words:
                    word_counts = add_word_to_count(word_counts, word.lower())
            elif exclude_words:
                if word.lower() not in exclude_words:
                    word_counts = add_word_to_count(word_counts, word.lower())
            else:
                word_counts = add_word_to_count(word_counts, word.lower())


    sorted_words = sort_word_counts(word_counts)
    return sorted_words


##### Grouped Word Counts #####

def get_word_counts_include_word_groups(words, include_words):
    word_groups = make_word_groups(include_words)
    for word in words:
        for group in word_groups:
            if word in group["words"]:
                group["count"] += 1

    sorted_words = sort_word_counts_with_groups(word_groups)
    return sorted_words


##### Private Functions #####

def add_word_to_count(word_counts, word):
    if word in word_counts:
        word_counts[word] += 1
    else:
        word_counts[word] = 1
    return word_counts


def make_word_groups(word_groups):
    groups = [];
    for word_group in word_groups:
        group = {};
        group["words"] = word_group
        group["count"] = 0
        groups.append(group)

    return groups


def sort_word_counts(word_counts):
    return sorted(word_counts.items(), key=lambda x:x[1])


def sort_word_counts_with_groups(word_groups):
    return sorted(word_groups, key=lambda group:group['count'])
