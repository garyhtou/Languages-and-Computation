"""Template for answers to be submitted as Part 1 of HW6, CPSC 3400, Spring 2021
ONLY change the string constants below and hand in this file after RENAMING it
to hw6.py. You can use (and modify) hw6_test.py to test your submission. Do NOT
hand in hw6_template.py or hw6_test.py.
"""


# Create a single regular expression that matches a string of digits and
# contains exactly two fives. Examples of acceptable strings include: "15445 " ,
# " 55 " , " 05563 " . However, the string is to be rejected if it contains
# anything other than digits.
a = r'^[012346789]*5[012346789]*5[012346789]*$'


# Create a single regular expression that matches a time expressed in the form
# "1:45 PM".
# Additional notes:
#   - The hours part must be a number from 1 to 12, the minutes range from 00 to
#     59, and the time must indicate either AM or PM (uppercase only and
#     preceded by exactly one space).
b = r'(?:^|\s)(?:1[0-2]|[1-9]):[0-5][0-9] (?:AM|PM)'


# Create a single regular expression that matches a string representing a comma
# separated list of variable names such as: hello, get_max, sum3
# Additional notes:
#   - A variable name consists of letters, digits, and underscores but cannot
#     start with a digit.
#   - There is exactly one space after every comma. No other spaces are allowed.
#   - Commas and spaces are not allowed before the first name and after the last
#     name.
#   - An empty string is considered a match.
#   - It is not a match if the list is not properly formed or if one of the
#     variable names is invalid.
c = r'(?:^$|^(?:[a-zA-Z_][a-zA-Z_0-9]*)(?:, [a-zA-Z_][a-zA-Z_0-9]*)*$)'

# Create a substitution, using a regular expression, that replaces all less than
# (<) and less than and equal to (<=) expressions with the equivalent greater
# than (>) or greater than or equal (>=). For instance, "a < b" would be
# replaced with "b > a".
# Additional notes:
#   - Only swap the "word" before and after the comparison. A word consists of
#     letters, digits, and underscores.
#   - Zero or more spaces may separate the comparison operator and the words.
#     When performing the substitution, use one space to separate the comparison
#     operator from the words.
#   - Do not perform the substitution if there is comparison does not contain a
#     word before and/or after the comparison. For example, a '<' sign appears at
#     the beginning of the string.
#   - You may assume that the string does not contain any chained comparisons
#     like a < b < c.
d = r'(?P<first>[a-zA-Z0-9_]+) *(?P<gt><)(?P<eq>=)? *(?P<second>[a-zA-Z0-9_]+)'
d_sub = r'\g<second> >\g<eq> \g<first>'
