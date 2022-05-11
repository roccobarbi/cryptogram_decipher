import random
import argparse

from .fitness import calculate_fitness


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


def invert_list_elements(input_list, first, second):
    output = []
    for element in input_list:
        output.append(element)
    output[first] = input_list[second]
    output[second] = input_list[first]
    return output


def iteration(ciphertext, language, alphabet, key_list, mode):
    first, second = extract_two(len(alphabet))
    temp_keys = invert_list_elements(key_list, first, second)
    key_dict_temp = {}
    for i in range(len(alphabet)):
        key_dict_temp[alphabet[i]] = temp_keys[i]
    plaintext = decode(ciphertext, key_dict_temp)
    fitness = calculate_fitness(plaintext, language=language, mode=mode)
    return plaintext, fitness, temp_keys


def restart_cycle(ciphertext, alphabet, language, mode, iterations=ITERATIONS):
    key_list = list(alphabet)
    random.shuffle(key_list)
    key_dict = {}
    for i in range(len(alphabet)):
        key_dict[ALPHABET[i]] = key_list[i]
    plaintext = decode(ciphertext, key_dict)
    fitness = calculate_fitness(plaintext, language=language, mode=mode)
    changed = 0
    for i in range(iterations):
        text_temp, fitness_temp, key_list_temp = iteration(ciphertext, language, alphabet, key_list, mode)
        if fitness_temp < fitness:
            changed += 1
            plaintext = text_temp
            fitness = fitness_temp
            key_list = key_list_temp
    print('Changed {} times'.format(changed))
    return plaintext, fitness


def decipher(restarts, alphabet, language, mode, iterations, ciphertext, results):
    for tries in range(restarts):
        print(str(tries))
        results[tries] = restart_cycle(ciphertext, alphabet, language, mode, iterations=iterations)
        print('{index:d}: {fitness:.5f}'.format(index=tries, fitness=results[tries][1]))
    final_result = None
    for result in range(len(results)):
        if final_result is None:
            final_result = results[result]
        if results[result][1] < final_result[1]:
            final_result = results[result]
    return final_result


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
    final_result = decipher(
        args.restarts,
        args.alphabet,
        args.language,
        args.mode,
        args.iterations,
        ciphertext)
    print(final_result)


if __name__ == "__main__":
    main()
