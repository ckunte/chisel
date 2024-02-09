#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# mc.py -- 2021 C Kunte
from config import EXT, POSTS, SHOWPOSTS, TFMT, TMPL, WWW
from functools import cmp_to_key
import jinja2
import markdown
import os
import pathlib
import time


LOC = [
    pathlib.Path.home() / POSTS,
    pathlib.Path.home() / WWW,
    pathlib.Path.home() / TMPL,
]


def FORMAT(text):
    return markdown.markdown(text, extensions=["smarty"])


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
                date = time.strptime(date_str, TFMT[0])
                year, month, day, hour, minute = date[:5]
                cover = f.readline().strip("\n\t")
                content = "".join(f.readlines()[0:])
                formatted_content = FORMAT(content)
                feed_date = time.strftime(TFMT[1], date)
                filename = "{}".format(os.path.splitext(name)[0])
                files.append(
                    {
                        "title": title,
                        "epoch": time.mktime(date),
                        "cover": cover,  # cover image if exists in line 3 of the post
                        "content": formatted_content,
                        "feed_date": feed_date,
                        "filename": filename,  # exclude file extension
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


# @step
# def home(f, e):
#    write_file(
#        f"index{EXT[0]}",
#        e.get_template("home.html").render(entries=f[: SHOWPOSTS[0]]),
#    )


@step
def feed(f, e):
    write_feed(
        "feed.json", e.get_template("feed.json").render(entries=f[: SHOWPOSTS[1]])
    )


@step
def weeknotes(f, e):
    write_file(
        f"w{EXT[0]}",
        e.get_template("weeknotes.html").render(entries=f[: SHOWPOSTS[2]]),
    )


def main():
    print("Chiseling...")
    print("\tReading files...", end="")
    files = sorted(get_tree(LOC[0]), key=cmp_to_key(compare_entries))
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(LOC[2]))
    print("done.")
    print("\tRunning steps...")
    for step in STEPS:
        step(files, env)
    print("\tdone.")
    print("done.")


if __name__ == "__main__":
    main()
