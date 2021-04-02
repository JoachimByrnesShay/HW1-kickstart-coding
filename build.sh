top=./templates/top.html
bottom=./templates/bottom.html


cat $top content/index.html $bottom > docs/index.html
cat $top content/about.html $bottom > docs/about.html
cat $top content/blog.html $bottom > docs/blog.html
cat $top content/projects.html $bottom > docs/projects.html