import modules.pages

def apply_template(content):
    template = open("templates/base.html").read()
    return template.format(content=content)

def create_output(pages):
    for this_page in pages:
        main_content = open(this_page['filename']).read()
        open(this_page['output'], 'w+').write(apply_template(main_content))



def main():
    pages = modules.pages.PAGES
    create_output(pages)
    
main()
