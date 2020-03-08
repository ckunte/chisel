# Chisel

Chisel is a (lean and simple) static site generator written in [python]. It is a personalised fork of [dz's version] converted to python3 with the following additional features.

## Features

1. Content parsing to generate smart typographic punctuation via [smartypants extension] to [markdown in python]
1. Static pages (e.g. about page)
1. RSS feed generator
1. A shorter (year-based) permalink structure with support for clean URLs
1. Post descriptions
1. [Jinja] templates featuring
	1. Customised homepage
	1. Custom archive page
	1. Post navigation
	1. Post count
	1. Read time
	1. [KaTeX] support for rendering math in posts
	1. Syntax highlighting for code via [highlight.js]

### Regrets

It has:

- No taxonomy support
- No built-in search

## Installation

```bash
git clone --depth=1 https://github.com/ckunte/chisel.git
python3 -m pip install -r chisel/requirements.txt
```

And to upgrade requirements, run:

```bash
python3 -m pip install --upgrade -r chisel/requirements.txt
```

## Site settings

There are two (plain text) files that need user input, viz.,

1. `chisel_conf.py`: Set folder locations, number of posts in RSS feed, and clean URL settings
2. `templates/site_settings.jinja`: Set site_title, author, author's email, and number of posts to show on the homepage

### Suggested folder structure

- `chisel`: folder containing this repository
- `posts`: folder containing posts written in markdown
- `www`: folder containing generated site (upload its contents to a web host)

## How it works

1. Write posts in Markdown, save it as `post-title.md` or `posttitle.md` (or `post_title.md`) in a designated folder, say, `posts`. (See Sample Entry for post format below.)
2. Run `python3 chisel.py` in a Terminal, and C1 will parse all `.md`, `.markdown` or `.mdown` files in `posts` folder to another designated folder, say `www` in html. -- ready to be uploaded to a web server, typically to either a `www` or a `public_html` folder on a web host.
3. Sync all files and folders from the local `www` folder to the root folder of a web host (typically to a `www` or a `public_html` folder) to get a website with generated content.

### Typical usage

```bash
cd ~/Sites/chisel
python3 chisel.py
```

### Sample post

Post format is simple, which is as follows:

- Line 1: Enter a title
- Line 2: Enter date in Y-m-d HH:MM
- Line 3: Description line
- Line 4: Blank line
- Line 5: Content in Markdown here onward

Contents of a post named `sample.md` are as follows:

```markdown
Chateau de Chambord
2010-05-05 21:50
One last contribution by the Renaissance master.

The 50km route from Amboise to Chambord is scenic, the air in early April still uncomfortably cold. Visibility is greater from lack of foliage early in Spring. The entrance is grand, the chateau looks iconic from afar.
```

[dz's version]: https://github.com/dz/chisel
[python]: http://www.python.org/
[Jinja]: https://jinja.palletsprojects.com/
[KaTeX]: https://katex.org/
[markdown in python]: https://python-markdown.github.io/
[smartypants extension]: https://python-markdown.github.io/extensions/smarty/
[highlight.js]: https://highlightjs.org
