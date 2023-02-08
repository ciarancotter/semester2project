import os
files = os.listdir("./source/")
toc_string = "Welcome to Semester 2 Project's documentation!\n==============================================\n.. toctree::\n\t:maxdepth: 2\n\t:caption: Contents:\n\n"
for i, file in enumerate(files):
	if file.endswith(".rst"):
		toc_string += "\n\t"+file

toc_string += "\n\n"


with open('index.rst', 'r') as file:
    index_file = file.readlines()

first = index_file.index("Welcome to Semester 2 Project's documentation!\n")
last = index_file.index("Indices and tables\n")

index_file[first-1:last] = toc_string

with open('index.rst', 'w') as file:
    file.writelines(index_file)
