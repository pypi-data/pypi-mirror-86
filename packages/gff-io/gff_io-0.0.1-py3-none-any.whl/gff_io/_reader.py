"""
GFF3 File Format
----------------

The first line of a GFF3 file must be a comment that identifies the version, e.g.

```
##gff-version 3
```

Fields must be tab-separated. Also, all but the final field in each feature line must contain a
value; "empty" columns should be denoted with a '.'.

- seqid: name of the chromosome or scaffold;
- source: name of the program that generated this feature, or the data source (database or project
  name);
- type: type of feature. Must be a term or accession from the SOFA sequence ontology;
- start: Start position of the feature, with sequence numbering starting at 1;
- end: End position of the feature, with sequence numbering starting at 1;
- score: A floating point value;
- strand: defined as + (forward) or - (reverse);
- phase: One of '0', '1' or '2'. '0' indicates that the first base of the feature is the first base
  of a codon, '1' that the second base is the first base of a codon, and so on;
- attributes: A semicolon-separated list of tag-value pairs, providing additional information about
  each feature. Some of these tags are predefined, e.g. ID, Name, Alias, Parent - see the GFF
  documentation for more details;

Example:

```
##gff-version 3
ctg123 . mRNA            1300  9000  .  +  .  ID=mrna0001;Name=sonichedgehog
ctg123 . exon            1300  1500  .  +  .  ID=exon00001;Parent=mrna0001
ctg123 . exon            1050  1500  .  +  .  ID=exon00002;Parent=mrna0001
ctg123 . exon            3000  3902  .  +  .  ID=exon00003;Parent=mrna0001
ctg123 . exon            5000  5500  .  +  .  ID=exon00004;Parent=mrna0001
ctg123 . exon            7000  9000  .  +  .  ID=exon00005;Parent=mrna0001
```
"""
from __future__ import annotations

import dataclasses
from collections import OrderedDict
from pathlib import Path
from typing import IO, Dict, Iterator, List, Optional, Type, Union

from more_itertools import peekable
from xopen import xopen

__all__ = [
    "ParsingError",
    "Item",
    "Reader",
    "read_gff",
]


class ParsingError(Exception):
    """
    Parsing error.
    """

    def __init__(self, line_number: int, opt_msg: Optional[str] = None):
        """
        Parameters
        ----------
        line_number
            Line number.
        opt_msg
            Optional message.
        """
        msg = f"Line number {line_number}."
        if opt_msg is not None:
            msg = f"{msg} {opt_msg}"
        super().__init__(msg)
        self._line_number = line_number

    @property
    def line_number(self) -> int:
        """
        Line number.

        Returns
        -------
        Line number.
        """
        return self._line_number


@dataclasses.dataclass
class Item:
    """
    GFF item.

    Attributes
    ----------
    seqid
        Bla.
    """

    seqid: str
    source: str
    type: str
    start: str
    end: str
    score: str
    strand: str
    phase: str
    attributes: str

    def attributes_asdict(self) -> Dict:
        attrs = []
        for item in self.attributes.split(";"):
            name, value = item.partition("=")[::2]
            attrs.append((name, value))
        return OrderedDict(tuple(attrs))

    @classmethod
    def parse(cls: Type[Item], line: str, line_number: int) -> Item:
        try:
            args = line.split("\t")
            assert len(args) == 9
            return cls(*tuple(args))
        except Exception:
            raise ParsingError(line_number)

    def copy(self) -> Item:
        """
        Copy of itself.

        Returns
        -------
        GFF item.
        """
        from copy import copy

        return copy(self)


class Reader:
    """
    GFF reader.
    """

    def __init__(self, file: Union[str, Path, IO[str]]):
        """
        Parameters
        ----------
        file
            File path or IO stream.
        """
        if isinstance(file, str):
            file = Path(file)

        if isinstance(file, Path):
            file = xopen(file, "r")

        self._file = file
        self._lines = peekable(line for line in file)
        self._line_number = 0

        try:
            line = self._next_line()
        except StopIteration:
            raise ParsingError(self._line_number, "Expected `##gff-version 3`.")

        self._header = line
        if self._header != "##gff-version 3":
            raise ParsingError(self._line_number, "Expected `##gff-version 3`.")

        try:
            line = self._lines.peek()
            while line.startswith("##"):
                self._next_line()
                line = self._lines.peek()
        except StopIteration:
            pass

    def read_item(self) -> Item:
        """
        Get the next item.

        Returns
        -------
        Next item.
        """
        line = self._next_line()
        if line.startswith("##"):
            raise StopIteration()
        return Item.parse(line, self._line_number)

    def read_items(self) -> List[Item]:
        """
        Get the list of all items.

        Returns
        -------
        List of all items.
        """
        return list(self)

    def close(self):
        """
        Close the associated stream.
        """
        self._file.close()

    @property
    def header(self) -> str:
        """
        File header.

        Returns
        -------
        Header.
        """
        return self._header

    def _next_line(self) -> str:
        line = next(self._lines).strip()
        self._line_number += 1
        return line

    def __iter__(self) -> Iterator[Item]:
        while True:
            try:
                yield self.read_item()
            except StopIteration:
                return

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        del exception_type
        del exception_value
        del traceback
        self.close()

    def __str__(self) -> str:
        return self.header


def read_gff(file: Union[str, Path, IO[str]]) -> Reader:
    """
    Open a GFF file for reading.

    Parameters
    ----------
    file
        File path or IO stream.

    Returns
    -------
    GFF reader.
    """
    return Reader(file)
