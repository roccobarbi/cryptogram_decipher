from crypto_tools import data
from crypto_tools.stats.letter_frequency import LetterFrequency
from crypto_tools.stats.ngram_frequency import NgramFrequency


def calculate_fitness(text, language="en"):
    lf = LetterFrequency(text).calculate()
    bf = NgramFrequency(text=text, nvalue=2).calculate()
    fitness = 100
    for letter in lf:
        fitness -= abs(data.letter_frequency_by_language[language][letter] - lf[letter])
    for bigram in bf:
        fitness -= abs(data.bigram_frequency_by_language[language][bigram] - bf[bigram])
    for index in range(len(text) - 2):
        if text[index:index+1] in data.frequent_short_words_by_language[language][2]:
            fitness += 1
