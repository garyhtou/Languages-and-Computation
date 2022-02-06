import sys
import json
import random
import re
import time
import subprocess
import string


def randPointerName():
    start = string.ascii_letters + ('_' * 8)  # increase chance of underscore
    all = start + string.digits

    # first letter
    name = ''.join(random.choices(start, k=1))
    # rest of the name (optional)
    name += ''.join(random.choices(all, k=random.randint(0, 4)))

    return name


def genFile(name):
    inputFileName = f'sample_{name}_input.txt'
    inputFile = open(inputFileName, "w")

    # Create input file
    numBlocks = random.randint(1, 25)
    inputFile.write(f'{numBlocks}\n')

    used_pointers = []
    for line in range(random.randrange(1, numBlocks*2)):
        tail = None
        head = None

        if random.random() < 0.2:
            # pointer
            tail = randPointerName()
            while tail in used_pointers:
                tail = randPointerName()
        else:
            tail = random.randint(0, numBlocks-1)

        head = random.randint(0, numBlocks-1)

        inputFile.write(f'{tail},{head}\n')
    inputFile.close()

    # Output file
    answer = open(f'sample_{filename}_output.txt', "w")
    proc = subprocess.Popen(['python3', '../hw3.py',  inputFileName],
                            stdout=answer, stderr=answer)

    answer.close()


if __name__ == '__main__':

    for i in range(100):
        filename = i+1
        genFile(filename)
