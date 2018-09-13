# rppc

Reproducible Python Package Creator

`rppc` provides a command line interface for creating a skeleton for a reproducible python package. The package structure here follow the standards and conventions of much of the scientific Python eco-system. With these standards and recommendations, others will be able to use your code, port your code into other projects, and collaborate with other users.

The package created tries to follow University of Washington eScience Institute [Guidelines for Reproducible and Open Science](http://uwescience.github.io/reproducible/guidelines.html).

## 2 Factor Authentication

Note that `git` CLI commands only accept basic authentication procedures. If you have 2FA set up on your account, you have to generate a [Personal Access Token](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/). In this case, when you are asked to enter a password in a manner such as:

`Enter the GitHub password for <user_name>`:

You have to enter your access token instead of your own password.
