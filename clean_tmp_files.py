import glob
import os

from src.constants import PF_HOME

extentions_to_remove = ['*.osm', '*.graph', '*.html']

# Downloaded and generated files in /
for extension in extentions_to_remove:
    files_to_remove = glob.iglob(PF_HOME + extension)
    for file in files_to_remove:
        os.remove(file)

# Generated HTML files in templates
html_files_whitelist = ['base.html', 'index.html', 'content.html']
files_to_remove = glob.iglob(PF_HOME + 'src/templates/' + '*.html')
for file in files_to_remove:
    if file.split('/')[-1] not in html_files_whitelist:
        os.remove(file)
