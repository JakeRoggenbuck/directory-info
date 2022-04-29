#!/usr/bin/env python3
from os import getcwd
from pathlib import Path
from termcolor import colored
import argparse
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
NONE = Lang("NONE")


def check_lang(path: Path) -> Lang:
    if (path / Path("./setup.py")).exists():
        return PYTHON

    if (path / Path("./package.json")).exists():
        return JAVASCRIPT

    if (path / Path("./Cargo.toml")).exists():
        return RUST

    return NONE


class Zebra:
    def __init__(self):
        self.colors = ["white", "blue"]
        self.color_index = 0

    def color(self):
        new = 0 if self.color_index else 1
        color = self.colors[self.color_index]
        self.color_index = new
        return color

    def pad(self, length: int, char="-"):
        return " " + colored((length - 2) * char, self.color()) + " "


ZEBRA = Zebra()


class Directory:
    def __init__(self, path: Path, show_url: bool):
        self.path = path
        self.show_url = show_url

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
    def lang(self):
        return check_lang(Path(self.path))

    @property
    def has_lang(self):
        return self.lang != NONE

    @property
    def url(self):
        if (config := (self.path / ".git" / "config")).exists():
            with open(config) as file:
                for line in file:
                    if line[:6] == "\turl =":
                        return colored(line.split(" ")[-1].rstrip(), "green")
                else:
                    return colored("local only", "yellow")
        return ""

    def __repr__(self):
        first = self.git_status.ljust(5) + self.name
        second = self.url if self.show_url else ""

        char = "-" if len(self.url) > 2 else " "

        out = first

        if len(first) > 55:
            out += ZEBRA.pad(3, char=char) + second
        else:
            length = 56 - len(first)
            out += ZEBRA.pad(length + 2, char=char) + second

        if self.has_lang:
            out += self.lang.emoji + " " + self.lang.name

        return out


def create(show_url: bool):
    dirs = []
    current_directory = Path(getcwd())

    for file_path in current_directory.iterdir():
        if file_path.is_dir():
            directory = Directory(file_path, show_url)
            dirs.append(directory)

    return dirs


def run(dirs: list):
    for directory in dirs:
        print(directory)


def parser():
    parse = argparse.ArgumentParser()
    parse.add_argument("-u", "--url", help="Show URL", action="store_true")
    return parse.parse_args()


if __name__ == "__main__":
    args = parser()

    directories = create(args.url)
    run(directories)
