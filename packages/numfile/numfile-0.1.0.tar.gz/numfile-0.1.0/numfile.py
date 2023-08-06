"""
Automatically assign an increasing sequence number to file names.
"""

__version__ = "0.1.0"

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Union, Optional, IO, Iterator, List


@dataclass
class NumberedFile:
    """File name with an automatically incrementing counter."""

    parent: Path
    name: str
    number: Optional[int] = None
    suffix: str = ""

    @classmethod
    def of(cls, path: Union[str, Path]) -> "NumberedFile":
        """Create a new instance from string or a path object."""

        if isinstance(path, str):
            path = Path(path)

        parts: list[str] = path.name.split(".")
        name, suffix = parts[0], ".".join(parts[1:])

        if suffix != "":
            suffix = f".{suffix}"

        match = re.match(r"^(.*?)-(\d+)?$", path.name.rstrip(suffix))
        stem = match.group(1) if match else name
        number = int(match.group(2)) if match else None

        return cls(path.parent, stem, number, suffix)

    @property
    def path(self) -> Path:
        """Return the full path of the current file."""
        if self.number is None:
            filename = f"{self.name}{self.suffix}"
        else:
            filename = f"{self.name}-{self.number}{self.suffix}"
        return self.parent / filename

    @property
    def next(self) -> "NumberedFile":
        """Return a file with the next number."""

        _latest = self.latest

        if _latest.path.exists():
            if _latest.number is None:
                number = 2
            else:
                number = _latest.number + 1
        else:
            number = _latest.number or 1

        return NumberedFile(
            _latest.parent,
            _latest.name,
            number,
            _latest.suffix,
        )

    @property
    def latest(self) -> "NumberedFile":
        """Return a file with the highest number."""
        files = self.siblings_descending
        return files[0] if len(files) > 0 else self

    @property
    def siblings_ascending(self) -> List["NumberedFile"]:
        """Return similar files in the same directory in ascending order."""
        return sorted(self.siblings, key=lambda x: x.number or 0)

    @property
    def siblings_descending(self) -> List["NumberedFile"]:
        """Return similar files in the same directory in ascending order."""
        return sorted(self.siblings, key=lambda x: x.number or 0, reverse=True)

    @property
    def siblings(self) -> Iterator["NumberedFile"]:
        """Return similar files in the same directory."""
        if self.parent.exists():
            for child in self.parent.iterdir():
                sibling = NumberedFile.of(child.absolute())
                if self.name == sibling.name and self.suffix == sibling.suffix:
                    yield sibling


def open_all(
    path: Union[str, Path],
    mode: str = "r",
    encoding: Optional[str] = "utf-8",
    *args,
    **kwargs,
) -> Iterator[IO]:
    """Open numbered files in ascending order in read mode by default."""
    for numbered_file in NumberedFile.of(path).siblings_ascending:
        file: Optional[IO] = None
        try:
            yield (
                file := open(
                    numbered_file.path,
                    mode=mode,
                    encoding=encoding,
                    *args,
                    **kwargs,
                )
            )
        finally:
            if file is not None:
                file.close()


def open_latest(
    path: Union[str, Path],
    mode: str = "a",
    encoding: Optional[str] = "utf-8",
    *args,
    **kwargs,
) -> IO:
    """Open a file with the highest number in append mode by default."""
    return open(
        NumberedFile.of(path).latest.path,
        mode=mode,
        encoding=encoding,
        *args,
        **kwargs,
    )


def open_next(
    path: Union[str, Path],
    mode: str = "w",
    encoding: Optional[str] = "utf-8",
    *args,
    **kwargs,
) -> IO:
    """Open a file with the next number in write mode by default."""
    return open(
        NumberedFile.of(path).next.path,
        mode=mode,
        encoding=encoding,
        *args,
        **kwargs,
    )
