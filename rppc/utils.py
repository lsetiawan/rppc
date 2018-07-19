import os

def file_writer(folder, filename, content):
    with open(os.path.join(folder, filename), 'w') as f:
        f.write(content)

def folder_creator(base_dir, folder_name):
    new_folder = os.path.join(base_dir, folder_name)
    if not os.path.exists(new_folder):
        os.mkdir(new_folder)
    
    return new_folder

