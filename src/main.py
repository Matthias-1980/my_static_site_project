import os
import shutil

from blocks import *
from htmlnode import *

def main():
    # copy_static_to_public() 
    
    content_file_path = "../content/index.md"
        
    template_file_path = "../template.html"
    dest_path = "../public/"
    generate_page(content_file_path, template_file_path, dest_path)


def generate_page(from_path, template_path, dest_path):
    html_file_name = "index.html"
    print(f"Generating page from {from_path} to {dest_path}")
    print(f"using {template_path}")

    open_file = open(from_path)
    index_md = open_file.read()
    open_file.close()

    open_file2 = open(template_path)
    template_html = open_file2.read()
    open_file2.close()
    
    title = extract_title(from_path)
    
    markdown_html_node = markdown_to_html_node(index_md)
    html = markdown_html_node.to_html()
    
    template_html = template_html.replace("{{ Title }}", title)    
    template_html = template_html.replace("{{ Content }}", html)
    
    if os.path.exists(dest_path):
        open_file3 = open((dest_path + html_file_name), 'w', encoding="utf-8")
        open_file3.write(template_html)
        open_file3.close()
    else:
        raise Exception("path to write html file does not exist, exiting.")


#Assumptions:
#  That the parameter "markdown" points to a file containing text.
#  That some where in the file is a title that starts with an "# " and
# ends with a '\n'
#Expected behaviour:
#  Opens a file pointed at by the parameter "markdown".
#  Looks for a title in that file .. .
#  Returns the title from that file.
#Encapsulation change:
#  None.
def extract_title(markdown):
    open_file = open(markdown)
    file_content = open_file.read()
    open_file.close()

    first_flag = False
    second_flag = False
    ret_title = ""
    for cha in file_content:
        if cha == '#' and not first_flag:
            first_flag = True
            continue
        if cha == ' ' and first_flag and not second_flag:
            second_flag = True
            continue
        else:
            first_flag = False

        if second_flag:
            if cha == '\n':
                break
            ret_title += cha
    
    return ret_title


#Assumptions:
#   That the folder public, within the root of the project, exists.
#Expected behaviour:
#  Copies the content of one folder to another: static to public folder.
#Encapsulation change:
#   Deletes the folder public that is in the root of the project.
#   Creates an empty folder called public in the root of the project.
#   Populates that public folder with the content of the static folder.
def copy_static_to_public():
    public_exists = False
    static_exists = False
    src_exists = False

    public_path = "./../public/"
    static_path = "./../static/"

    sub_dir_list = os.listdir("..")
    for item in sub_dir_list:
        if item == "public":
            public_exists = True
        if item == "static":
            static_exists = True
        if item == "src":
            src_exists = True

    if not public_exists and not static_exists and not src_exists:
        raise Exception("one or more of the folders does not exist, exiting.")

    cwd = os.getcwd()
    cwd = cwd.split('/')

    cur_working_dir = cwd.pop()
    if cur_working_dir != "src":
        raise Exception("program ran in wrong directory")

    parent_dir = cwd.pop()
    if parent_dir != "my_static_site_project":
        raise Exception("program ran in wrong directory")

    shutil.rmtree(public_path)
    os.mkdir(public_path)

    dir_list = os.listdir(static_path)
    loopy(static_path, dir_list, public_path)


#Assuptions:
#  That the function copy_static_to_public has done rigorous testing
# to make sure that this function, loopy, is ran in the correct environment.
#Expected behaviour:
#  Loopy contains a semi-fail switch that is a counter. That counter tries
# to prevent Loopy from running a mock by preventing it from moving more than
# 10 files or directories.
#Encapsulation change:
def loopy(file_dir, file_list, to_folder):
    counter = 0
    count_to = 10
    for file in file_list:
        counter += 1
        if counter >= count_to:
            print("the function loopy has reached its fail safe counter.")
            break
        if os.path.isfile((file_dir + file)):
            shutil.copy((file_dir + file), to_folder)
        elif os.path.isdir((file_dir + file)):
            new_from_folder = file_dir + file + '/'
            new_file_list = os.listdir(new_from_folder)
            new_to_folder = to_folder + file + '/'
            os.mkdir(new_to_folder)
            loopy(new_from_folder, new_file_list, new_to_folder) 

main()
