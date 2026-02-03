#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# mc.py -- 2025 C Kunte

from config import EXT, POSTS, SHOWPOSTS, TFMT, TMPL, WWW
from functools import cmp_to_key
import hashlib
import j2m
import jinja2
import markdown
import os
import pathlib
import time


# Define the locations for posts, www, and templates
LOC_POSTS = pathlib.Path.home() / POSTS
LOC_WWW = pathlib.Path.home() / WWW
LOC_TMPL = pathlib.Path.home() / TMPL


def FORMAT(text):
    """Convert markdown text to HTML."""
    return markdown.markdown(text, extensions=["smarty", "extra"])


# Store the steps for processing
STEPS = []


def step(func):
    """Decorator to wrap processing steps with print statements."""

    def wrapper(*args, **kwargs):
        print(f"\t\tGenerating {func.__name__}...", end="")
        try:
            func(*args, **kwargs)
            print("done.")
        except Exception as e:
            print(f"failed: {e}")

    STEPS.append(wrapper)
    return wrapper


def get_tree(source):
    """Walk through the source directory and gather post data."""
    files = []
    for root, _, fs in os.walk(source):
        for name in fs:
            if not name.endswith(
                (".md", ".mdown")
            ) or name.startswith("."):
                continue

            path = pathlib.Path(root) / name

            try:
                with open(path, "r", encoding="utf-8") as f:
                    title = f.readline().strip()
                    date_str = f.readline().strip()
                    content = f.read()

                    date = time.strptime(date_str, TFMT[0])
                    year = date.tm_year

                    formatted_content = FORMAT(content)
                    feed_date = time.strftime(TFMT[1], date)
                    nice_date = time.strftime(TFMT[2], date)
                    filename_without_ext = path.stem

                    files.append(
                        {
                            "title": title,
                            "epoch": time.mktime(date),
                            "content": formatted_content,
                            "url": f"{year}/{filename_without_ext}",
                            "feed_date": feed_date,
                            "nice_date": nice_date,
                        }
                    )
            except Exception as e:
                print(f"Error processing file '{path}': {e}")
    return files


def compare_entries(x, y):
    # Sort by epoch in descending order
    if y["epoch"] != x["epoch"]:
        return y["epoch"] - x["epoch"]
    # If epochs are the same, sort by filename in descending order
    return (y["filename"] > x["filename"]) - (
        x["filename"] > y["filename"]
    )


def write_file(url_path, data, is_feed=False):
    """Write data to a file, handling directory creation."""
    full_path = LOC_WWW / url_path
    if not is_feed:
        full_path = full_path.with_suffix(
            EXT[1]
        )  # Add .html extension for regular pages

    full_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(data)
    except Exception as e:
        print(f"Failed to write file '{full_path}': {e}")


@step
def home(files, env):
    """Generate the home page."""
    write_file(
        f"index{EXT[0]}",
        env.get_template("home.j2").render(entries=files),
    )


@step
def notes(files, env):
    """Generate individual note pages."""
    # Pre-load the template once for efficiency
    detail_template = env.get_template("detail.j2")
    for file in files:
        write_file(
            file["url"],
            detail_template.render(entry=file, entries=files),
        )


@step
def feed(files, env):
    """Generate the feed."""
    write_file(
        "feed.json",
        env.get_template("feed.j2").render(
            entries=files[: SHOWPOSTS[0]]
        ),
        is_feed=True,  # Indicate this is a feed file, so no .html extension is added
    )


def main():
    """Main function to orchestrate file processing."""
    print("Chiseling...")
    print("\tReading files...", end="")
    try:
        files = sorted(
            get_tree(LOC_POSTS),
            key=cmp_to_key(compare_entries),
        )
        print("done.")
    except Exception as e:
        print(f"Error during file reading: {e}")
        return

    print("\tSetting up Jinja2 environment...", end="")
    try:
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(LOC_TMPL),
            extensions=["j2m.MarkdownExtension"],
            autoescape=jinja2.select_autoescape(
                ["html", "xml", "json"]
            ),
        )
        print("done.")
    except Exception as e:
        print(f"Error setting up Jinja2: {e}")
        return

    print("\tRunning steps...")
    for step_func in STEPS:
        try:
            step_func(files, env)
        except Exception as e:
            print(f"A step failed but the process will continue: {e}")
    print("\tdone.")


if __name__ == "__main__":
    main()
