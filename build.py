
TOP = open("templates/top.html").read()
BOTTOM = open("templates/bottom.html").read()

INDEX = "index.html"
ABOUT = "about.html"
BLOG = "blog.html"
PROJECTS = "projects.html"

MY_PAGES = [INDEX, ABOUT, BLOG, PROJECTS]

def build_pg_content(page):
    return TOP + open(f"./content/{page}").read() + BOTTOM

def write_pg(page, full_content):
    open(f"./docs/{page}", "w+").write(full_content)

for pg in MY_PAGES:
    write_pg(pg, build_pg_content(pg))
