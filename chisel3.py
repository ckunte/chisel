#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Chisel by D Zhou, github.com/dz
# Fork and mod by C Kunte, github.com/ckunte
import re
import time
import os
import jinja2
import markdown
from functools import cmp_to_key
# SETTINGS: Begin user inputs --
LOC = [
    os.environ["HOME"] + "/Sites/posts/",         # post files in markdown (.md)
    os.environ["HOME"] + "/Sites/ln.lo/",         # local www folder
    os.environ["HOME"] + "/Sites/chisel/vanilla/" # jinja2 templates
]
RSS_SHOW = 9 # change the number of entries in RSS feed to suit
# -- End of user inputs --
TFMT = ["%B %-d, %Y", "%a, %d %b %Y %H:%M:%S %z", "%Y-%m-%d", "%b %d"] # Date: [As shown, In RSS, in .md posts] respectively
FORMAT = lambda text: markdown.markdown(text,extensions=['markdown.extensions.smarty','markdown.extensions.tables','markdown.extensions.footnotes'])
EXT = ["", ".html"] # URLEXT, PATHEXT
STEPS = []
def step(func):
    def wrapper(*args, **kwargs):
        print("\t\tGenerating %s..." %func.__name__, end="");
        func(*args, **kwargs)
        print("done.")
    STEPS.append(wrapper)
    return wrapper

def get_tree(source):
    files = []
    for root, ds, fs in os.walk(source):
        for name in fs:
            if name[0] == ".": continue
            if not re.match(r'^.+\.(md|mdown)$', name): continue
            path = os.path.join(root, name)
            f = open(path, "r")
            title = f.readline().strip('\n\t')
            date = time.strptime(f.readline().strip(), TFMT[2])
            year, month, day = date[:3]
            files.append({
                'title': title,
                'epoch': time.mktime(date),
                'content': FORMAT(''.join(f.readlines()[1:])),
                'url': '/'.join([str(year), os.path.splitext(name)[0]]),
                'pretty_date': time.strftime(TFMT[0], date),
                'rssdate': time.strftime(TFMT[1], date),
                'sdate': time.strftime(TFMT[3], date),
                'date': date,
                'year': year,
                'month': month,
                'day': day,
                'filename': name})
            f.close()
    return files

def compare_entries(x, y):
    result = (y['epoch'] > x['epoch']) - (y['epoch'] < x['epoch'])
    if result == 0:
        return (y['filename'] > x['filename']) - (y['filename'] < x['filename'])
    return result

def write_file(url, data):
    path = LOC[1] + url + EXT[1]
    dirs = os.path.dirname(path)
    if not os.path.isdir(dirs):
        os.makedirs(dirs)
    file = open(path, "w")
    file.write(data)
    file.close()

# def write_feed(url, data):
#     path = LOC[1] + url
#     file = open(path, "w")
#     file.write(data)
#     file.close()

@step
def posts(f, e):
    for file in f:
        write_file(file['url'], e.get_template('detail.html').render(entry=file, entries=f))

@step
def homepage(f, e):
    write_file('index%s' %EXT[0], e.get_template('home.html').render(entries=f[:RSS_SHOW]))

@step
def archive(f, e):
    write_file('archive%s' %EXT[0], e.get_template('archive.html').render(entries=f))

# @step
# def feed(f, e):
#     write_feed('rss.xml', e.get_template('feed.html').render(entries=f[:RSS_SHOW]))

# @step
# def aboutpage(f, e):
#     write_file('about%s' %EXT[0], e.get_template('about.html').render(entry=f))

def main():
    print("Chiseling...");
    print("\tReading files...", end="");
    files = sorted(get_tree(LOC[0]), key=cmp_to_key(compare_entries))
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(LOC[2]))
    print("done.")
    print("\tRunning steps...");
    for step in STEPS:
        step(files, env)
    print("\tdone.")
    print("done.")

if __name__ == "__main__":
    main()