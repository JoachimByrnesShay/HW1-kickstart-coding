"""import of modules.pages (modules/pages.py) allows usage of the PAGES variable: a list of dictionaries, one per each main 
site page.  datetime is imported from the standardd library to be utilized inside the get_year() function"""
import datetime
import glob
import os
import sys
import modules.blog_posts
import codecs as co
import markdown 
import mistune
import jinja2
from jinja2 import Template
# import markdown.extensions.md_in_html
# import markdown.extensions.fenced_code
# import markdown.extensions.extra


def get_year():
    """return current year using datetime module"""
    year = datetime.date.today().year
    return year

def apply_base_template(title, content, pages, link_pdir='./', css_pdir='./'):
    """inserts page content, title, and page nav links into template and returns full content"""
    year = get_year()
    template = Template(open("templates/base.html").read())
    template_vars = {'title':title, 'pages': pages, 'content': content, 'link_pdir':link_pdir, 'year': year, 'css_pdir': css_pdir}
    templated_file = template.render(**template_vars)
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


def md_to_html(file):
    exts = ['markdown.extensions.meta', 'markdown.extensions.extra']
    #'markdown.extensions.fenced_code','markdown.extensions.md_in_html','markdown.extensions.tables','markdown.extensions.toc', 'markdown.extensions.smarty'] 
    #file = open(file_path, 'r').read()
    #exts = ['md_in_html', 'meta', 'extra', 'nl2br']
    #ret = markdown.markdown(file, extensions=exts)
    ret = markdown.Markdown(extensions=exts).convert(file)
    #ret = markdown.markdown(file, extensions=exts)
    #ret = markdown.markdown(file, extensions=exts)
    #template = Template(open('templates/base.html').read())
    #final = template.render({'content':ret})
    # print(ret)
    return ret

def create_main_pages(pages, blogs):
    """ creates main site pages in docs/ using PAGES list in modules/pages.py"""
    for this_page in pages:
        file = f"""{open(this_page['filename'], 'r').read()}"""
        file_to_html = md_to_html(file)
        # print(file_to_html)
        # break
        #main_content = Template(open(this_page['filename']).read())
        blog_index = ''
        if this_page['title'] == 'Blog':
            blog_index = create_blog_index(blogs)
            
        main_content = Template(file_to_html).render(blog_index)

        # print(main_content)
        # break
        title = this_page['title']
        template_vars = {'title': title, 'pages': pages, 'content': main_content}
        # if this_page['title'] == 'Blog':
        #     template_vars['blog_index'] = create_blog_index(blogs)
           # main_content = main_content.render(create_blog_index(blogs))
        # else:
        #     main_content = main_content.render()
        full_content = apply_base_template(**template_vars)

        open(this_page['output'], 'w+').write(full_content)


# def create_main_pages(pages, blogs):
#     """ creates main site pages in docs/ using PAGES list in modules/pages.py"""
#     for this_page in pages:
#         main_content = Template(open(this_page['filename']).read())
#         if this_page['title'] == 'Blog':
#             main_content = main_content.render(create_blog_index(blogs))
#         else:
#             main_content = main_content.render()
#         title = this_page['title']
#         full_content = apply_base_template(title=title, pages=pages, content=main_content)
#         open(this_page['output'], 'w+').write(full_content)

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
    #print({'blog_index': content})
    return {'blog_index': content}


def create_output(main_pages, blog_pages):
    """creates output files in docs/ for content in each content/*html page after applying templating with links and title"""
    create_blog_pages(pages=main_pages, blogs=blog_pages)
    create_main_pages(pages=main_pages, blogs=blog_pages)


def get_file_paths(folder, type):
    return glob.glob(f'{folder}/*{type}')

def get_file_name(file_path):
    return os.path.basename(file_path)

def get_file_name_only(file_path):
    file_name = get_file_name(file_path)
    name_only, extension = os.path.splitext(file_name)
    return name_only

def get_title(file_name):
    title,extension = os.path.splitext(file_name)
    if title.lower() == 'index':
        return 'Home'
    else:
        return title.capitalize()

def create_content_file_dict(file_path):
    file_dict = {}
    file_dict['filename'] = file_path
    file_name = get_file_name(file_path)

    file_dict['output'] = f"docs/{get_file_name_only(file_path)}.html"
    file_dict['title'] = get_title(file_name)
    print(file_dict)
    return file_dict

def create_content_list():
    file_paths = get_file_paths('content', 'md')
    files = []
    index_path = ''
    for file_path in file_paths:
        if 'index' in file_path:
            index_path = file_path
        else:
            files.append(create_content_file_dict(file_path))
    # moves index page dictionary to front of list so that it will be the first iterated value when 
    # links are created, i.e. "HOME" will be the first link in nav
    files.insert(0, create_content_file_dict(index_path))
    return files
   
def functional_args():
    return len(sys.argv) > 1

def build_requested():
    return functional_args() and sys.argv[1] == 'build'

def new_requested():
    return functional_args() and sys.argv[1] == 'new'
 
def new_content():
    return open("templates/new_content.html").read()

def new_file():
    file_name = input("Enter name of html content file to create: ").strip()
    sanitized = [c if c.isalpha() else '_' for c in file_name]
    file_name = ('').join(sanitized)
    content = Template(new_content())
    open(f"content/{file_name}.html", "w+").write(content.render())

def print_command_line_help():
    instruction = """
    Usage:
        Rebuild site:     python manage.py build
        Create new page:  python manage.py new
        """
    print(instruction)

# def md_to_html(file_path):
#     #exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite','markdown.extensions.tables','markdown.extensions.toc']
#     exts = ['markdown.extensions.meta']#, 'markdown.extensions.extra','markdown.extensions.tables','markdown.extensions.toc'] 
#     g2 = open("content/index.md", 'r').read()
#     #fr = jinja2.Markup(g2)
   
#     ret = markdown.markdown(g2)
#     template = Template(open('templates/base.html').read())

#     final = template.render({'content':ret})
#     print(final)
# def md_to_html(file_path):
#     exts = ['markdown.extensions.meta']#, 'markdown.extensions.extra','markdown.extensions.tables','markdown.extensions.toc'] 
#     file = open(file_path, 'r').read()
#     ret = markdown.markdown(file)
#     template = Template(open('templates/base.html').read())
#     final = template.render({'content':ret})
#     print(final)
    


def main():
    # PAGES is a list in modules/pages.py, BLOG_POSTS is list in modules/blog_posts.py
    pages = create_content_list()
    blogs = modules.blog_posts.BLOG_POSTS
    # md_to_html()
    create_output(pages, blogs)
  

