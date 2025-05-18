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


# Define the locations for posts, www, and templates
LOC = [
    pathlib.Path.home() / POSTS,
    pathlib.Path.home() / WWW,
    pathlib.Path.home() / TMPL,
]


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
            if name.startswith(".") or not name.endswith((".md", ".mdown")):
                continue
            
            path = os.path.join(root, name)
            try:
                with open(path, "r") as f:
                    title = f.readline().strip("\n\t")
                    date_str = f.readline().strip()
                    date = time.strptime(date_str, TFMT[0])
                    year, month, day, hour, minute = date[:5]
                    # cover = f.readline().strip("\n\t")
                    content = f.read()  # Read the rest of the content
                    formatted_content = FORMAT(content)
                    feed_date = time.strftime(TFMT[1], date)
                    nice_date = time.strftime(TFMT[2], date)
                    # filename = os.path.splitext(name)[0] # exclude file extension
                    
                    files.append({
                        "title": title,
                        "epoch": time.mktime(date),
                        # "cover": cover,  # cover image if exists in line 3 of the post
                        "content": formatted_content,
                        "url": f"{year}/{os.path.splitext(name)[0]}",
                        #"url": f"notes/{os.path.splitext(name)[0]}",
                        "feed_date": feed_date,
                        "nice_date": nice_date,
                        # "filename": filename,
                    })
            except Exception as e:
                print(f"Error processing file '{path}': {e}")
    return files


def compare_entries(x, y):
    """Compare two entries for sorting."""
    result = (y["epoch"] > x["epoch"]) - (y["epoch"] < x["epoch"])
    return result or (y["filename"] > x["filename"]) - (x["filename"] > y["filename"])


def write_file(url, data):
    """Write data to a file."""
    path = pathlib.Path(LOC[1]) / f"{url}{EXT[1]}"
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, "w") as f:
            f.write(data)
    except Exception as e:
        print(f"Failed to write file '{path}': {e}")


def write_feed(url, data):
    """Write feed data to a JSON file."""
    path = pathlib.Path(LOC[1]) / url
    try:
        with open(path, "w") as f:
            f.write(data)
    except Exception as e:
        print(f"Failed to write feed '{path}': {e}")


@step
def home(files, env):
    """Generate the home page."""
    write_file(
        f"index{EXT[0]}",
        #env.get_template("home.j2").render(entries=files[: SHOWPOSTS[0]]),
        env.get_template("home.j2").render(entries=files),
    )


#@step
#def notes_index(files, env):
#    """Generate the home page."""
#    write_file(
#        f"notes/index{EXT[0]}",
#        env.get_template("notes.j2").render(entries=files),
#    )

@step
def notes(files, env):
    for i, file in enumerate(files):
        write_file(
            file["url"], env.get_template("detail.j2").render(entry=file, entries=files)
        )

@step
def feed(files, env):
    """Generate the feed."""
    write_feed(
        "feed.json", env.get_template("feed.j2").render(entries=files[: SHOWPOSTS[0]])
    )


def main():
    """Main function to orchestrate file processing."""
    print("Chiseling...")
    print("\tReading files...", end="")
    try:
        files = sorted(get_tree(LOC[0]), key=cmp_to_key(compare_entries))
        print("done.")
    except Exception as e:
        print(f"Error reading files: {e}")
        return
    
    print("\tSetting up Jinja2 environment...", end="")
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(LOC[2]),
        extensions=["j2m.MarkdownExtension"],
    )
    print("done.")

    print("\tRunning steps...")
    for step in STEPS:
        step(files, env)
    print("\tdone.")
    print("Process completed.")


if __name__ == "__main__":
    main()
