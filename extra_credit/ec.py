"""
Gary Tou
CPSC 3400, Extra Credit Assignment - Language Interpreter
1/19/2022
https://seattleu.instructure.com/courses/1602042/assignments/7001950
"""


import sys
import re
import csv


def interpret(script_filepath, data_filepath, pipeline_name):
    """
    Applies a pipeline from the script file to the Table provided by the data
    file. Returns the resulting Table upon successfully executing the pipeline
    on the Table. Please see the documentation (docstring) for the Table class
    for more information regarding the returned Table.

    Args:
        script (string): File path of the script file which contains the
            pipeline
        data (string): File path of the data CSV file
        pipeline (string): The name of the pipeline to be executed. This
            pipeline must be defined in the script file.

    Returns:
        Table: The resulting Table after executing the pipeline
    """
    pipeline = Pipeline(parse(script_filepath, pipeline_name))

    table = Table.from_file(data_filepath)

    output_table = pipeline.execute(table)

    print("===========================================================")
    print()
    print("INPUT TABLE:")
    print(table)
    print("OUTPUT TABLE:")
    print(output_table)

    return output_table


ARITH = "arithmetic"
PROJ = "project"


class InvalidPipeline(Exception):
    """
    Custom exception for invalid pipelines (bad syntax, etc.)
    """
    pass


class InvalidData(Exception):
    """
    Custom exception for invalid data (non-float values, etc.)
    """
    pass


class InvalidColumn(Exception):
    """
    Custom exception for invalid columns name (non-existent, etc.)
    """
    pass


def parse(script_file, pipeline):
    """
    Parse a script file and return the raw string for a specific pipeline

    Args:
        script_file (string): filepath of the scriipt file
        pipeline (string): name of the pipeline

    Raises:
        InvalidPipeline: The provided pipeline is missing or invalid

    Returns:
        string: The raw string for the pipeline
    """
    try:
        with open(script_file) as file:
            script = file.read()

            match = re.search(
                r"(pipeline\s+" + re.escape(pipeline) + r"\s+=(?:.|\s)*?;)", script)

            if match is None:
                raise InvalidPipeline(f"Pipeline {pipeline} not found")

            return match.group(0)
    except FileNotFoundError:
        print("Script file not found")
        sys.exit(1)


class Pipeline:
    """
    Represents a pipeline — which is made up of a sequence of Operations
    """

    def __init__(self, pipeline_str):
        self.raw = pipeline_str

        # Parse the pipline
        match = re.search(
            r"^pipeline\s+(?P<name>\w+)\s+=\s+(?P<body>(?:.|\s)+)\s+;$",
            pipeline_str)

        if match is None:
            raise InvalidPipeline(f"Pipeline is invalid")

        self.name = match.group("name")
        body = match.group("body")

        operation_strs = list(map(str.strip, body.split("|")))

        self.operations = list(map(lambda s: Operation(s), operation_strs))

    def execute(self, table):
        """
        Execute all operations in this pipeline on the given table

        Args:
            table (Table): The table to perform the pipeline on

        Returns:
            Table: The resulting table after all Operations have been performed
        """
        curr_table = table
        for operation in self.operations:
            curr_table = curr_table.apply(operation)

        return curr_table


class Operation:
    """
    Represents a single arithmetic (+, -, *, /, %) operation or a projection
    """

    def __init__(self, operation_str):
        arith_match = re.search(
            re.escape(ARITH)
            + r"\s+(?P<sym>\+|-|\*|/|%)\s+(?P<left>\w+)\s+(?P<right>\w+)\s+(?P<output>\w+);?",
            operation_str)

        if arith_match is not None:
            self.op = ARITH
            self.sym = arith_match.group("sym")
            self.left = arith_match.group("left")
            self.right = arith_match.group("right")
            self.output = arith_match.group("output")

            return

        proj_match = re.search(
            re.escape(PROJ) + r"\s+((?:.|\n)+);?",
            operation_str)

        if proj_match is not None:
            proj_cols = list(map(str.strip, proj_match.group(1).split()))

            self.op = PROJ
            self.cols = proj_cols
            return

        raise InvalidPipeline(f"Invalid operation: {operation_str}")

    def calculate(self, cols, row):
        """
        Performs the arithmetic calculation on the given row. This method can
        only be applied to arithmetic operations.

        Args:
            cols (list of strings): The column names of the table
            row (list of lists of floats): The rows of the table

        Raises:
            InvalidColumn: A column required for this operation is missing
            InvalidPipeline: The operation contains an unsupported arithmetic
                symbol

        Returns:
            float: The result of the arithmetic operation
        """
        leftValue = None
        rightValue = None

        try:
            leftValue = row[cols.index(self.left)]
        except ValueError as exc:
            raise InvalidColumn(f"Column {self.left} not found") from exc

        try:
            rightValue = row[cols.index(self.right)]
        except ValueError as exc:
            raise InvalidColumn(f"Column {self.right} not found") from exc

        if self.sym == "+":
            return leftValue + rightValue
        elif self.sym == "-":
            return leftValue - rightValue
        elif self.sym == "*":
            return leftValue * rightValue
        elif self.sym == "/":
            return leftValue / rightValue
        elif self.sym == "%":
            return leftValue % rightValue
        else:
            raise InvalidPipeline(f"Invalid arithmetic symbol: {self.sym}")

    def project(self, cols, row):
        """
        Performs a projection on the given row. This method can only be applied
        to projection Operations.

        Args:
            cols (list of strings): The column names of the table
            row (list of lists of floats): The rows of the table

        Raises:
            InvalidColumn: A column required for this operation is missing

        Returns:
            list of lists of floats: The resulting row after the projection
        """
        try:
            return [row[cols.index(col)] for col in self.cols]
        except ValueError as exc:
            raise InvalidColumn(f"A required column is missing")from exc

    def proj_columns(self):
        """
        Get the columns that are projected in this operation

        Returns:
            list of strings: Column names that remain after the projection
        """
        return self.cols


class Table:
    """
    Represents a table of data. A table can be created from a CSV file using the
    `from_file` class method. Each table's columns can be accessed using the
    `columns` method, and the rows (data) can be accessed using the `data`
    method.
    """

    def __init__(self, cols, data):
        self.cols = cols
        self.data = data

    @classmethod
    def from_file(cls, data_file):
        """
        Creates a table from a given data CSV file path

        Args:
            data_file (string): file path to the data CSV file

        Raises:
            InvalidData: The provided data contains non-float values

        Returns:
            Table: The Table created from the data CSV file
        """
        cols = []
        data = []

        try:
            header = True
            with open(data_file, newline='') as csvfile:
                spamreader = csv.reader(csvfile)
                for row in spamreader:
                    if header:
                        # Save the header row (columns of the table)
                        cols = row
                        header = False
                        continue

                    # Convert all values to floats
                    rowFloat = []
                    for cell in row:
                        try:
                            rowFloat.append(float(cell))
                        except:
                            raise InvalidData(
                                f"Invalid data: {cell} is not a float")

                    data.append(rowFloat)

            return cls(cols, data)

        except FileNotFoundError:
            print("Data file not found")
            sys.exit(1)

    def apply(self, operation):
        """
        Applies a given operation to this table. This table will not be modified

        Args:
            operation (Operation): The Operation to apply

        Returns:
            Table: The resulting table after the operation has been applied
        """
        if operation.op == ARITH:
            return Table(
                self.cols + [operation.output],
                [row + [operation.calculate(self.cols, row)]
                 for row in self.data]
            )

        elif operation.op == PROJ:
            return Table(
                operation.proj_columns(),
                [operation.project(self.cols, row)
                 for row in self.data]
            )

        else:
            return self

    def columns(self):
        return self.cols

    def data(self):
        return self.data

    def __str__(self):
        """
        Prepare a string representation of this table for pretty printing

        Returns:
            string: Pretty print string representation of this table
        """
        str = ""

        row_format = "{:<15}" * len(self.cols)
        str += (row_format.format(*self.cols)) + '\n'
        str += "-" * 15 * len(self.cols) + '\n'
        for row in self.data:
            str += (row_format.format(*row)) + '\n'

        str += '\n'

        return str


# if __name__ == "__main__":
#     interpret("timeDifferences.pipes", "times.csv", "timeDifference")

#     interpret("math.pipes", "math.csv", "add")
#     interpret("math.pipes", "math.csv", "sub")
#     interpret("math.pipes", "math.csv", "mul")
#     interpret("math.pipes", "math.csv", "div")
#     interpret("math.pipes", "math.csv", "mod")

#     interpret("fractions.pipes", "fraction.csv", "fraction")

#     interpret("spacing.pipes", "spacing.csv", "spacingLeading")
#     interpret("spacing.pipes", "spacing.csv", "spacingMultiLine")
#     interpret("spacing.pipes", "spacing.csv", "spacingReverse")

#     # The following are expected to fail
#     # interpret("math.pipes", "math.csv", "fail")
