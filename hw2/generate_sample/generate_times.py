import sys
import json
import random
import re
import time
import subprocess

WRONG_CHANCE = 0.05


def randTime():
    if randIsWrong(0.05):
        return random.choice([
            f'{randHour()}  {randMin()} {randMeridiem()}',
            f'{randHour()} {randMin()}  {randMeridiem()}',
        ])

    return f'{randHour()} {randMin()} {randMeridiem()}'


def randHour():
    if randIsWrong():
        return random.choice([
            f'{(int(random.random() * 5)+13):02d}',
            f'{((-int(random.random() * 5))+1):02d}',
            '0',
            '13'
            f'{(int(random.random() * 10))}',
            "wut",
        ])
    return f'{int(random.random() * 12) + 1}'


def randMin():
    if randIsWrong():
        return random.choice([
            f'{(int(random.random() * 5)+60):02d}',
            f'{(-int(random.random() * 5)):02d}',
            '60',
            f'{(int(random.random() * 10))}',
            "wut",
        ])
    return f'{int(random.random() * 59):02d}'


def randMeridiem():
    if randIsWrong():
        return random.choice([
            'am',
            'pm',
            'wut',
        ])
    return f'{random.choice(["AM", "PM"])}'


def randIsWrong(chance=WRONG_CHANCE):
    return random.random() < chance


if __name__ == '__main__':
    for i in range(100):
        # filename = int(time.time())
        filename = i+1
        outputFilename = f'sample_{filename}_input.txt'
        output = open(outputFilename, "w")
        numTimes = int(random.random() * 10) + 5
        for time in range(1, numTimes):
            output.write(f'{randTime()}\n')
        output.close()

        answer = open(f'sample_{filename}_output.txt', "w")
        proc = subprocess.Popen(['python3', 'hw2.py',  outputFilename],
                                stdout=answer, stderr=answer)

        answer.close()
