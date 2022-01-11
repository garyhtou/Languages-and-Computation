"""
Gary Tou
CPSC 3400, HW 1
1/10/2022
https://seattleu.instructure.com/courses/1602042/assignments/6989791
"""

# SUMMARY
# In this assignment, you will be tabulating results of a survey where people
# were asked to vote for their top three favorite colors (in order). The results
# of the survey are stored in an input file that has one or more lines in the
# following format:
#
# `blue green red`
# Each line refers to one survey response.
# The first color listed is the favorite color (call this a 1st place vote). The
# second color listed is the second favorite color (call this a 2nd place vote).
# The third color listed is the third favorite color (call this a 3rd place
# vote).  The colors are separated by a single space.
# Each color is a single word consisting of only lowercase letters.

import sys

def process_file(filename):
    """Reads and parses the input file. Creates and returns a dictionary
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


def get_first_place_votes(votes, color):
    """Returns the number of 1st place votes (possibly zero) for the provided
    color.
    Additional Restrictions: You must not use a loop in this function.

    Args:
        votes (dict of string: (int, int, int)): Dictionary returned from
            :func:`process_file`
        color (string): Color to look up
    Returns:
        int: Number of 1st place votes for the provided color
    """


def create_favorite_color_list(votes):
    """Returns an ordered list of colors based on the number of 1st place votes.
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
    """


def create_color_score_dict(votes):
    """Creates and returns a dictionary consisting of key-value pairs where the
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
    """


def print_dictionary(dictionary):
    """Prints the dictionary in sorted order (use sorted function). Print each
    entry on a separate line in the following format:
    .. code-block:: text
    key: value

    Additional Restrictions: You can make no assumptions on the type of
    dictionary.

    Args:
        dictionary (dict): Any dictionary
    Returns:
        None
    """


if __name__ == '__main__':
    # Get the name of the input file from the command line (using sys.argv)
    
    # https://stackoverflow.com/questions/14016742/detect-and-print-if-no-command-line-argument-is-provided
    
    if len(sys.argv) == 0:
        