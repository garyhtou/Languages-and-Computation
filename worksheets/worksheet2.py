"""
Gary Tou
CPSC 3400, Worksheet 2
1/7/2022
"""


def worksheet2a():
    # Gary: Sharer
    # Kate: Narrator
    # Terence: Reporter
    lo = int(input('low: '))
    hi = int(input('high: '))
    for i in range(lo, hi, 3):
        print(i)


def worksheet2b():
    # Gary: Narrator
    # Kate: Reporter
    # Terence: Sharer
    pass


def worksheet2c(list):
    # Individual work
    def floatify(list):
        hasNonFloat = True
        for num in list:
            if type(num) == int:
                num = float(num)
            else:
                hasNonFloat = False

        return hasNonFloat

    def purify(seq):
        return tuple(seq)

    floatify(list)
    purify(list)


def worksheet2d():
    # Individual work
    def letter_frequency(text):
        """Return a dictionary keyed by the alphabetic letters in given 
        text, counting the occurences of each letter. 
        """
        letter_counts = {}
        for letter in text:
            # standardize letter
            stdLetter = letter.upper()
            if letter.isalpha():  # only count letters
                if stdLetter not in letter_counts:
                    letter_counts[stdLetter] = 0  # add key to dictionary
                letter_counts[stdLetter] += 1  # increment count for letter
        return letter_counts

    def grade_range(grade):
        grade_table = {'A': (0.9, 1.0), 'B': (0.8, 0.9), 'C': (0.7, 0.8),
                       'D': (0.6, 0.7), 'F': (0.0, 0.6)}
        # return print(grade_table[grade])
        return grade_table[grade]

    # letter_frequency(text)
    print(grade_range('A'))


def main():
    worksheet2a()
    worksheet2b()
    worksheet2c()
    worksheet2d()


if __name__ == "__main__":
    main()
