# wib
A simplified common interface to both ```git``` and ```hg```.

About the name [wib](https://en.wikipedia.org/wiki/Worse_is_better)

The idea is to have a unified interface to two currently popular distributed version control
systems (and suggest sensible defaults). The aim is to have a small set of commands that
cover the use cases for users who do not use version control extensively, with a set of
semantically meaningful commands.

**Everybody should be using version control regularly!**

## Installation

    $ pip install wib

If you already have wib installed, update by:

    $ pip install --upgrade wib

## Simplified view of distributed version control

There are three locations to keep in mind:

- Local file system (no versioning, view as usual using your standard viewer)
- Local repository (this is often the location that trips up users)
- Remote repository (we assume this to be somewhere like github.com, which has a nice
  interface for browsing.)

The key idea behind distributed version control is that the local repository contains everything,
and hence in theory you do not need a "server". However, for most new users, since the local
repository is hard to view and browse, it is an opaque and confusing mess. We hope to limit
the commands to a subset of the functionality to reduce confusion.

Consider the three locations listed above.
To synchronise between the local and remote repositories,
use the pair of commands ```up``` and ```down```.
The ```down``` command also updates the local file system automatically. ```up``` and ```down```
are most often used for communicating with your co-authors.
The idea behind the local repository is to be able to maintain versions even when you are
offline. Consider the situation when you are editing a particular file, and would like
to version it, this is when you ```commit``` a version it to the repository.
If you have made a mistake you can ```revert``` back to the previous committed version.

## Commands

Longer term, automated (and transparent) detection and handling of binary files
will simplify the user experience.

To learn how to use it:

    $ wib --help

Summary of commands

**up/down** - Synchronise local repository to remote repository using **up**load
  (and vice versa using **down**load)

    $ wib up
    $ wib down
    $ wib down git@github.com:myname/myrepo.git

**track/untrack** - Keep track of this file / Forget about tracking this file.

    $ wib track myfile
    $ wib untrack myfile

**commit** - Commit saved changes to the repository. Use ```--name``` to tag.

    $ wib commit "why I am saving this version"
    $ wib commit --name v0.3 "a release with cool new features"

**revert** - Revert changed files back to the version in the repository

    $ wib revert myfile

**status** - See which files are changed, checked in, and uploaded.

    $ wib status

**log** - See history

    $ wib log

**diff** - See changes that occurred since last check in.

    $ wib diff myfile

### Starting a new project/repository

We suggest to initialise a repository on a remote server, for example
[github](https://github.com/), [bitbucket](https://bitbucket.org) or
[gitlab](https://about.gitlab.com).
Then copy the URL of the repository (not the website) from the server and use **down**.

For example, to get a local copy of this repository

    $ wib down git@github.com:chengsoonong/wib.git


### Developer notes

Need to set up ```~/.pypirc```, see for example [this blog post](http://blog.irashid.com/how-to-register-you-python-package-in-pypi/).

Upload and release:

PyPI TEST

    $ python setup.py register -r testpypi
    $ python setup.py sdist upload -r testpypi

PyPI LIVE

    $ python setup.py register -r pypi
    $ python setup.py sdist upload -r pypi


### References
This package is just a wrapper on top of:

- ```git```
- ```hg```
- ```git lfs```  (TODO)
- Mercurial large files extension  (TODO)

The unified interface is motivated by:

- gitless, and paper by Santiago Perez De Rosso and Daniel Jackson, Purposes, Concepts, Misfits, and a Redesign of Git, OOPSLA, 2016
- [repo](http://source.android.com/source/using-repo.html)
- binary handling in [subversion](http://svnbook.red-bean.com/en/1.6/svn.forcvs.binary-and-trans.html)


### FAQ

- When you have a file with spaces in the name, use quotes **and** escape the spaces. E.g.
  ```wib track "test\ file\ with\ space.txt"```
