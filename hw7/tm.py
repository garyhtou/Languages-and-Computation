"""Turing machine simulator
K. Lundeen for CPSC 3400, Seattle University for Homework 7

Usage:
   python3 tm.py tm_file input_string [mode]

   mode (default 3):
   1 - interactive, step by step
   2 - step by step, noninteractive
   3 - just show final tape output, halting state, and accept/reject
"""

import sys

# Modes
STEP_INTERACTIVE = 1
STEP_BY_STEP = 2
RESULT_ONLY = 3


class TuringMachine(object):
    """The Turing machine simulator"""

    def __init__(self, tm_file, input_tape):
        """filename is a TM file as described in homework assignment HW7:
        In a Turing machine, states are represented by non-negative integers.
        The tape alphabet consists of any desired characters. The character B
        represents a blank character.

        In the file, the first line contains two integers separated by a comma:
            initial state, accepting state

        Each subsequent line of the file refers to a different transition
        represented by a comma-separated list:
            current state, current input, next state, new symbol, direction

        For instance, the line 0,x,1,y,R means that if the Turing machine is
        currently in state 0 with the head reading an x it will transition to
        state 1, overwrite the current tape cell with a y, and then move the
        head right one cell.

        Notes:
        •	The five fields within a line are separated by commas.
        •	Spaces in the line are removed and ignored. You may have an
        optional
            comment at the end of the line that starts with a # character
            (like in Python).
        •	The symbol B represents a blank character on the tape.
        •	The direction can be either L or R.
        •	Only one accepting state (noted on the first line) is permitted. As
            with Turing machines, you cannot have transitions out of the
            accepting state.
        •	The same input pair (current state, current input) cannot appear
            multiple times in the file.
        •	The simulator halts when there is no transition for the current
            input pair. Just like real Turing machines, it is possible for the
            simulator to go into an infinite loop.
        •	After the required first line, lines that start with # are ignored
            and can be used for comments.
        •	If you do something wrong (such as type in the filename
            incorrectly), you will likely get an uncaught Python exception
            rather than a clear error message.
        """
        self.tape = input_tape
        self.head = 0
        self.current = None
        self.delta = {}
        with open(tm_file, 'r') as lines:
            for line in lines:
                line = line.split('#')[0].rstrip()
                line = line.replace(' ', '')
                if line == '':
                    continue
                fields = line.split(',')
                if self.current is None:
                    self.current, self.accepting = (int(f) for f in fields)
                else:
                    in_state, in_tape, out_state, out_tape, way = fields
                    in_state, out_state = int(in_state), int(out_state)
                    if way not in ('R', 'L'):
                        raise ValueError('direction must be R or L')
                    if len(in_tape) != 1 or len(out_tape) != 1:
                        raise ValueError('current_input and new_symbol must '
                                         'be single characters')
                    self.delta[(in_state, in_tape)] = (out_state, out_tape, way)

    def step(self):
        """Go one step forward; halt (return False) if nothing to do"""
        key = (self.current, self.tape[self.head])
        if key in self.delta:
            out_state, out_tape, way = self.delta[key]
            self.current = out_state
            self.tape = (self.tape[:self.head] + out_tape + self.tape[
                                                            self.head + 1:])
            if way == 'R':
                self.head += 1
                if len(self.tape) == self.head:
                    self.tape += 'B'
            elif self.head == 0:
                self.tape = 'B' + self.tape
            else:
                self.head -= 1
            return True
        else:
            return False

    def simulate(self, mode):
        """Step through the simulation until it halts"""
        self.display(mode)
        while self.step():
            self.display(mode)
        print('output:', self.tape.lstrip('B').rstrip('B'))
        print('state: ', self.current)
        print('accepted' if self.current == self.accepting else 'rejected')

    def display(self, mode):
        """Display on the console the current state of the tm"""
        if mode == RESULT_ONLY:
            return
        print(self.tape)
        print(' ' * self.head + '^')
        print(self.current)
        if mode == STEP_INTERACTIVE:
            input()
        else:
            print()


if __name__ == '__main__':
    if not 3 <= len(sys.argv) <= 4:
        print('Usage:\n'
              '\tpython3 tm.py tm_file input_string [mode]\n'
              '\n'
              '\tmode (default 3):\n'
              '\t1 - interactive, step by step\n'
              '\t2 - step by step, noninteractive\n'
              '\t3 - just show final tape output, halting state, '
              'and accept/reject\n')
        exit(1)
    tm_file, input_string = sys.argv[1:3]
    mode = RESULT_ONLY if len(sys.argv) == 3 else int(sys.argv[3])
    if not STEP_INTERACTIVE <= mode <= RESULT_ONLY:
        raise ValueError('Mode must be 1, 2, or 3')
    tm = TuringMachine(tm_file, input_string)
    tm.simulate(mode)
