#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# mc.py -- 2021 C Kunte
import os, re, time, datetime
import markdown, jinja2
from functools import cmp_to_key
from config import *


LOC = [
    os.environ["HOME"] + "/" + POSTS, 
    os.environ["HOME"] + "/" + WWW,
    os.environ["HOME"] + "/" + TMPL
]


FORMAT = lambda text: markdown.markdown(text,extensions=['smarty','footnotes'])


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
            date = time.strptime(f.readline().strip(), TFMT[0])
            year, month, day, hour, minute = date[:5]
            week = datetime.date(year, month, day).isocalendar()[1]
            files.append({
              'title': title,
              'date': date,
              'epoch': time.mktime(date),
              'content': FORMAT(''.join(f.readlines()[1:])),
              'feed_date': time.strftime(TFMT[1], date),
              'year': year,
              'week': week
              })
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

    
def write_feed(url, data):
    path = LOC[1] + url
    file = open(path, "w")
    file.write(data)
    file.close()


@step
def home(f, e):
    write_file('index%s' %EXT[0], e.get_template('home.html').render(entries=f[:SHOWPOSTS[0]]))


@step
def feed(f, e):
    write_feed('rss.xml', e.get_template('atom.xml').render(entries=f[:SHOWPOSTS[1]]))


@step
def weeknotes(f, e):
    write_file('w%s' %EXT[0], e.get_template('weeknotes.html').render(entries=f[:SHOWPOSTS[2]]))


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
