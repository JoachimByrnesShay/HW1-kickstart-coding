import modules.pages

def main():
    base = open('templates/base.html').read()

    pages = modules.pages.PAGES

    for this_page in pages:
        main_content = open(this_page['filename']).read()
        new_content = base.format(content=main_content) 
        open(this_page['output'], 'w+').write(new_content)

main()
