#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Chisel by D Zhou (github.com/dz); Fork + mod by C Kunte (github.com/ckunte)
import sys
import re
import time
import os
import pathlib
import jinja2
import markdown
from functools import cmp_to_key
import gzip
from config import *


LOC = [
    os.path.join(os.environ["HOME"], POSTS),
    os.path.join(os.environ["HOME"], WWW),
    os.path.join(os.environ["HOME"], TMPL),
]


FORMAT = lambda text: markdown.markdown(
    text, extensions=["smarty", "tables", "fenced_code", "footnotes"]
)


STEPS = []


def step(func):
    def wrapper(*args, **kwargs):
        print(f"\t\tGenerating {func.__name__}...", end="")
        func(*args, **kwargs)
        print("done.")

    STEPS.append(wrapper)
    return wrapper


def get_tree(source):
    files = []
    for root, ds, fs in os.walk(source):
        for name in fs:
            if name.startswith(".") or not name.endswith((".md", ".mdown")):
                continue
            path = os.path.join(root, name)
            with open(path, "r") as f:
                title = f.readline().strip("\n\t")
                date_str = f.readline().strip()
                date = time.strptime(date_str, TFMT[2])
                year, month, day, hour, minute = date[:5]
                files.append(
                    {
                        "title": title,
                        "epoch": time.mktime(date),
                        "desc": f.readline().strip("\n\t"),
                        "content": FORMAT("".join(f.readlines()[1:])),
                        "url": f"{year}/{os.path.splitext(name)[0]}",
                        "pretty_date": time.strftime(TFMT[0], date),
                        "feed_date": time.strftime(TFMT[3], date),
                        "year": year,
                        "filename": name,
                    }
                )
    return files


def compare_entries(x, y):
    result = (y["epoch"] > x["epoch"]) - (y["epoch"] < x["epoch"])
    if result == 0:
        return (y["filename"] > x["filename"]) - (y["filename"] < x["filename"])
    return result


def write_file(url, data):
    path = pathlib.Path(LOC[1]) / f"{url}{EXT[1]}"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write(data)


def write_feed(url, data):
    path = pathlib.Path(LOC[1]) / url
    with open(path, "w") as f:
        f.write(data)


# def write_sitemap(url, data):
#    path = pathlib.Path(LOC[1]) / url
#    with gzip.open(path, "wb") as f:
#        f.write(data.encode("UTF-8"))


# @step
# def gen_sitemap(f, e):
#    write_sitemap("sitemap.xml.gz", e.get_template("sitemap.html").render(entries=f))


@step
def feed(f, e):
    write_feed("feed.json", e.get_template("feed.json").render(entries=f[:RSS_SHOW]))
    # write_feed("rss.xml", e.get_template("atom.xml").render(entries=f[:RSS_SHOW]))


@step
def homepage(f, e):
    write_file(f"index{EXT[0]}", e.get_template("home.html").render(entries=f))


@step
def notes(f, e):
    for i, file in enumerate(f):
        write_file(
            file["url"], e.get_template("detail.html").render(entry=file, entries=f)
        )


# @step
# def aboutpage(f, e):
#    write_file(f"about{EXT[0]}", e.get_template("about.html").render(entries=f))


# @step
# def notes_list(f, e):
#    write_file(f"archive{EXT[0]}", e.get_template("archive.html").render(entries=f))


# @step
# def sponsoring(f, e):
#    write_file(f"mad{EXT[0]}", e.get_template("mad.html").render(entries=f))


def main():
    print("Chiseling...")
    print("\tReading files...", end="")
    files = sorted(get_tree(LOC[0]), key=cmp_to_key(compare_entries))
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(LOC[2]),
        extensions=["jinja2_markdown.MarkdownExtension"],
    )
    print("done.")
    print("\tRunning steps...")
    for step in STEPS:
        step(files, env)
    print("\tdone.")
    print("done.")


if __name__ == "__main__":
    sys.exit(main())
