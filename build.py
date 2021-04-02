
TOP = open("templates/top.html").read()
BOTTOM = open("templates/bottom.html").read()

INDEX = "index.html"
ABOUT = "about.html"
BLOG = "blog.html"
PROJECTS = "projects.html"

MY_PAGES = [INDEX, ABOUT, BLOG, PROJECTS]


def build_pg_content(page):
    title = page.split('.')[0].upper()
    # this variables are present in top.html
    page_variables = {'title':title, 'index_state': "", 'blog_state': "", 'about_state': "", 'projects_state':""}

    # insert active class into inline class list on link if current page
    for pg_var in page_variables:
        if title.lower() in pg_var:
            page_variables[pg_var] = 'active'

    # fill in correct values in the html code of top.html per each page, based on variables
    top_content = f"{TOP}".format(**page_variables)

    # combine all
    return top_content + open(f"./content/{page}").read() + BOTTOM

    # this particular methodology sorted out by experimenting with stackoverflow references to similar  scenarioes, but not exactly the same, at https://stackoverflow.com/questions/5952344/how-do-i-format-a-string-using-a-dictionary-in-python-3-x


def write_pg(page, full_content):
    open(f"./docs/{page}", "w+").write(full_content)

for pg in MY_PAGES:
    write_pg(pg, build_pg_content(pg))
