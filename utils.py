import datetime
import glob
import os
import sys
import markdown
from jinja2 import Template

def get_year():
    """return current year using datetime module"""
    year = datetime.date.today().year
    return year


def apply_base_template(title, content, pages, link_pdir='./', css_pdir='./'):
    """inserts page content, title, year, and page nav links into template and returns full content"""
    year = get_year()
    template = Template(open("templates/base.html").read())
    template_vars = {'title':title, 'pages': pages, 'content': content, 'link_pdir':link_pdir, 'year': year, 'css_pdir': css_pdir}
    templated_file = template.render(**template_vars)
    return templated_file


def create_blog_pages(pages, blogs, blog_pdir='docs/'):
    """creates individual blog pages in blog/.  blog_pdir adjusts relative links based on parent dir of blogs dir.  current site is hosted from docs/ on github pages.
    as implemented, for blog pages there are no links in nav set to active state""" 
    # pass blog_base.html as content to base.html in apply_base_template() function
    blog_base = open('templates/blog_base.html').read()
    
    for blog in blogs:
        blog_content_template = Template(apply_base_template(title=blog['title'], content=blog_base,pages=pages, link_pdir='../', css_pdir='../'))
        file_name = open(blog_pdir + blog['filename'], 'w+')

        blog_vars = {'blog_item_title': blog['title'], 'blog_item_date': blog['date'], 'blog_item_content': blog['content']}
        file_name.write(blog_content_template.render(blog_vars))


def markdown_to_html(file_contents):
    exts = ['meta', 'extra']
    markdowned = markdown.Markdown(extensions=exts)

    html = markdowned.convert(file_contents)
    meta_data = markdowned.Meta
    return (html, meta_data)

def has_markdown_page(page):
    md_content_folder = get_file_paths('content/mainpage_markdown/', 'md')
    for filepath in md_content_folder:
        fp = get_file_name(filepath)
        if page in fp:
           return True
    return False

def create_main_pages(pages, blogs):
    """ creates main site pages in docs/ using PAGES list in modules/pages.py"""
    for this_page in pages:

        md_name = get_file_name_only(this_page['filename']) + '_md'
        file_contents = f"""{open(this_page['filename'], 'r').read()}"""
        file_to_html, meta = markdown_to_html(file_contents)

        title = this_page['title'] + ': ' + meta['base_title'][0]
        blog_index = ''
        md_contents = ''
        if this_page['title'] == 'Blog':
            blog_index = create_blog_index(blogs)
        
        if has_markdown_page(md_name):
            location = f'content/mainpage_markdown/{md_name}' + '.md'
            md_contents, meta = markdown_to_html(open(location).read())
    
        main_content = Template(file_to_html).render(blog_index=blog_index, new_md_content=md_contents)
        template_vars = {'title': title, 'pages': pages, 'content': main_content}
        full_content = apply_base_template(**template_vars)
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
    
    return content


def create_blogs():
    blog_files = get_file_paths('content/blogs', 'md')

    blogs = []
    mdown = markdown.Markdown(extensions=["meta"])
    for blog in blog_files:
        blog_item = {}
        blog_content = open(blog, 'r').read()
        blog_item['filename'] = create_blog_filepath(blog)
        html, meta = markdown_to_html(blog_content)
        blog_item['date'] = meta['date'][0]
        blog_item['title'] = meta['title'][0]
        blog_item['content'] = html
        blogs.append(blog_item)
    return blogs

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


def create_blog_filepath(file_path):
    return 'blog/' + get_file_name_only(file_path) + '.html'
    
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
    return file_dict


def create_content_list():
    file_paths = get_file_paths('content/mainpages', 'md')
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

   

# command line-usage related functions
def functional_args():
    return len(sys.argv) > 1


def build_requested():
    return functional_args() and sys.argv[1] == 'build'


def new_requested():
    return functional_args() and sys.argv[1] == 'new'

 
def new_content():
    return open("templates/new_content.html").read()


def new_file_starter_text():
    return "##### This is new markdown content\n  \n\rAnd this is new markdown content\n \n\rFile can be edited in /content/mainpage_markdown/"


def new_file():
    print("""A blank markdown file will be created at /content/mainpage_markdown with the filename = filename + '_md.md'. 
    This file is for user edits of the basic central content desired for filename.html.
    User can insert markdown in the '_md.md' file and then rebuild.
    *************************************************************************************************\n""")

    file_name = input("Please enter name of new file.  After edits to markdown if any and after build, result will be filename.html\n::").strip()
    sanitized = [c if c.isalpha() else '_' for c in file_name]
    
    file_name = ('').join(sanitized)
    content = new_content()    
    open(f"content/mainpage_markdown/{file_name}_md.md", "w+").write(new_file_starter_text())   
    open(f"content/mainpages/{file_name}.md", "w+").write(content)


def print_command_line_help():
    instruction = """
    Usage:
        Rebuild site:     python manage.py build
        Create new main site page:  python manage.py new
        """
    print(instruction)



def main():
    pages = create_content_list()
    blogs = create_blogs()
    create_output(pages, blogs)
  