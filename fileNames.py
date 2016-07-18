import os

def rename_files():
    # (1) get the files from a folder
    file_list = os.listdir("/home/zrtho/Downloads/prank")
    #print(file_list)
    saved_path = os.getcwd()
    #print ( " CWD is " + saved_path)
    os.chdir("/home/zrtho/Downloads/prank")
    # (2) rename files
    for file_name in file_list:
        os.rename(file_name, file_name.translate(None, "0123456789"))   
    os.chdir(saved_path)
rename_files()
