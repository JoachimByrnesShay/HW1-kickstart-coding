"""import of modules.pages (modules/pages.py) allows usage of the PAGES variable: a list of dictionaries, one per each main 
site page.  datetime is imported from the standardd library to be utilized inside the get_year() function"""
import datetime
import modules.pages

def get_year():
    """return current year using datetime module"""
    year = datetime.date.today().year
    return year

def apply_template(title, links, content):
    """inserts page content, title, page nav links, current year into template and returns full content"""
    year = get_year()
    template = open("templates/base.html").read()
    template_vars = {'title':title, 'links':links, 'content':content, 'year': year}
    # using string format() with {} placeholders in html instead of replace() with {{}}
    return template.format(**template_vars)

def get_link_classes(this_page, compared_page):
    """called inside of create_li_links().  creates a class list to be applied to each of all nav links
    created per each site page"""

    link_classes = ['nav-link', 'text-white']
    # append the .active class to avove default classes list if the link is a link for the current page
    if this_page['title'] == compared_page['title']:
        link_classes.append("active")
    # return this list as a space separated string to be inserted in the templating
    return (' ').join(link_classes)

def create_li_links(pages, curr_page):
    """creates set of html li > a links to be inserted into placeholder via templatig inside of ul.navbar-nav 
    with appropriate href, link text, and adds .active class to inline class list for link where required"""
    list_links = ''
    li_with_link = '<li class="nav-item"><a class="{link_classes}" href="{link_href}">{link_title}</a></li>'
    for page in pages:
        link_classes = get_link_classes(curr_page, page)
        link_href = page['output'].split('/')[1]
        link_title = page['title'].upper()
        list_links += li_with_link.format(link_classes=link_classes, link_href=link_href, link_title=link_title)
    return list_links

def create_output(pages):
    """creates output files in docs/ for content in each content/*html page after applying templating with links and title"""
    for this_page in pages:
        main_content = open(this_page['filename']).read()
        links = create_li_links(pages, this_page)
        title = this_page['title'].upper()
        open(this_page['output'], 'w+').write(apply_template(title=title, links=links, content=main_content))

def main():
    # PAGES is a list in modules/pages.py
    pages = modules.pages.PAGES
    create_output(pages)
   
if __name__ == '__main__':
    main()
