"""
Lab 1
A concordance extraction
"""


def tokenize(text: str) -> list:
    """
    Splits sentences into tokens, converts the tokens into lowercase, removes punctuation
    :param text: the initial text
    :return: a list of lowercased tokens without punctuation
    e.g. text = 'The weather is sunny, the man is happy.'
    --> ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy']
    """
    tokens = []
    if isinstance(text, str):
        text += ' '
        text_clean = ''
        for symbol in text:
            if symbol.isalpha() or symbol == ' ':
                text_clean += symbol
            else:
                symbol_index = text.index(symbol)
                if text[symbol_index + 1] == ' ':
                    text_clean += ' '
                elif text[symbol_index + 1].isalpha():
                    text_clean += symbol
        text_lower = text_clean.lower()
        tokens = text_lower.split()

    return tokens


def remove_stop_words(tokens: list, stop_words: list) -> list:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    e.g. tokens = ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy']
    stop_words = ['the', 'is']
    --> ['weather', 'sunny', 'man', 'happy']
    """
    tokens_clean = []
    if isinstance(tokens, list):
        if isinstance(stop_words, list):
            for token in tokens:
                if token not in stop_words:
                    tokens_clean.append(token)
                else:
                    continue
            return tokens_clean
        else:
            return tokens

    return tokens_clean


def calculate_frequencies(tokens: list) -> dict:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens without stop words
    :return: a dictionary with frequencies
    e.g. tokens = ['weather', 'sunny', 'man', 'happy']
    --> {'weather': 1, 'sunny': 1, 'man': 1, 'happy': 1}
    """
    freq_dict = {}
    if isinstance(tokens, list):
        for token in tokens:
            freq_dict[token] = tokens.count(token)

    return freq_dict


def get_top_n_words(freq_dict: dict, top_n: int) -> list:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words to return
    :return: a list of the most common words
    e.g. tokens = ['weather', 'sunny', 'man', 'happy', 'and', 'dog', 'happy']
    top_n = 1
    --> ['happy']
    """
    top_n_words = []
    if isinstance(freq_dict, dict) and isinstance(top_n, int):
        if top_n <= len(freq_dict):
            freq_list = list(freq_dict.items())
            freq_list.sort(key=lambda num: num[1], reverse=True)
            freq_dict_sorted = dict(freq_list)
            top_words = []
            for frequency, word in enumerate(freq_dict_sorted):
                top_words.append(word)
            top_n_words = top_words[:top_n]

    return top_n_words


def get_concordance(tokens: list, word: str, left_context_size: int, right_context_size: int) -> list:
    """
    Gets a concordance of a word
    A concordance is a listing of each occurrence of a word in a text,
    presented with the words surrounding it
    :param tokens: a list of tokens
    :param word: a word-base for a concordance
    :param left_context_size: the number of words in the left context
    :param right_context_size: the number of words in the right context
    :return: a concordance
    e.g. tokens = ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy',
                    'the', 'dog', 'is', 'happy', 'but', 'the', 'cat', 'is', 'sad']
    word = 'happy'
    left_context_size = 2
    right_context_size = 3
    --> [['man', 'is', 'happy', 'the', 'dog', 'is'], ['dog', 'is', 'happy', 'but', 'the', 'cat']]
    """
    concordance = []
    if isinstance(tokens, list) and isinstance(word, str) and isinstance(left_context_size, int) and isinstance(right_context_size, int):
        word_indexes = []
        tokens_copy = tokens.copy()
        for token in tokens_copy:
            if token == word:
                token_index = tokens_copy.index(token)
                word_indexes.append(token_index)
                tokens_copy.pop(token_index)
                tokens_copy.insert(token_index, '?')
        left_limit = word_indexes[-1]
        right_limit = len(tokens)
        right_limit - int(word_indexes[-1])
        left_subconcordance = []
        right_subconcordance = []
        if left_context_size >= 1 and left_context_size <= left_limit:
            for index in word_indexes:
                left_example = tokens[index - left_context_size:index]
                left_example.append(word)
                left_subconcordance.append(left_example)
        if right_context_size >= 1 and right_context_size <= right_limit:
            for index in word_indexes:
                right_example = tokens[index + 1:index + right_context_size + 1]
                right_example.insert(0, word)
                right_subconcordance.append(right_example)
        if len(left_subconcordance) == 0:
            concordance = right_subconcordance
        elif len(right_subconcordance) == 0:
            concordance = left_subconcordance
        elif len(left_subconcordance) == 0 and len(right_subconcordance) == 0:
            pass
        else:
            for index in word_indexes:
                example = tokens[index - left_context_size:index]  # left context
                example.append(word)
                example += tokens[index + 1:index + right_context_size + 1]  # right context
                concordance.append(example)

    return concordance


def get_adjacent_words(tokens: list, word: str, left_n: int, right_n: int) -> list:
    """
    Gets adjacent words from the left and right context
    :param tokens: a list of tokens
    :param word: a word-base for the search
    :param left_n: the distance between a word and an adjacent one in the left context
    :param right_n: the distance between a word and an adjacent one in the right context
    :return: a list of adjacent words
    e.g. tokens = ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy',
                    'the', 'dog', 'is', 'happy', 'but', 'the', 'cat', 'is', 'sad']
    word = 'happy'
    left_n = 2
    right_n = 3
    --> [['man', 'is'], ['dog, 'cat']]
    """
    adjacent_words = []
    if isinstance(tokens, list) and isinstance(word, str) and isinstance(left_n, int) and isinstance(right_n, int):
        concordance = get_concordance(tokens, word, left_n, right_n)
        if len(concordance) != 0:
            for example in concordance:
                if example[0] == word:
                    right_adjacent_word = [example[right_n]]
                    adjacent_words.append(right_adjacent_word)
                elif example[-1] == word:
                    left_adjacent_word = [example[0]]
                    adjacent_words.append(left_adjacent_word)
                else:
                    right_and_left_adjacent_words = [example[0], example[-1]]
                    adjacent_words.append(right_and_left_adjacent_words)

    return adjacent_words


def read_from_file(path_to_file: str) -> str:
    """
    Opens the file and reads its content
    :return: the initial text in string format
    """
    with open(path_to_file, 'r', encoding='utf-8') as fs:
        data = fs.read()

    return data


def write_to_file(path_to_file: str, content: list):
    """
    Writes the result in a file
    """
    pass


def sort_concordance(tokens: list, word: str, left_context_size: int, right_context_size: int, left_sort: bool) -> list:
    """
    Gets a concordance of a word and sorts it by either left or right context
    :param tokens: a list of tokens
    :param word: a word-base for a concordance
    :param left_context_size: the number of words in the left context
    :param right_context_size: the number of words in the right context
    :param left_sort: if True, sort by the left context, False – by the right context
    :return: a concordance
    e.g. tokens = ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy',
                    'the', 'dog', 'is', 'happy', 'but', 'the', 'cat', 'is', 'sad']
    word = 'happy'
    left_context_size = 2
    right_context_size = 3
    left_sort = True
    --> [['dog', 'is', 'happy', 'but', 'the', 'cat'], ['man', 'is', 'happy', 'the', 'dog', 'is']]
    """
    pass