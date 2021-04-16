"""import of modules.pages (modules/pages.py) allows usage of the PAGES variable: a list of dictionaries, one per each main 
site page.  datetime is imported from the standardd library to be utilized inside the get_year() function"""
import datetime
import glob
import os
import modules.blog_posts
from jinja2 import Template

def get_year():
    """return current year using datetime module"""
    year = datetime.date.today().year
    return year

def apply_base_template(title, content, pages, link_pdir='./', css_pdir='./'):
    """inserts page content, title, and page nav links into template and returns full content"""
    year = get_year()
    template = Template(open("templates/base.html").read())
    template_vars = {'title':title, 'pages': pages, 'content': content, 'link_pdir':link_pdir, 'year': year, 'css_pdir': css_pdir}
    templated_file = template.render(template_vars)
    return templated_file

def create_blog_pages(pages, blogs, blog_pdir='docs/'):
    """creates individual blog pages in blog/.  blog_dir adjusts relative links based on parent dir of blogs dir.  current site is hosted from docs/ on github pages.
    as implemented, for blog pages there are no links in nav set to active state, pasing None as curr_page in create_li_links() below insures that"""
    #links = create_li_links(pages, curr_page=None, links_pdir='../')
    # pass blog_base.html as content to base.html in apply_base_template() function
    blog_base = open('templates/blog_base.html').read()
    blog_content_template = Template(apply_base_template(title="Blog Item", content=blog_base, pages=pages, link_pdir='../', css_pdir='../'))
    for blog in blogs:
        file_name = open(blog_pdir + blog['filename'], 'w+')
        blog_vars = {'blog_item_title': blog['title'], 'blog_item_date': blog['date'], 'blog_item_content': blog['content']}
        file_name.write(blog_content_template.render(blog_vars))

def create_main_pages(pages, blogs):
    """ creates main site pages in docs/ using PAGES list in modules/pages.py"""
    for this_page in pages:
        main_content = Template(open(this_page['filename']).read())
        if this_page['title'] == 'Blog':
            main_content = main_content.render(create_blog_index(blogs))
        else:
            main_content = main_content.render()
        title = this_page['title']
        full_content = apply_base_template(title=title, pages=pages, content=main_content)
        open(this_page['output'], 'w+').write(full_content)

def create_blog_index(blogs):
    """ creates content for docs/blog.html consisting of indexing of blog pages by title and 30 character lead.
    uses BLOG_POSTS in modules/blog_posts.py"""
    #item_template = open('templates/blog_index_item.html').read()
    item_template = Template(open('templates/blog_index_item.html').read())
    content = ''
    for blog_item in blogs:
        title = blog_item['title']
        snippet = blog_item['content'][:30] + '...'
        filename = './' + blog_item['filename']
        content += item_template.render(title=title, filename=filename, snippet=snippet)
    return {'blog_index': content}

def create_output(main_pages, blog_pages):
    """creates output files in docs/ for content in each content/*html page after applying templating with links and title"""
    create_blog_pages(pages=main_pages, blogs=blog_pages)
    create_main_pages(pages=main_pages, blogs=blog_pages)


def get_file_paths(folder):
    return glob.glob(f'{folder}/*html')

def get_file_name(file_path):
    return os.path.basename(file_path)

def get_title(file_name):
    title,extension = os.path.splitext(file_name)
    if title.lower() == 'index':
        return 'Home'
    else:
        return title.capitalize()

def create_content_file_dict(file_path):
    file_dict = {}
    file_dict['filename'] = file_path
    file_name = get_file_name(file_path.replace('md', 'html'))
    file_dict['output'] = f"docs/{file_name}"
    file_dict['title'] = get_title(file_name)
    return file_dict

def create_content_list():
    file_paths = get_file_paths('content')
    files = []
    for file_path in file_paths:
        if 'index' in file_path:
            index_path = file_path
        else:
            files.append(create_content_file_dict(file_path))
    # moves index page dictionary to front of list so that it will be the first iterated value when 
    # links are created, i.e. "HOME" will be the first link in nav
    files.insert(0, create_content_file_dict(index_path))
    return files
   
def main():
    # PAGES is a list in modules/pages.py, BLOG_POSTS is list in modules/blog_posts.py
    pages = create_content_list()
    blogs = modules.blog_posts.BLOG_POSTS
    create_output(pages, blogs)
  

