#!/usr/bin/env python3
from os import listdir, getcwd, chdir
from pathlib import Path
from termcolor import colored
import attr


@attr.s
class Lang:
    name: str = attr.ib()
    emoji: str = attr.ib(default="📦")

    def __hash__(self):
        return self.name


PYTHON = Lang("Python", "🐍")
RUST = Lang("Rust", "🦀")
JAVA = Lang("Java")
JAVASCRIPT = Lang("JS")


class Directory:
    def __init__(self, path: Path):
        self.path = path

    @property
    def has_git(self):
        return (self.path / ".git").exists()

    @property
    def git_status(self):
        return ".git" if self.has_git else "----"

    @property
    def name(self):
        return colored(str(self.path.name), "blue", attrs=["bold"])

    def __repr__(self):
        return self.git_status.ljust(5) + self.name


def create():
    dirs = []
    current_directory = Path(getcwd())

    for file_path in current_directory.iterdir():
        if file_path.is_dir():
            directory = Directory(file_path)
            dirs.append(directory)

    return dirs


def run(dirs: list):
    for directory in dirs:
        print(directory)


if __name__ == "__main__":
    directories = create()
    run(directories)
