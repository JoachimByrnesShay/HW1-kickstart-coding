import modules.pages

def apply_template(content, title):
    template = open("templates/base.html").read()
    return template.format(title=title, content=content)

def create_output(pages):
    for this_page in pages:
        main_content = open(this_page['filename']).read()
        title = this_page['title'].upper()
        open(this_page['output'], 'w+').write(apply_template(title=title, content=main_content))



def main():
    pages = modules.pages.PAGES
    create_output(pages)

main()
