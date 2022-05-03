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
    def __init__(self, path: Path, no_url: bool, no_emoji: bool):
        self.path = path
        self.no_url = no_url
        self.no_emoji = no_emoji

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
        url = "" if self.no_url else self.url

        char = "-"

        out = first

        if len(first) > 55:
            out += ZEBRA.pad(3, char=char)
        else:
            length = 56 - len(first)
            out += ZEBRA.pad(length + 2, char=char)

        if self.has_lang:
            pre = " " if self.no_emoji else self.lang.emoji
            out += (pre + " " + self.lang.name).ljust(10 if self.no_emoji else 9)
        else:
            out += " " * 10

        out += url

        return out


def create(show_url: bool, no_emoji: bool):
    dirs = []
    current_directory = Path(getcwd())

    for file_path in current_directory.iterdir():
        if file_path.is_dir():
            directory = Directory(file_path, show_url, no_emoji)
            dirs.append(directory)

    return dirs


def run(dirs: list):
    for directory in dirs:
        print(directory)


def parser():
    parse = argparse.ArgumentParser()
    parse.add_argument("--no-url", help="No URL", action="store_true")
    parse.add_argument("--no-emoji", help="No Emoji", action="store_true")
    return parse.parse_args()


if __name__ == "__main__":
    args = parser()

    directories = create(args.no_url, args.no_emoji)
    run(directories)
