import random
import argparse
import sys

from fitness import calculate_fitness


RESTARTS = 5
ITERATIONS = 10000
ALPHABET = "abcdefghijklmnopqrstuvwxyz"
MODES = {
    "a": "aristocrat",
    "p": "patristocrat"
}


def decode(text, key):
    plaintext = []
    for character in text:
        if not str(character).isalpha():
            plaintext.append(character)
        else:
            plaintext.append(key[character])
    return ''.join(plaintext)


def extract_two(length):
    first = random.randrange(length)
    second = first
    while second == first:
        second = random.randrange(length)
    return first, second


def iteration(ciphertext, language, alphabet, key_string, mode):
    first, second = extract_two(len(alphabet))
    temp_letter = key_string[first]
    key_list = []
    for letter in key_string:
        key_list.append(letter)
    key_list[first] = key_list[second]
    key_list[second] = temp_letter
    key_dict_temp = {}
    for i in range(len(alphabet)):
        key_dict_temp[alphabet[i]] = key_list[i]
    plaintext = decode(ciphertext, key_dict_temp)
    fitness = calculate_fitness(plaintext, language=language, mode=mode)
    key_string = ''.join([str(item) for item in key_list])
    return plaintext, fitness, key_string


def restart_cycle(ciphertext, alphabet, language, mode):
    key_list = list(alphabet)
    random.shuffle(key_list)
    key_string = ''.join([str(item) for item in key_list])
    key_dict = {}
    for i in range(len(alphabet)):
        key_dict[ALPHABET[i]] = key_string[i]
    plaintext = decode(ciphertext, key_dict)
    fitness = calculate_fitness(plaintext, language=language, mode=mode)
    for i in range(ITERATIONS):
        text_temp, fitness_temp, key_string_temp = iteration(ciphertext, language, alphabet, key_string, mode)
        if fitness_temp < fitness:
            plaintext = text_temp
            fitness = fitness_temp
            key_string = key_string_temp
    return plaintext, fitness


def main():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--text", "-t", required=True, type=str, help="the text to be decrypted")
    argument_parser.add_argument("--language", "-l", required=False, type=str, default="en",
                                 help="the language of the text")
    argument_parser.add_argument("--alphabet", "-a", required=False, type=str, default=ALPHABET,
                                 help="the alphabet that has to be considered")
    argument_parser.add_argument("--iterations", "-i", required=False, type=int, default=ITERATIONS,
                                 help="the number of iterations in each restart cycle")
    argument_parser.add_argument("--restarts", "-r", required=False, type=int, default=RESTARTS,
                                 help="the number of restart cycles")
    argument_parser.add_argument("--mode", "-m", required=False, type=str, default="a",
                                 choices=MODES.keys(), help="The type of cryptogram.")
    args = argument_parser.parse_args()
    ciphertext = args.text.lower()
    results = {}
    for tries in range(RESTARTS):
        print(str(tries))
        results[tries] = restart_cycle(ciphertext, args.alphabet, args.language, args.mode)
        print(str(tries) + ": " + str(results[tries][1]))
    final_result = None
    for result in range(len(results)):
        if final_result is None:
            final_result = results[result]
        if results[result][1] < final_result[1]:
            final_result = results[result]
    print(final_result)


if __name__ == "__main__":
    main()
