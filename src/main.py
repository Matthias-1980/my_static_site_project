import os
import shutil

from blocks import *
from htmlnode import *

def main():
    copy_static_to_public() 
        
    dir_path_content = "./content/"
    template_path = "./template.html"
    dest_dir_path = "./public/"

    print("Generating pages ..")
    generate_pages_recursive(dir_path_content, template_path, dest_dir_path)

#Note:
#   Flaw: that the content folder in the root of the project contains only
#  directories and files with the extention "md" which is markdown files.
#  (the function will convert ANY file inside of the content folder directory
#  tree into an index.html file (which is a flaw)).
#Assumptions: 
#   That the dir_path_content parameter points to a file to convert.
#   That the dest_dir_path parameter points to a location to write a file.
#   That the template_path parameter points to a template file to use in 
#  a converstion of a file into an index dot html file.
#Expected behaviour:
#   Recursively takes a file from, and down, the content folder's directory 
#  tree, and turns it into a dot html file in the destination folder. 
#  The recursion part is that the content
#  folder's directory tree is used in the destination folder when the html
#  files are generated.
#Encapsulation change:
#   Creates index dot html files in the destination folder and 
#  its sub directories.
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    cur_content_dir = os.listdir(dir_path_content)
    html_file_name = "index.html"
    
    for file in cur_content_dir:
        if os.path.isfile((dir_path_content + file)):
            print(f"{dir_path_content + file} -> {dest_dir_path + html_file_name}")
            from_path = dir_path_content + file
            
            open_file = open(from_path)
            index_md = open_file.read()
            open_file.close()

            open_file2 = open(template_path)
            template_html = open_file2.read()
            open_file2.close()
    
            title = extract_title(from_path)
   
            index_md_to_textnodes = text_to_textnodes(index_md)
            new_string = ""
            for textnode in index_md_to_textnodes:
                new_string += (text_node_to_html_node(textnode)).to_html()

            markdown_html_node = markdown_to_html_node(new_string)
            html = markdown_html_node.to_html()
            
            template_html = template_html.replace("{{ Title }}", title)    
            template_html = template_html.replace("{{ Content }}", html)
    
            if os.path.exists(dest_dir_path):
                open_file3 = open((dest_dir_path + html_file_name), 'w', encoding="utf-8")
                open_file3.write(template_html)
                open_file3.close()
            else:
                raise Exception("path to write html file does not exist, exiting.")



        elif os.path.isdir((dir_path_content + file)):
            new_content_dir = dir_path_content + file + '/'
            new_dest_path = dest_dir_path + file + '/'
            if not os.path.exists(new_dest_path):
                os.mkdir(new_dest_path)

            generate_pages_recursive(new_content_dir, template_path, new_dest_path)

    
    


#Note: Function is not used. Can be deleted.
#Assumptions:
#  that the parameter "from_path" points to a file containing text.
#  that the parameter "template_path" points to an html file that 
# will be copied and the copy gets altered.
#  that the parameter "dest_path" points to a folder to write the html to.
#Expected behaviour:
#  the "from_path" file gets converted into html, and the template_path file
# gets altered with that new html inserted into it. The new html gets written
# to the dest_path folder with the name defined by html_file_name variable.
#Encapsulation change:
# index.html gets written to the folder defined by "dest_path" parameter.
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
   
    index_md_to_textnodes = text_to_textnodes(index_md)
    new_string = ""
    for textnode in index_md_to_textnodes:
        new_string += (text_node_to_html_node(textnode)).to_html()

    markdown_html_node = markdown_to_html_node(new_string)
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
    content_exists = False
    static_exists = False
    src_exists = False

    public_path = "./public/"
    static_path = "./static/"

    dir_list = os.listdir(".")
    for item in dir_list:
        if item == "content":
            content_exists = True
        if item == "static":
            static_exists = True
        if item == "src":
            src_exists = True

    if not content_exists and not static_exists and not src_exists:
        raise Exception("program ran in wrong directory, exiting.")

    if os.path.exists(public_path):
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
#  This function copies the content of one directory and its sub directories
# into another directory. In short it copies the directory structure and files.
#Note:
#  change the name.
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
