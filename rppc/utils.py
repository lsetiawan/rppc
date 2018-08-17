import os
import requests

GITHUB_API_URL = 'https://api.github.com'

def file_writer(folder, filename, content):
    with open(os.path.join(folder, filename), 'w') as f:
        f.write(content)

def folder_creator(base_dir, folder_name):
    new_folder = os.path.join(base_dir, folder_name)
    if not os.path.exists(new_folder):
        os.mkdir(new_folder)
    
    return new_folder

def check_package(package_name, github_username):
    # CURRENTLY DOESN'T GET ALL REPOS IN USER DIRECTORY!
    # TODO: Fix me!
    url = '/'.join([GITHUB_API_URL, 'users', f'{github_username}', 'repos'])
    req = requests.get(url)

    if req.status_code == 200:
        filtered_repo = list(filter(lambda x: x['full_name'] == f'{github_username}/{package_name}', req.json()))
        try:
            html_url = filtered_repo[0]['html_url']
        except Exception as e:
            print(e)
    else:
        return Exception(req.text)
