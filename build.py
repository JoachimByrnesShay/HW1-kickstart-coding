import modules.pages

def main():
    top = open("templates/top.html").read()
    bottom = open("templates/bottom.html").read()

    pages = modules.pages.PAGES

    for this_page in pages:
        main_content = open(this_page['filename']).read()
        new_content = top + main_content + bottom
        open(this_page['output'], 'w+').write(new_content)

main()
