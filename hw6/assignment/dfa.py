"""DFA Simulator
K. Lundeen for CPSC 3400, Seattle University for Homework 6

Usage:
   python3 dfa.py dfa_file strings_file
"""

import sys


class DFA(object):
    """DFA Simulator
    >>> dfa = DFA('dfa_example.txt')
    >>> dfa.alphabet
    {'a': 0, 'b': 1}
    >>> dfa.states
    [[0, 1], [0, 2], [0, 2]]
    >>> dfa.final
    {2}
    """
    def __init__(self, filename):
        """filename is a dfa file as described in homework assignemnt HW6:
        •   The first line will contain one or more characters that define the
            input alphabet.
            •	Each character in the input alphabet is separated by a single
                space.
            •	Each character in the input alphabet is a unique single letter
                or digit.
        •	All subsequent lines will each refer to a different state in the
            DFA. The second line in the file (the first line after the input
            alphabet definition line) will be state 0. The third line in the
            file will be state 1, the fourth line in the file will be state 2,
            and so forth.
            •	The first character in the line will either be a '+' (accepting
                state) or '–' (rejecting state).
            •	Then there will be n nonnegative integers where n is the number
                of characters in the input alphabet. Each integer refers to the
                destination state for a transition for the corresponding input
                character.
            •	The corresponding input character is based on the order of the
                states and the order of the input characters on the first line
                of the file. If the input alphabet line is "D O G". The first
                integer the destination state for input D, the second is for
                input O, the third is for input G.
            •	The integers are separated by a single space. There is also a
                single space between the first character (+ or –) and the first
                integer.
        •	State 0 is the starting state.
        •	The simulator does not have any explicit error checking for
            incorrectly formatted files. Many errors (but not necessarily all of
            them) will cause an exception to be thrown, aborting the program.
        """
        self.alphabet = None
        self.states = []
        self.final = set()
        with open(filename, 'r') as lines:
            for line in lines:
                if self.alphabet is None:
                    self.alphabet = {}
                    for i, symbol in enumerate(line.split()):
                        self.alphabet[symbol] = i
                else:
                    states = line.split()
                    if states[0] == '+':
                        self.final.add(len(self.states))
                    self.states.append([int(state) for state in states[1:]])

    def simulate(self, string):
        """Process a string through this DFA. Return the ending state."""
        state = 0
        for symbol in string:
            state = self.states[state][self.alphabet[symbol]]
        return state

    def is_final(self, state):
        """Determine if given state is a final (accepting) state."""
        return state in self.final


def dfa_simulator(dfa_file, strings_file):
    """Create a DFA simulator and run each string in given file though it.
    The strings file contains one or more strings that will be executed in the
    DFA.
    •	Each line will be interpreted as a test string.
    •	Each string will be processed by the DFA and the simulator will print
        out the final state along with whether the string is accepted or
        rejected.
    •	The lines in the string file must only contain characters from the DFA
        alphabet. If a letter outside the alphabet is found, a KeyError
        exception will abort the script.
    >>> dfa_simulator('dfa_example.txt', 'strings_example.txt')
    'abb' ends in state 2: accepted
    'abababaabb' ends in state 2: accepted
    '' ends in state 0: rejected
    'aab' ends in state 1: rejected
    """
    dfa = DFA(dfa_file)
    with open(strings_file, 'r') as strings:
        for string in strings:
            string = string.rstrip()
            state = dfa.simulate(string)
            note = 'accepted' if dfa.is_final(state) else 'rejected'
            print("'{}' ends in state {}: {}".format(string, state, note))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage:\n\tpython3 dfa.py dfa_file strings_file')
        exit(1)
    dfa_file, strings_file = sys.argv[1:]
    dfa_simulator(dfa_file, strings_file)
