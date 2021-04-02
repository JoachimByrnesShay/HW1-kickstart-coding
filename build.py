
TOP = open("templates/top.html").read()
BOTTOM = open("templates/bottom.html").read()

INDEX = "index.html"
ABOUT = "about.html"
BLOG = "blog.html"
PROJECTS = "projects.html"

CREATED_INDEX = TOP + open(f"./content/{INDEX}").read() + BOTTOM

open(f"./docs/{INDEX}", "w+").write(CREATED_INDEX)

