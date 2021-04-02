
TOP = open("templates/top.html").read()
BOTTOM = open("templates/bottom.html").read()

INDEX = "index.html"
ABOUT = "about.html"
BLOG = "blog.html"
PROJECTS = "projects.html"

BUILD_INDEX = TOP + open(f"./content/{INDEX}").read() + BOTTOM
BUILD_ABOUT = TOP + open(f"./content/{ABOUT}").read() + BOTTOM
BUILD_BLOG = TOP + open(f"./content/{BLOG}").read() + BOTTOM
BUILD_PROJECTS = TOP + open(f"./content/{PROJECTS}").read() + BOTTOM

open(f"./docs/{INDEX}", "w+").write(BUILD_INDEX)
open(f"./docs/{ABOUT}", "w+").write(BUILD_ABOUT)
open(f"./docs/{BLOG}", "w+").write(BUILD_BLOG)
open(f"./docs/{PROJECTS}", "w+").write(BUILD_PROJECTS)


