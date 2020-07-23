# Chisel configuration
POSTS = "Sites/notes/"            # location of posts (in markdown) folder 
WWW = "Sites/ck.lo/"              # local www folder (upload contents to a web host)
TMPL = "Sites/chisel/plain/" 	  # jinja templates folder
# Number of posts to show in RSS feed
RSS_SHOW = 3
# For URLs without ending in .html
EXT = ["", ".html"]  # [URLEXT, PATHEXT]
## For URLs ending in .html
#EXT = [".html", ""]  # [URLEXT, PATHEXT]
TFMT = [                        # Various date and time formats
    "%B %Y",                    # Date as shown on html pages
    "%a, %d %b %Y %H:%M:%S %z", # Date and time for RSS feed
    "%Y-%m-%d %H:%M"            # Time format to use in markdown posts
    ]
