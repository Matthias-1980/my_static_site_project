import os
import shutil


def main():
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
    
    
def loopy(file_dir, file_list, to_folder):
    counter = 0
    count_to = 10
    for file in file_list:
        counter += 1
        if counter >= count_to:
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
