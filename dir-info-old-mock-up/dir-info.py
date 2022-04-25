#!/usr/bin/env python3

from termcolor import colored
import attr

@attr.s
class Lang:
    name = attr.ib()
    emoji = attr.ib(default="📦")

    def __hash__(self):
        return self.name

PYTHON = Lang("Python", "🐍")
RUST = Lang("Rust", "🦀")
JAVA = Lang("Java")
JAVASCRIPT = Lang("JS")

repos = [
    ('ImportLint', PYTHON, "Clean out your python imports."),
    ('mahou', RUST, "Compact programming language."),
    ('qme4', JAVA, "Exploration game."),
    ('Highlight', JAVASCRIPT, "Social media app"),
    ('pathfinder', RUST, "Utility to add and remove items from $PATH."),
    ('pac_drop', PYTHON, "Configuration manager"),
    ('learning-langs', PYTHON, "A place to put things I have learned."),
    ('pygron', PYTHON, "Python JSON viewer."),
    ('pathfinder', RUST, "Utility to add and remove items from $PATH."),
    ('github_api', PYTHON, "Access github API."),
    ('MongoLinkShorten', PYTHON, "Web app to shorten URls."),
]

print("")

for repo in repos:
    name = colored(repo[0].ljust(20), "blue", attrs=["bold"])
    emoji = repo[1].emoji
    lang = colored(repo[1].name.rjust(10), attrs=["bold"])
    desc = repo[2]

    message = f"{emoji} {name} {lang} {desc}"
    print(message)

print("")
