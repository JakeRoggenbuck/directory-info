from functools import cached_property

from os import listdir, getcwd
from pathlib import Path


class Directory:
    def __init__(self, path_str: str):
        self.path_str = path_str
        self.path = Path(self.path_str)

        if not self.path.is_dir():
            self = None

        self.name = self.path_str.split("/")[-1]

    @cached_property
    def is_dir(self):
        return self.path.exists()

    @cached_property
    def files(self):
        return listdir(self.path)

    @cached_property
    def has_readme(self):
        for name in ["readme.md", "readme.rst"]:
            if name in map(str.lower, self.files):
                print(name)
                return True

        return False

    def __repr__(self):
        return f"{self.name}"

if __name__ == "__main__":
    dirs = map(lambda x: Directory(x), listdir(getcwd()))
    for directory in dirs:
        print(directory)
