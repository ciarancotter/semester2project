# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

sys.path.insert(0, os.path.abspath('..'))


project = 'Semester 2 Project'
copyright = '2023, Team 2'
author = 'Team 2'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

files = os.listdir("./source/")
toc_string = "Welcome to Semester 2 Project's documentation!\n==============================================\n.. toctree::\n\t:maxdepth: 2\n\t:caption: Contents:\n"
for i, file in enumerate(files):
	if file.endswith(".rst"):
		toc_string += "\n\tsource/"+file

toc_string += "\n\n"


with open('index.rst', 'r') as file:
    index_file = file.readlines()

first = index_file.index("Welcome to Semester 2 Project's documentation!\n")
last = index_file.index("Indices and tables\n")

index_file[first:last] = toc_string

with open('index.rst', 'w') as file:
    file.writelines(index_file)


