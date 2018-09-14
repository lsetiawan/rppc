# rppc

Reproducible Python Package Creator

`rppc` provides a command line interface for creating a skeleton for a reproducible python package. The package structure here follow the standards and conventions of much of the scientific Python eco-system. With these standards and recommendations, others will be able to use your code, port your code into other projects, and collaborate with other users.

The package created tries to follow University of Washington eScience Institute [Guidelines for Reproducible and Open Science](http://uwescience.github.io/reproducible/guidelines.html).

**NOTE: This package only works for Python 3.5 and above**

## 2 Factor Authentication

Note that `git` CLI commands only accept basic authentication procedures. If you have 2FA set up on your account, you have to generate a [Personal Access Token](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/). In this case, when you are asked to enter a password in a manner such as:

`Enter the GitHub password for <user_name>`:

You have to enter your access token instead of your own password.

## How to use this package

0. Install the package from pypi

```bash
pip install rppc
```

1. Create a yaml file with you favorite editor called `package.yml`

```yaml
name: mypythonpackage
description: This is the description for the package
author:
  name: First Last
  email: myemail@example.com
dependencies:
  - pandas
  - numpy
github-id: github_username
```

2. Run `rppc init`. Note that this will ask for a license to choose. If you are unsure of which is the most appropriate license for your package, please refer to [choosealicense.com](https://choosealicense.com/)

```bash
# The optional --github argument will allow to push the newly created repository to your github
rppc init --file package.yml --github
```

## Contact the developer

The best way to contact the developer about this package is through issues. Please create an issue if you have found any bugs, or have request for an enhacement. Any other questions can also go there. Thank you!
