import math

from crypto_tools import data
from crypto_tools.stats.letter_frequency import LetterFrequency, LetterCounter
from crypto_tools.stats.ngram_frequency import NgramFrequency, NgramCounter


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
    total = 0
    fitness = 0
    lf = LetterFrequency(text)
    lc = LetterCounter(text).count()
    length = 0
    t4c = NgramCounter(text=text, nvalue=4, joined=True, lower=True).count()
    letter_total_diff = 0
    for letter in lf.calculate():
        if str(letter) in lf.get_alphabet():
            letter_diff = data.letter_frequency_by_language[language][letter] - lf.calculate()[letter]
            letter_total_diff += abs(letter_diff) * lc[letter]
            length += lc[letter]
    fitness -= letter_total_diff / length
    for tetragram in t4c.keys():
        if tetragram in data.tetragram_frequency_by_language[language].keys():
            total += t4c[tetragram] * math.log10(data.tetragram_frequency_by_language[language][tetragram])
        else:
            total += t4c[tetragram] * math.log10(0.000000000000001)
    if total == 0:
        raise Exception("total 0?!?")
    fitness += abs(total / len(text))
    return fitness


FITNESS_MODES = {
    "a": fitness_aristocrat,
    "p": fitness_patristocrat
}


def calculate_fitness(text, language="en", mode="a"):
    return FITNESS_MODES[mode](text, language)
