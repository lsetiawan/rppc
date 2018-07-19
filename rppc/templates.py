
def readme_template(package_name, package_description):
    return f"""# {package_name}\n---\n
{package_description}\n
This package has been automatically generated, 
please edit this file for better description."""

def dev_dependencies(additional_text):
    return f"""# Testing packages
pytest

# Linting packages
flake8
flake8-builtins
flake8-comprehensions
flake8-import-order
flake8-mutable
flake8-print
flake8-quotes

# Debugging packages
ipython
ipykernel

{additional_text}
"""

def setup_template(package_name, package_description, author_name, author_email, license_detail):
    return f"""# This setup.py was autogenerated, please edit for further details
import os
from codecs import open

from setuptools import find_packages, setup

import versioneer

here = os.path.abspath(os.path.dirname(__file__))

# Dependencies.
with open('requirements.txt') as f:
    requirements = f.readlines()
install_requires = [t.strip() for t in requirements]

with open(os.path.join(here, 'README'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='{package_name}',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='{package_description}',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    author='{author_name}',
    author_email='{author_name}',
    maintainer='{author_name}',
    maintainer_email='{author_email}',
    python_requires='>=3',
    license='{license_detail['spdx_id']}',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords=[],
    include_package_data=True,
    packages=find_packages(),
    install_requires=install_requires,
)
"""

def setup_cfg_template(package_name):
    return f"""[metadata]
# This includes the license file in the wheel.
license_file = LICENSE

[bdist_wheel]
# This flag says to generate wheels that support both Python 2 and Python
# 3. If your code will not run unchanged on both Python 2 and 3, you will
# need to generate separate wheels for each Python version that you
# support. Removing this line (or setting universal to 0) will prevent
# bdist_wheel from trying to make a universal wheel. For more see:
# https://packaging.python.org/tutorials/distributing-packages/#wheels
universal=0

[versioneer]
VCS = git
style = pep440
versionfile_source = {package_name}/_version.py
versionfile_build = {package_name}/_version.py
tag_prefix = v
parentdir_prefix = {package_name}-
"""

def manifest(additional_text):
    return f"""include README.md
include *.txt

{additional_text}
"""

def tests_example():
    return """# -*- coding: utf-8 -*-

def test_hello_world():
    text = 'Hello World'
    assert text == 'Hello World'
"""

def travis_template(package_name):
    return f"""language: python

sudo: false

dist: trusty

matrix:
  fast_finish: true
  include:
  - python: 3.6
    env: TEST_TARGET=default
  - python: 3.6
    env: TEST_TARGET=coding_standards
  allow_failures:
  - python: 3.6
    env: TEST_TARGET=coding_standards

before_install:
  - |
    URL="http://bit.ly/miniconda"
    echo ""
    if [ ! -f $HOME/miniconda/bin/conda ] ; then
      echo "Fresh miniconda installation."
      wget $URL -O miniconda.sh
      rm -rf $HOME/miniconda
      bash miniconda.sh -b -p $HOME/miniconda
    fi
  - export PATH="$HOME/miniconda/bin:$PATH"
  - conda update conda --yes
  - conda config --set show_channel_urls true
  - conda config --add channels conda-forge --force
  - conda create --yes -n TEST python=$TRAVIS_PYTHON_VERSION --file requirements.txt --file requirements-dev.txt
  - source activate TEST

# Test source distribution.
install:
  - python setup.py sdist && version=$(python setup.py --version) && pushd dist  && pip install {package_name}-${{version}}.tar.gz && popd

script:
  - if [[ $TEST_TARGET == 'default' ]]; then
      cp -r tests /tmp && cd /tmp ;
      pytest -vv tests ;
    fi
    
  - if [[ $TEST_TARGET == 'coding_standards' ]]; then
      flake8 --max-line-length=105 {package_name} ;
    fi
"""

