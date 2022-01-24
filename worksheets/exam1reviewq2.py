from pprint import pprint
import sys


def tally_last(file):
    letters = {}
    with open(file) as file:
        while (line := file.readline().strip()):
            words = line.split()

            for word in words:
                letter = word[-1]

                if letter in letters:
                    letters[letter] += 1
                else:
                    letters[letter] = 1

    return letters


# print(tally_last(sys.argv[1]))
pprint(tally_last(sys.argv[1]))

# python3 worksheets/exam1reviewq1.py ~/Code/garyhtou/cpsc3400/hw1/generate_sample/sample2.txt;
