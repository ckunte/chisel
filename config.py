# Chisel configuration
POSTS = "Sites/wkly/"          # location of posts (in markdown) folder 
WWW = "Sites/ck.lo/"         # local www folder (upload contents to a web host)
TMPL = "Sites/chisel/plain/"   # jinja templates folder

SHOWPOSTS = [1, 12, 54]

TFMT = [
  "%Y-%m-%d %H:%M",
  "%Y-%m-%dT%H:%M:00+08:00",
  "%b %d %H:%M"
]

EXT = ["", ".html"] # URLEXT, PATHEXT