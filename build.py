"""import of modules.pages (modules/pages.py) allows usage of the PAGES variable: a list of dictionaries, one per each main 
site page.  datetime is imported from the standardd library to be utilized inside the get_year() function"""
import datetime
import modules.pages
import modules.blog_posts

def get_year():
    """return current year using datetime module"""
    year = datetime.date.today().year
    return year

def apply_base_template(title, links, content, css_pdir='./'):
    """inserts page content, title, page nav links, current year into template and returns full content
    adjusts css href  with css_pdir prepended if needed for relative links based on parent directory of css folder, as needed from inside docs/blogs"""
    year = get_year()
    template = open("templates/base.html").read()
    template_vars = {'title':title, 'links':links, 'content':content, 'year': year, 'css_pdir': css_pdir}
    # using string format() with {} placeholders in html instead of replace() with {{}}
    return template.format(**template_vars)

def get_link_classes(this_page, compared_page):
    """called inside of create_li_links().  creates a class list to be applied to each of all nav links
    created per each site page"""
    link_classes = ['nav-link', 'text-white']
    # append the .active class to avove default classes list if the link is a link for the current page
    if this_page and this_page['title'] == compared_page['title']:
        link_classes.append("active")
    # return this list as a space separated string to be inserted in the templating
    return (' ').join(link_classes)

def create_li_links(pages, curr_page, links_pdir='./'):
    """creates set of html li > a links to be inserted into placeholder via templatig inside of ul.navbar-nav 
    with appropriate href, link text, and adds .active class to inline class list for link where required.
    links_pdir variable allows to adjust path relative to parent directory (such as for links in blog/1.html)"""
    list_links = ''
    li_with_link = '<li class="nav-item"><a class="{link_classes}" href="{link_href}">{link_title}</a></li>'
    for page in pages:
        link_classes = get_link_classes(curr_page, page)
        link_href = links_pdir + page['output'].split('/')[1]
        link_title = page['title'].upper()
        list_links += li_with_link.format(link_classes=link_classes, link_href=link_href, link_title=link_title)
    return list_links

def create_blog_pages(pages, blogs, blog_pdir='docs/'):
    """creates individual blog pages in blog/.  blog_dir adjusts relative links based on parent dir of blogs dir.  current site is hosted from docs/ on github pages.
    as implemented, for blog pages there are no links in nav set to active state, pasing None as curr_page in create_li_links() below insures that"""
    links = create_li_links(pages, curr_page=None, links_pdir='../')
    # pass blog_base.html as content to base.html in apply_base_template() function
    blog_base = open('templates/blog_base.html').read()
    blog_content_template = apply_base_template(title="Blog Item", links=links, content=blog_base, css_pdir='../')
    for blog in blogs:
        file_name = open(blog_pdir + blog['filename'], 'w+')
        blog_vars = {'blog_item_title': blog['title'], 'blog_item_date': blog['date'], 'blog_item_content': blog['content']}
        file_name.write(blog_content_template.format(**blog_vars))

def create_main_pages(pages, blogs):
    """ creates main site pages in docs/ using PAGES list in modules/pages.py"""
    for this_page in pages:
        main_content = open(this_page['filename']).read()
        if this_page['title'] == 'Blog':
            main_content = main_content.format(**create_blog_index(blogs))
        links = create_li_links(pages, this_page)
        title = this_page['title'].upper()
        open(this_page['output'], 'w+').write(apply_base_template(title=title, links=links, content=main_content))

def create_blog_index(blogs):
    """ creates content for docs/blog.html consisting of indexing of blog pages by title and 30 character lead.
    uses BLOG_POSTS in modules/blog_posts.py"""
    item_template = open('templates/blog_index_item.html').read()
    content = ''
    for blog_item in blogs:
        title = blog_item['title']
        snippet = blog_item['content'][:30] + '...'
        filename = blog_item['filename']
        content += item_template.format(title=title, filename=filename, snippet=snippet)
    return {'blog_index': content}

def create_output(main_pages, blog_pages):
    """creates output files in docs/ for content in each content/*html page after applying templating with links and title"""
    create_blog_pages(pages=main_pages, blogs=blog_pages)
    create_main_pages(pages=main_pages, blogs=blog_pages)
   
def main():
    # PAGES is a list in modules/pages.py, BLOG_POSTS is list in modules/blog_posts.py
    pages = modules.pages.PAGES
    blogs = modules.blog_posts.BLOG_POSTS
    create_output(pages, blogs)

if __name__ == '__main__':
    main()
