def get_word_array_exclude_words(words, exclude_words):
    word_counts = {}
    for word in words:
        if word != "" and word != '' and word != '"' and word.lower() not in exclude_words:
            word_counts = add_word_to_array(word_counts, word.lower())
    return word_counts


def get_word_array_include_words(words, include_words):
    word_counts = {}
    for word in words:
        if word.lower() in include_words:
            word_counts = add_word_to_array(word_counts, word.lower())
    return word_counts


def get_word_array_include_word_groups(words, include_words):
    word_groups = make_word_groups(include_words)
    for word in words:
        for group in word_groups:
            if word in group["words"]:
                group["count"] += 1
    return word_groups


def make_word_groups(word_groups):
    groups = [];
    for word_group in word_groups:
        group = {};
        group["words"] = word_group
        group["count"] = 0
        groups.append(group)

    return groups


def get_word_array(words):
    word_counts = {}
    for word in words:
        if word != '' and word != ' ':
            word_counts = add_word_to_array(word_counts, word.lower())
    return word_counts


def add_word_to_array(word_counts, word):
    if word in word_counts:
        word_counts[word] += 1
    else:
        word_counts[word] = 1
    return word_counts


def sort_word_array(word_counts):
    return sorted(word_counts.items(), key=lambda x:x[1])


def sort_word_array_with_groups(word_groups):
    return sorted(word_groups, key=lambda group:group['count'])
