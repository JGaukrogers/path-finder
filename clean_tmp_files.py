import glob
import os

from src.constants import TEMPLATES_HOME

# Generated HTML files in templates
html_files_whitelist = ['base.html', 'index.html', 'content.html']
files_to_remove = glob.iglob(str(TEMPLATES_HOME) + '/' + '*.html')
for file in files_to_remove:
    if file.split('/')[-1] not in html_files_whitelist:
        os.remove(file)
