# helloworld_app - A Sample Python Application

A sample Python Library. It includes these components

- Project setup - setup.py, setup.cfg
- README and Makefile
- Dockerfile

The directory structure is shown here

| Files                              | Notes                                   |
| -----------------------------------| --------------------------------------- |
| .pylintrc                          | pylint config                           |
| Dockerfile                         | sample dockerfile                       |
| Makefile                           | init, build, test                       |
| README.md                          | This document                           |
| requirements.txt                   | for docker caching only, see setup.cfg  |
| setup.cfg                          | project description and dependencies    |
| setup.py                           | see setup.cfg                           |
| src/*                              | source code                             |

To start a new Python application project, clone this project.


## Docker build setup

When installing packages from Aquabyte PyPI, it needs credentials to access Github. In a development environment, we usually use an ssh private key to authenticate. This approach uses ssh forwarding from the host to Docker so that it can authenticate during docker build.


Run docker build using this command
```
DOCKER_BUILDKIT=1 docker build --ssh=default -f Dockerfile .
```

In the Dockerfile
```
# Install application including those in Aquabyte PyPI
RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts
ENV PIP_EXTRA_INDEX_URL=http://aquabyte-repository.s3-website-us-west-1.amazonaws.com/pypi/
ENV PIP_TRUSTED_HOST=aquabyte-repository.s3-website-us-west-1.amazonaws.com

RUN --mount=type=ssh pip3 -v install --no-cache-dir {packages}
```

Reference - [Makefile](Makefile) and [Dockerfile](Dockerfile).

See this article for details about [Build secrets and SSH forwarding](https://medium.com/@tonistiigi/build-secrets-and-ssh-forwarding-in-docker-18-09-ae8161d066) in Docker.



## Github workflow setup

When running Github workflow for continuous integration, it needs credentials to access Github. Note that the workflow by default has access to the current repository. But the library is referencing another repository in Aquabtye. This approach uses Github token and git URL rewriting (as oppose to adding a private SSH key to github).

Add a Github token to the repository's secret. (TODO: we should use a machine user for this)

Use this in the install dependency section in the workflow

```
    - name: Install dependencies
      # These are configuration and authentication for Aquabyte PyPI
      env:
        PIP_EXTRA_INDEX_URL: http://aquabyte-repository.s3-website-us-west-1.amazonaws.com/pypi/
        PIP_TRUSTED_HOST: aquabyte-repository.s3-website-us-west-1.amazonaws.com
        GITHUB_TOKEN: ${{ secrets.GITHUBTOKEN20200730 }}
      run: |
        git config --global url."https://${GITHUB_TOKEN}@github.com/".insteadOf "ssh://git@github.com/"
        make init
        git config --global --unset url."https://${GITHUB_TOKEN}@github.com/".insteadOf
```

Reference - [helloworld_app.yml](https://github.com/aquabyte-new/aquabyte_repository/blob/master/.github/workflows/helloworld_app.yml)


# Initial Development Setup

Run this to create the virtual environment and download data files.
```
make init
```

After this, activate your virtual environment by
```
source .venv/bin/activate
```
