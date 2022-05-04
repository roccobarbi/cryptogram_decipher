from crypto_tools import data
from crypto_tools.stats.letter_frequency import LetterFrequency
from crypto_tools.stats.ngram_frequency import NgramFrequency


DIFF_AMPLIFICATION = 15


def fitness_aristocrat(text, language):
    lf = LetterFrequency(text).calculate()
    bf = NgramFrequency(text=text, nvalue=2).calculate()
    short_words_weights = {
        1: 3,
        2: 2,
        3: 1,
        4: 1,
        5: 2,
        6: 1,
        7: 1,
        8: 1,
        9: 1,
        10: 1,
        11: 1,
        12: 1,
        13: 1,
        14: 1,
        15: 1,
        16: 1
    }
    fitness = 0
    for letter in lf:
        if str(letter).isalpha():
            fitness += abs(data.letter_frequency_by_language[language][letter] - lf[letter]) * DIFF_AMPLIFICATION
    for bigram in bf:
        if bigram not in data.bigram_frequency_by_language[language].keys():
            fitness += bf[bigram] * DIFF_AMPLIFICATION
        else:
            fitness += abs(data.bigram_frequency_by_language[language][bigram] - bf[bigram]) * DIFF_AMPLIFICATION
    words = text.split()
    for word in words:
        if len(word) < 14 and word in data.frequent_short_words_by_language[language][len(word)]:
            fitness -= 0.5 * short_words_weights[len(word)]
    return fitness


def fitness_patristocrat(text, language):
    lf = LetterFrequency(text).calculate()
    bf = NgramFrequency(text=text, nvalue=2).calculate()
    fitness = 0
    for letter in lf:
        if str(letter).isalpha():
            fitness += abs(data.letter_frequency_by_language[language][letter] - lf[letter]) * DIFF_AMPLIFICATION
    for bigram in bf:
        if bigram not in data.bigram_frequency_by_language[language].keys():
            fitness += bf[bigram] * DIFF_AMPLIFICATION
        else:
            fitness += abs(data.bigram_frequency_by_language[language][bigram] - bf[bigram]) * DIFF_AMPLIFICATION
    for index in range(len(text) - 1):
        if text[index:index] in data.frequent_short_words_by_language[language][1]:
            fitness -= 0.5
    for index in range(len(text) - 2):
        if text[index:index + 1] in data.frequent_short_words_by_language[language][2]:
            fitness -= 0.5
    for index in range(len(text) - 3):
        if text[index:index + 2] in data.frequent_short_words_by_language[language][3]:
            fitness -= 0.5
    for index in range(len(text) - 4):
        if text[index:index + 3] in data.frequent_short_words_by_language[language][4]:
            fitness -= 0.5
    for index in range(len(text) - 5):
        if text[index:index + 4] in data.frequent_short_words_by_language[language][5]:
            fitness -= 0.5
    return fitness


FITNESS_MODES = {
    "a": fitness_aristocrat,
    "p": fitness_patristocrat
}


def calculate_fitness(text, language="en", mode="a"):
    return FITNESS_MODES[mode](text, language)
