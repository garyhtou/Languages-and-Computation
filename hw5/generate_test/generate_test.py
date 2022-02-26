import sys
import json
import random
import re
import time
import subprocess
import string


class Operation(object):
    def __init__(self, name, children):
        self.name = name
        self.children = children

    def __str__(self):
        if not self.children:
            return self.name

        params = [str(child) for child in self.children]
        return f'({self.name}({", ".join(params)}))'


class X(Operation):
    def __init__(self):
        super().__init__('X', [])


class Y(Operation):
    def __init__(self):
        super().__init__('Y', [])


class Const(Operation):
    def __init__(self, value):
        super().__init__('Const', [])
        self.value = value

    def __str__(self):
        return f'({self.name} {float(self.value)})'


class Neg(Operation):
    def __init__(self, child):
        super().__init__('Neg', [child])


class Add(Operation):
    def __init__(self, left, right):
        super().__init__('Add', [left, right])


class Sub(Operation):
    def __init__(self, left, right):
        super().__init__('Sub', [left, right])


class Mul(Operation):
    def __init__(self, left, right):
        super().__init__('Mul', [left, right])


term_classes = [X, Y, Const]
branch_classes = [Neg, Add, Sub, Mul]
classes = term_classes + branch_classes

NUM_TESTS = 100
DIM_FACTOR = 2


def create_expression(chance):
    def rand_class(classes):
        return random.choice(classes)

    klass = rand_class(branch_classes) if random.random(
    ) < chance else rand_class(term_classes)

    if klass == X:
        return X()
    elif klass == Y:
        return Y()
    elif klass == Const:
        return Const(round(random.uniform(-50, 50)))
    elif klass == Neg:
        return Neg(create_expression(chance/DIM_FACTOR))
    elif klass == Add:
        return Add(create_expression(chance/DIM_FACTOR), create_expression(chance/DIM_FACTOR))
    elif klass == Sub:
        return Sub(create_expression(chance/DIM_FACTOR), create_expression(chance/DIM_FACTOR))
    elif klass == Mul:
        return Mul(create_expression(chance/DIM_FACTOR), create_expression(chance/DIM_FACTOR))


def main():
    t = int(time.time())
    filename = f'hw5_tests.txt'
    file = open(filename, "w")

    for i in range(NUM_TESTS):
        expr = create_expression(random.uniform(0.5, 4))

        output = f'genTestAssertions "({str(expr)})" ({str(expr)}) "Gary\'s Generated test {i}_{t}"'

        file.write(f'{output}\n')

    file.close()


if __name__ == '__main__':
    main()
