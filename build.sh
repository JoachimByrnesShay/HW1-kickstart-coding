top=./templates/top.html
bottom=./templates/bottom.html
index=index.html
about=about.html
blog=blog.html
projects=projects.html

cat $top content/$index $bottom > docs/$index
cat $top content/$about $bottom > docs/$about
