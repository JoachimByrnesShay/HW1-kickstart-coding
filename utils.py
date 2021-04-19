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



def apply_base_template(title, content, pages, link_pdir='./', css_pdir='./', base_title=''):
    """inserts page content, title, year, and page nav links into template and returns full content"""
    year = get_year()

    template_vars = {'title':title, 'pages': pages, 'content': content, 'link_pdir':link_pdir, 'year': year, 'css_pdir': css_pdir}

    template = Template(open("templates/base.html").read())
    templated_file = template.render(**template_vars)
    
    return templated_file



def create_blog_pages(pages, blogs, blog_pdir='docs/'):
    """creates individual blog pages in blog/.  blog_pdir adjusts relative links based on parent dir of blogs dir.  current site is hosted from docs/ on github pages.
    as implemented, for blog pages there are no links in nav set to active state""" 
    # pass blog_base.html as content to base.html in apply_base_template() function
    blog_base = open('templates/blog_base.html').read()
    
    for blog in blogs:
        blog_vars = {'blog_item_title': blog['title'], 'blog_item_date': blog['date'], 'blog_item_content': blog['content']}
        blog_content_template = Template(apply_base_template(title=blog['title'], content=blog_base, pages=pages, link_pdir='../', css_pdir='../'))
        file_name = open(blog_pdir + blog['filename'], 'w+')
        file_name.write(blog_content_template.render(blog_vars))



def markdown_to_html(file_contents):
    """converts markdown content to html"""
    exts = ['meta', 'extra']
    markdowned = markdown.Markdown(extensions=exts)

    html = markdowned.convert(file_contents)
    meta_data = markdowned.Meta
    return (html, meta_data)



def has_markdown_page(page):
    """utility function to check if page being tested in any_accessory_content() function has a matching user editable md file in content/mainpage_markdown"""
    md_content_folder = get_file_paths('content/mainpage_markdown/', 'md')
    for filepath in md_content_folder:
        fp = get_file_name(filepath)
        if page in fp:
           return True
    return False



def any_accessory_content(page, blogs):
    """ returns dict with blog index data if page is 'Blog' and any user edited markdown content if there is a page in /content/mainpage_markdown
    which matches page in /content/mainpages """
    blog_index = ''
    md_contents = ''
    md_name = get_file_name_only(page['filename']) + '_md'

    if page['title'] == 'Blog':
        blog_index = create_blog_index(blogs)
    
    if has_markdown_page(md_name):
        location = f'content/mainpage_markdown/{md_name}' + '.md'
        md_contents, meta = markdown_to_html(open(location).read())

    return {'blog_index': blog_index, 'new_md_content': md_contents}



def create_main_pages(pages, blogs):
    """ creates main site pages in docs/ dynamically using main markdown file contents in content/mainpages """
    for this_page in pages:
        
        file_contents = f"""{open(this_page['filename'], 'r').read()}"""
        file_to_html, meta = markdown_to_html(file_contents)

        """ adds simple page specific title to base_title for main content pages, distinct from base_title below but in final page build they will be concatenated if BOTH exist """
        #print(meta)
        if 'title' in meta:
            title = meta['title']
        else:
            title = this_page['title']
  
        main_content = Template(file_to_html).render(any_accessory_content(this_page, blogs))
        # base_title is a thematic general title for main pages which is present as meta data in mainpages in content/mainpages
        # it is handled separately and not combined in python code with title as jinja2 for loop is used in the base template on title specifically (and not base_title)
        base_title = meta['base_title'][0]

        template_vars = {'title': title, 'base_title': base_title, 'pages': pages, 'content': main_content}
       
        full_content = apply_base_template(**template_vars)
        open(this_page['output'], 'w+').write(full_content)



def create_blog_index(blogs):
    """ creates content for docs/blog.html consisting of indexing of blog pages by title and 30 character lead.
    uses dynamically created blog post data from user created markdown files in content/blogs"""
    item_template = Template(open('templates/blog_index_item.html').read())
    content = ''
    
    for blog_item in blogs:
        title = blog_item['title']
        snippet = blog_item['content'][:30] + '...'
        filename = './' + blog_item['filename']
        content += item_template.render(title=title, filename=filename, snippet=snippet)
    
    return content



def create_blogs():
    """ returns a list of dictionaries of blog content for processing, one dictionary of data for each full blog entry created from markdown files in content/blogs"""
    blog_files = get_file_paths('content/blogs', 'md')
    blogs = []
    mdown = markdown.Markdown(extensions=["meta"])

    for blog_file in blog_files:
        blogs.append(blog_item_constructor(blog_file))

    return blogs



def blog_item_constructor(blog_location):
    """ returns a blog_item in the form of a dictionary including filename, date, title, and full content in html format;  used in create_blogs()"""
    blog_item = {}
    blog_content = open(blog_location, 'r').read()
    blog_item['filename'] = create_blog_filepath(blog_location)

    html, meta = markdown_to_html(blog_content)
    blog_item['date'] = meta['date'][0]
    blog_item['title'] = meta['title'][0]
    blog_item['content'] = html
   
    return blog_item



def create_output(main_pages, blog_pages):
    """creates output files in docs/ for content in each content/*html page after applying templating with all templating info including links and title"""
    create_blog_pages(pages=main_pages, blogs=blog_pages)
    create_main_pages(pages=main_pages, blogs=blog_pages)



def get_file_paths(folder, type):
    """ utility function to return list of files of type in specified folder"""
    return glob.glob(f'{folder}/*{type}')



def get_file_name(file_path):
    """  utility function to return filename with extension """
    return os.path.basename(file_path)



def get_file_name_only(file_path):
    """ utility function to return filename only, no extension"""
    file_name = get_file_name(file_path)
    name_only, extension = os.path.splitext(file_name)
    return name_only



def create_blog_filepath(file_path):
    """ utility function used in """
    return 'blog/' + get_file_name_only(file_path) + '.html'


    
def get_title(file_name):
    """ utility function to construct page title from filename for main pages"""
    title, extension = os.path.splitext(file_name)
    
    if title.lower() == 'index':
        return 'Home'
    else:
        return title.capitalize()



def create_content_file_dict(file_path):
    """ returns dict for markdown mainfiles found in /content/mainpage, with filename, intended html output location, and title """
    file_dict = {}
    file_dict['filename'] = file_path
    file_name = get_file_name(file_path)

    file_dict['output'] = f"docs/{get_file_name_only(file_path)}.html"
    file_dict['title'] = get_title(file_name)
    return file_dict



def create_content_list():
    """ returns list of all dictionaries created with create_content_file_dict(file_path)"""
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



# a group of command line-usage related functions are below
def functional_args():
    """ called in manage.py, returns boolean indicating if there is an addtional command line argument used with python3 manage.py """ 
    """ this is used as a utility with build_requested() and new_requested(), so that sys.argv[1] doesn't result in an error if there is no argv[1]"""
    return len(sys.argv) > 1



def build_requested():
    """ checks if build function is requested at command line """
    return functional_args() and sys.argv[1] == 'build'



def new_requested():
    """ checks if new file function is requested at command line """
    return functional_args() and sys.argv[1] == 'new'


 
def new_content():
    """ returns new content template, which is used when new file is requested at command line usage"""
    return open("templates/new_content.html").read()



def new_file():
    """ additional instruction when user requestes new file creation at command line usage """
    print("""A blank markdown file will be created at /content/mainpage_markdown with the filename = filename + '_md.md'. 
    This file is for user edits of the basic central content desired for filename.html.
    User can insert markdown in the '_md.md' file and then rebuild.
    *************************************************************************************************\n""")

    file_name = input("Please enter name of new file.  After edits to markdown if any and after build, result will be filename.html\n::").strip()
    # make sure that if user enters char in filename that is not alpha, replace char with '_'
    sanitized = [c if c.isalpha() else '_' for c in file_name]
    
    file_name = ('').join(sanitized)
    content = new_content()    
    # basic new file structure, using new_content.html template 
    open(f"content/mainpages/{file_name}.md", "w+").write(content)
    # user editable markdown file to match 
    open(f"content/mainpage_markdown/{file_name}_md.md", "w+").write(new_file_starter_text(file_name))   

    print(f"\nFile with name {file_name}.md created in content/mainpages, with matching user editable {file_name}_md.md at /content/mainpage_markdown\n")



def new_file_starter_text(file_name):
    """ returns starter content for the blank user editable markdown file in content/mainpage_markdown which will be created with matching new requested filename in content/mainpages 
    adds title in meta data in the markdown file for ease of use in dynamically constructing the file data when the main pages are built"""
    return f"title:{file_name}\n  \n\r##### This is new markdown content\n  \n\rAnd this is new markdown content\n \n\rFile can be edited in /content/mainpage_markdown/"



def print_command_line_help():
    """ when either no argument is passed to python3 manage.py or when the string passed is not 'build' or 'new', print help for command line usage when running python manage.py """
    instruction = """
    Usage:
        Rebuild site:     python manage.py build
        Create new main site page:  python manage.py new
        """
    print(instruction)



# main is conditionally called from manage.py, based upon user command line usage
def main():
    pages = create_content_list()
    blogs = create_blogs()
    create_output(pages, blogs)
  


  