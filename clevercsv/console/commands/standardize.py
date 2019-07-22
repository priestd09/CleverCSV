# -*- coding: utf-8 -*-

import io

from cleo import Command

from clevercsv.read import reader
from clevercsv.wrappers import detect_dialect
from clevercsv.write import writer

from ._utils import parse_int


class StandardizeCommand(Command):
    """
    Convert a CSV file to one that conforms to RFC-4180.

    standardize
        { path : The path to the CSV file }
        { --e|encoding= : Set the encoding of the CSV file. This will also be
        used for the output file. }
        { --n|num-chars= : Limit the number of characters to read for
        detection. This will speed up detection but may reduce accuracy. }
        { --o|output= : Output file to write to. If omitted, print to stdout.}
    """

    def handle(self):
        verbose = self.io.verbosity > 0
        path = self.argument("path")
        output = self.option("output")
        encoding = self.option("encoding")
        num_chars = parse_int(self.option("num-chars"), "num-chars")

        dialect = detect_dialect(
            path, num_chars=num_chars, encoding=encoding, verbose=verbose
        )
        out = (
            io.StringIO(newline=None)
            if output is None
            else open(output, "w", encoding=encoding)
        )
        with open(path, "r", newline="", encoding=encoding) as fp:
            read = reader(fp, dialect=dialect)
            write = writer(out, dialect="excel")
            for row in read:
                write.writerow(row)
        if output is None:
            self.line(out.getvalue())
        out.close()