""" imported as module inside of build.py.   PAGES is the pages list containing the
data for each page to be generated for the site.
"""

PAGES = [
    {
        'filename': 'content/index.html',
        'output': 'docs/index.html',
        'title': 'Home'
    },
    {
        'filename': 'content/about.html',
        'output': 'docs/about.html',
        'title': 'About'
    },
    {
        'filename': 'content/blog.html',
        'output': 'docs/blog.html',
        'title': 'Blog'

    },
    {
        'filename': 'content/projects.html',
        'output': 'docs/projects.html',
        'title': 'Projects'
    },
]
