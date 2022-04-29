import random
import argparse

from fitness import calculate_fitness


RESTARTS = 5
ITERATIONS = 10000
ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def decode(text, key):
    plaintext = []
    for character in text:
        if not str(character).isalpha():
            plaintext.append(character)
        else:
            plaintext.append(key[character])
    return ''.join(plaintext)


def main():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--text", "-t", required=True, type=str, help="the text to be decrypted")
    argument_parser.add_argument("--language", "-l", required=False, default="en", help="the language of the text")
    args = argument_parser.parse_args()
    ciphertext = args.text.lower()
    results = {}
    for tries in range(RESTARTS):
        print(tries)
        key_list = list(ALPHABET)
        random.shuffle(key_list)
        key_string = ''.join([str(item) for item in key_list])
        key_dict = {}
        for i in range(len(ALPHABET)):
            key_dict[ALPHABET[i]] = key_string[i]
        text = decode(ciphertext, key_dict)
        fitness = calculate_fitness(ciphertext, args.language)
        for iteration in range(ITERATIONS):
            first = random.randrange(len(ALPHABET))
            second = first
            while second == first:
                second = random.randrange(len(ALPHABET))
            temp_letter = key_string[first]
            key_list_temp = []
            for letter in key_string:
                key_list_temp.append(letter)
            key_list_temp[first] = key_list_temp[second]
            key_list_temp[second] = temp_letter
            key_dict_temp = {}
            for i in range(len(ALPHABET)):
                key_dict_temp[ALPHABET[i]] = key_list_temp[i]
            text_temp = decode(ciphertext, key_dict_temp)
            fitness_temp = calculate_fitness(text_temp, language=args.language)
            if fitness_temp > fitness:
                text = text_temp
                fitness = fitness_temp
                key_string = ''.join([str(item) for item in key_list_temp])
        results[tries] = (text, fitness)
    print(results)
    final_result = ("", 0)
    for result in range(len(results)):
        if results[result][1] > final_result[1]:
            final_result = results[result]
    print(final_result)


if __name__ == "__main__":
    main()
