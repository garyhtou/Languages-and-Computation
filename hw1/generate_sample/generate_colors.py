import sys
import json
import random
import re
import time


def randColor(colors):
    while True:
        color = colors[int(len(colors) * random.random())]
        name = color['name'].lower()

        if re.match("^([a-z]+)$", name):
            return name


if __name__ == '__main__':
    try:
        color_filepath = sys.argv[1]
    except IndexError:
        # Exit if no input file is provided
        print("Usage: generate_colors <filepath>")
        sys.exit(1)

    file = open(color_filepath)
    colors = json.load(file)

    output = open(f"sample_{int(time.time())}.txt", "w")
    num_votes = int(random.random() * 100) + 1
    for vote in range(1, num_votes):
        output.write(
            f"{randColor(colors)} {randColor(colors)} {randColor(colors)}\n")
    output.close()
