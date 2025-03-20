import sys
import argparse
import zipfile

from pathlib import Path
from enum import Enum
from typing import Sequence

import rarfile


class ArchiveType(str, Enum):
    ZIP = "zip"
    RAR = "rar"
    CBZ = "cbz"
    CBR = "cbr"


def main():
    target_folder = _get_target_folder()
    archives = _search_archives(target_folder)

    for archive in archives:
        sys.stdout.write(f"Unpacking it: {archive.name}...")
        match archive.suffix[1:]:
            case ArchiveType.ZIP | ArchiveType.CBZ:
                with zipfile.ZipFile(archive) as zipfile_:
                    if archive.stem == zipfile_.namelist()[-1].strip("/"):
                        dist = archive.parent
                    else:
                        dist = Path(archive.parent, archive.stem)
                    zipfile_.extractall(path=dist)
                sys.stdout.write(f"\rUnpacking it: {archive.name}... Done\n")
            case ArchiveType.RAR | ArchiveType.CBR:
                with rarfile.RarFile(archive) as rarfile_:
                    if archive.stem == rarfile_.namelist()[-1].strip("/"):
                        dist = archive.parent
                    else:
                        dist = Path(archive.parent, archive.stem)
                    rarfile_.extractall(path=dist)
                sys.stdout.write(f"\rUnpacking it: {archive.name}... Done\n")
            case _:
                break


def _get_target_folder() -> Path:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    return parser.parse_args().path.absolute()


def _search_archives(folder: Path) -> Sequence[Path]:
    archives = []
    for element in folder.rglob("*"):
        for archive_type in ArchiveType:
            if archive_type == element.suffix[1:]:
                archives.append(element)
    if len(archives) == 0:
        sys.stderr.write("Archives not found\n")
        exit(1)
    return archives


if __name__ == "__main__":
    main()
