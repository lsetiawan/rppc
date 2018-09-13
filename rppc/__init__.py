import os
import shutil
import sys
import re
import datetime
import argparse

import requests
from munch import Munch

import yaml

from doctr.local import GitHub_login

from .utils import (
    folder_creator,
    file_writer,
    create_repo,
    run_shell_command
)

from .templates import (
    tests_example,
    readme_template,
    dev_dependencies,
    setup_template,
    setup_cfg_template,
    manifest,
    travis_template,
    flake8_template,
    contributing_md,
    authors_md
)

__author__ = 'Landung Setiawan'
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

BASE_DIR = os.path.abspath(os.path.curdir)
LICENSES = requests.get('https://api.github.com/licenses').json()
DEFAULT_CREDENTIAL_LOC = '~/.git-credentials'

def create_package_dir(package_name):
    return folder_creator(BASE_DIR, package_name)

def create_tests(package_dir):
    tests_dir = folder_creator(package_dir, 'tests')
    file_writer(tests_dir, '__init__.py', '')
    file_writer(tests_dir, 'test_example.py', tests_example())

def create_travis(package_dir, package_name):
    file_writer(package_dir, '.travis.yml', travis_template(package_name))

def create_flake8(package_dir, package_name):
    file_writer(package_dir, '.flake8', flake8_template(package_name))

def create_authors(package_dir, author_name, author_email):
    file_writer(package_dir, 'AUTHORS.md', authors_md(author_name, author_email))

def create_contributing(package_dir, package_name, github_username):
    file_writer(package_dir, 'CONTRIBUTING.md', contributing_md(package_name, github_username))

def create_notebooks_folder(package_dir):
    notebooks_dir = folder_creator(package_dir, 'notebooks')
    file_writer(notebooks_dir, '.gitkeep', '')

def create_license(selection, package_dir, author_name):
    lic = LICENSES[selection]
    license_detail = requests.get(lic['url']).json()
    license_text = license_detail['body']
    year = datetime.datetime.now().year

    license_text = license_text.replace('[year]', f'{year}')
    license_text = license_text.replace('[fullname]', f'{author_name}')

    file_writer(package_dir, 'LICENSE', license_text)

    return license_detail

def create_setup(package_dir, package_name, package_description,
                author_name, author_email, license_detail):
    file_writer(package_dir,
                'setup.py',
                setup_template(
                    package_name,
                    package_description,
                    author_name,
                    author_email,
                    license_detail)
                )
    file_writer(package_dir, 'setup.cfg', setup_cfg_template(package_name))

def create_readme(package_dir, package_name, package_description):
    readme_text = readme_template(package_name, package_description)
    file_writer(package_dir, 'README.md', readme_text)

def create_requirements(package_dir, dependencies, **kwargs):
    cleaned_dependencies = list(map(lambda d: d.strip(' '), dependencies.split(',')))
    file_writer(package_dir, 'requirements.txt', '\n'.join(cleaned_dependencies))
    additional_text = kwargs.get('additional_text', '')
    file_writer(package_dir, 'requirements-dev.txt', dev_dependencies(additional_text))

def create_manifest(package_dir, **kwargs):
    additional_text = kwargs.get('additional_text', '')
    file_writer(package_dir, 'MANIFEST.in', manifest(additional_text))

def use_versioneer():
    run_shell_command(['versioneer', 'install'])

def create_sphinx_docs(package_dir, package_name,
                       package_description, author_name,
                       **kwargs):
    docs_dir = folder_creator(package_dir, 'docs')
    cmd = ['sphinx-quickstart', '--sep',
           f'--project={package_name}', f'--author="{author_name}"',
           '--ext-autodoc', '--ext-viewcode',
           '--extensions=sphinx.ext.napoleon', '--extensions=nbsphinx',
           '--makefile', '--dot=_',
           '--release=""', '-v', '""',
           '--suffix=.rst', '--language=en',
           '--master=index', '-q', '--no-batchfile', f'{docs_dir}']
    run_shell_command(cmd)

def init_package_code_dir(package_dir, package_name, **kwargs):
    package_code_dir = folder_creator(package_dir, package_name)

    author_name = kwargs.get('author_name', '')
    init_text = f"""__author__ = '{author_name}'"""
    file_writer(package_code_dir, '__init__.py', init_text)

def init_git(package_dir):
    os.chdir(package_dir)
    run_shell_command(['git', 'init'])

    gitignore = requests.get('https://raw.githubusercontent.com/github/gitignore/master/Python.gitignore').text
    gitignore_text = f"""{gitignore}\n# ipynb\n.ipynb_checkpoints\n"""
    file_writer(package_dir, '.gitignore', gitignore_text)

def get_user_input(info_file=None):
    args = dict()
    if info_file:
        ymldct = yaml.load(info_file)
        args['package_name'] = ymldct['name']
        args['package_description'] = ymldct['description']
        args['author_name'] = ymldct['author']['name']
        args['author_email'] = ymldct['author']['email']
        args['dependencies'] = ','.join(ymldct['dependencies'])
        args['gh_username'] = ymldct.get('github-id', 'someuser')
    else:
        args['package_name'] = input('Enter package name: ')
        args['package_description'] = input('Enter initial package description: ')
        args['author_name'] = input('Primary Author Name: ')
        args['author_email'] = input('Primary Author Email: ')
        args['dependencies'] = input('Package dependencies (comma separated): ')
        args['gh_username'] = input('What is your github username: ')

    license_list = list(map(lambda x: f"{x[0]}: {x[1]['name']}", enumerate(LICENSES)))
    license_list_str = '\n'.join(license_list)
    args['license'] = int(input(f"{license_list_str}\nSelect number: "))

    return Munch(**args)

def set_local_repo_credentials(gh_auth, credential_loc=None):
    if gh_auth is None or gh_auth.get('auth') is None:
        print('Authentication required. Please provide username and password!')
        exit(1)

    if credential_loc is None:
        credential_loc = DEFAULT_CREDENTIAL_LOC

    auth = gh_auth['auth']

    credential_url = f'https://{auth.username}:{auth.password}@github.com'

    print('Setting local repo credentials...')
    run_shell_command(['echo', f'"{credential_url}"', '>', credential_loc])
    run_shell_command(['git', 'config', 'credential.helper', f'"store --file {credential_loc}"'])

def unset_local_repo_credentials(credential_loc=None):
    if credential_loc is None:
        credential_loc = DEFAULT_CREDENTIAL_LOC

    print('Unsetting local repo credentials...')
    run_shell_command(['git', 'config', '--unset', 'credential.helper', f'"store --file {credential_loc}"'])
    run_shell_command(['rm', '-rf', credential_loc])

def init(info_file=None, init_github=False):
    # Get user inputs
    inputs = get_user_input(info_file)
    git_url = None
    gh_auth = None
    if init_github:
        # Get github login
        gh_auth = GitHub_login()
        github_username = gh_auth['auth'].username
        # Initialize repo
        git_url = create_repo(inputs.package_name, inputs.package_description, gh_auth)
    else:
        github_username = inputs.gh_username
    # Create package directory
    package_dir = create_package_dir(inputs.package_name)
    # Initialize git repo
    init_git(package_dir)
    # Create package code directory
    init_package_code_dir(package_dir, inputs.package_name, author_name=inputs.author_name)
    # Create notebooks directory
    create_notebooks_folder(package_dir)
    # Create license
    license_detail = create_license(inputs.license, package_dir, inputs.author_name)
    # Create flake8
    create_flake8(package_dir, inputs.package_name)
    # Create authors
    create_authors(package_dir, inputs.author_name, inputs.author_email)
    # Create contributing
    create_contributing(package_dir, inputs.package_name, github_username)
    # Create readme
    create_readme(package_dir, inputs.package_name, inputs.package_description)
    # Create requirements
    create_requirements(package_dir, inputs.dependencies)
    # Create setup.py
    create_setup(package_dir,
                inputs.package_name,
                inputs.package_description,
                inputs.author_name,
                inputs.author_email,
                license_detail)
    # Create Manifest.in
    create_manifest(package_dir)
    # Create tests
    create_tests(package_dir)
    # Create travis
    create_travis(package_dir, inputs.package_name)
    # Use Versioneer
    use_versioneer()
    # Create initial sphinx docs
    create_sphinx_docs(package_dir,
                       inputs.package_name,
                       inputs.package_description,
                       inputs.author_name)
    # Commit changes
    run_shell_command(['git', 'add', '.'])
    run_shell_command(['git', 'commit', '-m', '"Initialize package repository"'])

    # Push to github
    if git_url and gh_auth:
        set_local_repo_credentials(gh_auth)
        run_shell_command(['git', 'remote', 'add', 'origin', git_url])
        run_shell_command(['git', 'push', '-u', 'origin', 'master'])
        unset_local_repo_credentials()
