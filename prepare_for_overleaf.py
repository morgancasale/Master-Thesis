import os
import shutil
#from math import ceil

source_folder = os.getcwd()
out_folder = "../overleaf"

dir_to_delete = ["__pycache__", ".git", "svg-inkscape"]
file_ext_to_keep = [".tex", ".bib", ".cls", ".svg", ".png", ".jpg"] # ".png"
str_of_file_to_delete = ["Example", "Template"]

def on_rmtree_error(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.
    
    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    import stat
    # Is the error an access error?
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

def crawl_and_delete(start_folder):
    for root, dirs, files in os.walk(start_folder):
        for file in files:
            cond = any(str in file for str in str_of_file_to_delete) # Remove files that contain the string in str_of_file_to_delete
            cond |= not any(file.endswith(ext) for ext in file_ext_to_keep) # Keep files that end with the extension in file_ext_to_keep
            if cond:
                os.remove(os.path.join(root, file))
            
        for dir in dirs:
            if dir in dir_to_delete:
                shutil.rmtree(os.path.join(root, dir), onerror=on_rmtree_error)
            else:
                crawl_and_delete(os.path.join(root, dir))

# Copy the current folder to the Overleaf folder
if os.path.exists(out_folder):
    shutil.rmtree(out_folder, onerror=on_rmtree_error)
shutil.copytree(source_folder, out_folder, dirs_exist_ok=True)

# Remove all files that are not needed in the Overleaf project
crawl_and_delete(out_folder)

# num_of_files = sum([len(files) for r, d, files in os.walk(out_folder)])
# num_of_folders = round_up(num_of_files/40)

# if(num_of_folders > 1):
#     for i in range(1, num_of_folders):
#         shutil.copytree(out_folder, out_folder + str(i), dirs_exist_ok=True)