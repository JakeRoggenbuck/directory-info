#!/usr/bin/env python3
from os import getcwd
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


class Zebra:
    def __init__(self):
        self.colors = ["white", "blue"]
        self.color_index = 0

    def color(self):
        new = 0 if self.color_index else 1
        color = self.colors[self.color_index]
        self.color_index = new
        return color

    def pad(self, length: int):
        return " " + colored((length - 2) * "-", self.color()) + " "


ZEBRA = Zebra()


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

    @property
    def url(self):
        if (config := (self.path / ".git" / "config")).exists():
            with open(config) as file:
                for line in file:
                    if line[:6] == '\turl =':
                        return colored(line.split(" ")[-1].rstrip(), "green")
                else:
                    return colored("local only", "yellow")
        return ""

    def __repr__(self):
        first = self.git_status.ljust(5) + self.name
        second = self.url

        if len(first) > 55:
            return first + ZEBRA.pad(3) + second

        length = 56 - len(first)
        return first + ZEBRA.pad(length + 2) + second


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
