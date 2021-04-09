import datetime
import modules.pages

def get_year():
    year = datetime.date.today().year
    return year

def apply_template(title, links, content):
    year = get_year()
    template = open("templates/base.html").read()
    template_vars = {'title':title, 'links':links, 'content':content, 'year': year}
    return template.format(**template_vars)

def create_links(pages, page):
    list_links = ''
    li_with_link = '<li class="nav-item"><a class="nav-link text-white {active_class}" href="{link_href}">{link_title}</a></li>'
    for this_page in pages:
        if this_page['title'] == page['title']:
            active_class = "active"
        else:
            active_class = ""
        link_href = this_page['output'].split('/')[1]
        link_title = this_page['title'].upper()
        list_links += li_with_link.format(active_class=active_class, link_href=link_href, link_title=link_title)
    return list_links

def create_output(pages):
    for this_page in pages:
        main_content = open(this_page['filename']).read()
        links = create_links(pages, this_page)
        title = this_page['title'].upper()
        open(this_page['output'], 'w+').write(apply_template(title=title, links=links, content=main_content))


def main():
    pages = modules.pages.PAGES
    create_output(pages)

if __name__ == '__main__':
    main()