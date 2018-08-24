import os
import requests
import warnings

GITHUB_API_URL = 'https://api.github.com'

def file_writer(folder, filename, content):
    with open(os.path.join(folder, filename), 'w') as f:
        f.write(content)

def folder_creator(base_dir, folder_name):
    new_folder = os.path.join(base_dir, folder_name)
    if not os.path.exists(new_folder):
        os.mkdir(new_folder)
    
    return new_folder


def check_user(github_username):
    """Checks how many public repos user have"""
    users_url = '/'.join([GITHUB_API_URL, 'users', github_username])
    req = requests.get(users_url)
    if req.status_code == 200:
        user_public_repo = req.json()['public_repos']
        # How many pages to crawl through 100 per page
        return int(user_public_repo / 100) + 1
    else:
        return Exception(req.text)


def request_repos(*args):
    page, github_username, package_name, url = args
    req = requests.get(url, params={
        'per_page': 100,
        'page': page
    })
    if req.status_code == 200:
        filtered_repo = list(filter(lambda x: x['full_name'] == f'{github_username}/{package_name}', req.json()))
        if len(filtered_repo) > 0:
            return True
        return False
    else:
        return Exception(req.text)


def check_repos(max_page, *args):
    start_page = 0
    while start_page < max_page:
        start_page += 1
        if request_repos(start_page, *args):
            yield True


def check_package(package_name, github_username):
    url = '/'.join([GITHUB_API_URL, 'users', github_username, 'repos'])
    pages = check_user(github_username)
    rep = check_repos(pages, github_username, package_name, url)
    for r in rep:
        if r:
            warnings.warn(f'{package_name} exists on {github_username} Github account!')
            return r

def create_repo(package_name, package_description, github_auth):
    try:
        github_username = github_auth['auth'].username
        package_exists = check_package(package_name, github_username)
        if not package_exists:
            payload = {
                'name': package_name,
                'description': package_description,
                'homepage': '/'.join(['https://github.com', github_username, package_name]),
                'private': False,
                'has_issues': True,
                'has_projects': True,
                'has_wiki': True,
            }
            post_url = '/'.join([GITHUB_API_URL, 'user', 'repos'])
            req = requests.post(post_url, json=payload, auth=github_auth['auth'], headers=github_auth['headers'])
            if req.status_code in [201, 200]:
                return req.json()['clone_url']
            else:
                return Exception(req.text)
    except Exception as e:
        print(e)
