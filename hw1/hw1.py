"""
Gary Tou
CPSC 3400, HW 1
1/10/2022
https://seattleu.instructure.com/courses/1602042/assignments/6989791

SUMMARY
In this assignment, you will be tabulating results of a survey where people
were asked to vote for their top three favorite colors (in order). The results
of the survey are stored in an input file that has one or more lines in the
following format:
```
blue green red
```

- Each line refers to one survey response.
- The first color listed is the favorite color (call this a 1st place vote). The
    second color listed is the second favorite color (call this a 2nd place vote).
- The third color listed is the third favorite color (call this a 3rd place
    vote). The colors are separated by a single space.
- Each color is a single word consisting of only lowercase letters.
"""


import sys


def process_file(filename):
    """
    Reads and parses the input file. Creates and returns a dictionary
    consisting of key-value pairs where the key is a color and the value is a
    tuple consisting of three integers: (number of 1st place votes, number of
    2nd place votes, number of 3rd place votes). The dictionary only contains
    colors that appeared in the file.
    Assumptions: The input file exists and is formatted as described above. The
    input file contains at least one line.

    Args:
        filename (string): Name of the input file
    Returns:
        dict of string: (int, int, int): A dictionary consisting of key-value
            pairs where the key is string and the value is a tuple consisting of
            three integers.
    """
    votes = {}
    with open(filename) as file:
        # Loop through each line (strip leading and trailing whitespace)
        while (line := file.readline().strip()):
            # Split line for the 3 colors
            colors = line.split()
            # Loop through each color and increment the vote counter
            for index, color in enumerate(colors):
                # Add color to votes if it doesn't already exist
                if color not in votes:
                    votes[color] = (0, 0, 0)

                # Convert the tuple into a list and add the vote
                color_list = list(votes[color])
                # The index is also the vote place (1st, 2nd, 3rd)
                color_list[index] += 1
                # Convert the list back into a tuple
                votes[color] = tuple(color_list)

    return votes


def get_first_place_votes(votes, color):
    """
    Returns the number of 1st place votes (possibly zero) for the provided
    color.
    Additional Restrictions: You must not use a loop in this function.

    Args:
        votes (dict of string: (int, int, int)): Dictionary returned from
            :func:`process_file`
        color (string): Color to look up
    Returns:
        int: Number of 1st place votes for the provided color

    >>> get_first_place_votes({'red': (1, 2, 3), 'blue': (4, 5, 6)}, 'red')
    1
    >>> get_first_place_votes({'black': (24, 25, 26), 'white': (27, 28, 29)}, 'white')
    27
    >>> get_first_place_votes({'red': (1, 2, 3), 'blue': (4, 5, 6)}, 'green')
    0
    """
    try:
        return votes[color][0]
    except KeyError:
        # The color has no votes... at all.
        # I guess it must be a pretty yucky color ¯\_(ツ)_/¯
        return 0


def create_favorite_color_list(votes):
    """
    Returns an ordered list of colors based on the number of 1st place votes.
    The first item in the list is the color that had the most 1st place votes.
    The second item in the list is the color that had the second most 1st place
    votes. The list only contains colors that receive at least one 1st place
    vote. Ties are broken as follows: 1) winner is the color with higher number
    of 2nd place votes, 2) if still tied, winner is the color with higher number
    of 3rd place votes, 3) if still tied, winner is the color that appears
    earlier in alphabetical order.

    Args:
        votes (dict of string: (int, int, int)): Dictionary returned from
            :func:`process_file`
    Returns:
        list of string: Ordered list of colors based on the number of 1st place
            votes.

    >>> create_favorite_color_list({'red': (1, 2, 3), 'blue': (4, 5, 6)})
    ['blue', 'red']
    >>> create_favorite_color_list({'black': (24, 25, 26), 'white': (27, 28, 29)})
    ['white', 'black']
    >>> create_favorite_color_list({'red': (1, 2, 3), 'blue': (1, 5, 6)})
    ['blue', 'red']
    >>> create_favorite_color_list({'red': (1, 2, 6), 'blue': (1, 2, 3)})
    ['red', 'blue']
    >>> create_favorite_color_list({'red': (1, 2, 3), 'blue': (1, 2, 3)})
    ['blue', 'red']
    >>> create_favorite_color_list({'green': (0, 2, 3), 'yellow': (7, 2, 3)})
    ['yellow']
    """
    # filter out colors that don't have any 1st place votes
    filtered_votes = {key: value for (
        key, value) in votes.items() if value[0] > 0}

    # I am negating the value to sort in descending order (higher votes first).
    # Can't use "Reverse" because that would also reverse the alphabetical sort.
    return sorted(filtered_votes.keys(),
                  key=lambda color: (-votes[color][0],
                                     -votes[color][1],
                                     -votes[color][2],
                                     # lastly, sort by alphabetical order
                                     color))


def create_color_score_dict(votes):
    """
    Creates and returns a dictionary consisting of key-value pairs where the
    key is a color and the value is an integer that is computed using the
    following formula (number of 1st place votes x 3) + (number of 2nd place
    votes x 2) + (number of 3rd place votes). The dictionary only contains
    colors that appeared in the file.

    Args:
        votes (dict of string: (int, int, int)): Dictionary returned from
            :func:`process_file`
    Returns:
        dict of string: int: A dictionary consisting of key-value pairs where
            the key is string and the value is an integer.

    >>> create_color_score_dict({'red': (1, 2, 3), 'blue': (4, 5, 6)})
    {'red': 10, 'blue': 28}
    >>> create_color_score_dict({'black': (24, 25, 26), 'white': (27, 28, 29)})
    {'black': 148, 'white': 166}
    >>> create_color_score_dict({'red': (1, 2, 4)})
    {'red': 11}
    """
    # Create dictionary using comprehension
    return {key: (value[0] * 3) + (value[1] * 2) + (value[2])
            for (key, value) in votes.items()}


def print_dictionary(dictionary):
    """
    Prints the dictionary in sorted order (use sorted function). Print each
    entry on a separate line in the following format:
    .. code-block:: text
    key: value

    Additional Restrictions: You can make no assumptions on the type of
    dictionary.

    Args:
        dictionary (dict): Any dictionary
    Returns:
        None

    >>> print_dictionary({'red': (1, 2, 3), 'blue': (4, 5, 6)})
    blue: (4, 5, 6)
    red: (1, 2, 3)
    >>> print_dictionary({'white': (27, 28, 29), 'black': (24, 25, 26)})
    black: (24, 25, 26)
    white: (27, 28, 29)
    >>> print_dictionary({'red': (1, 2, 3), 'blue': (1, 5, 6)})
    blue: (1, 5, 6)
    red: (1, 2, 3)
    >>> print_dictionary({'red': [(1, 2, 6), (1, 2, 6)], 'blue': ((2, 3), 2, 3), 'green': None})
    blue: ((2, 3), 2, 3)
    green: None
    red: [(1, 2, 6), (1, 2, 6)]
    >>> print_dictionary({}) # prints nothing
    """
    for key, value in sorted(dictionary.items()):
        print(f"{key}: {value}")


if __name__ == '__main__':
    # Get the name of the input file from the command line (using sys.argv)
    try:
        filepath = sys.argv[1]
    except IndexError:
        # Exit if no input file is provided
        print("Usage: hw1 <filepath>")
        sys.exit(1)

    # Process the input file
    votes = process_file(filepath)

    # Print the dictionary
    print_dictionary(votes)

    # Get and print the first place votes for 'blue'
    first_place_blue = get_first_place_votes(votes, 'blue')
    print(first_place_blue)

    # Get and print the first place votes for 'green'
    first_place_green = get_first_place_votes(votes, 'green')
    print(first_place_green)

    # Get and print the favorite colors
    favorite_colors = create_favorite_color_list(votes)
    print(favorite_colors)

    # Get and print the color scores
    color_score = create_color_score_dict(votes)
    print_dictionary(color_score)
