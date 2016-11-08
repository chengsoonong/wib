# wib
A common interface to both ```git``` and ```hg```.

About the name [wib](https://en.wikipedia.org/wiki/Worse_is_better)

## Installation

    $ pip install .

## Commands

The idea would be to have a unified interface to two currently popular distributed version control
systems (and suggest sensible defaults).
Furthermore, automated (and transparent) detection and handling of binary files
will simplify the user experience.

To use it:

    $ wib --help

Summary of commands

* **init** - Start a new repository (defaults to git).
  For copying from a remote repository, use **download**.

  ```wib init myrepo```

* **track/untrack** - Keep track of this file / Forget about tracking this file.

  ```wib track myfile```

  ```wib untrack myfile```

* **checkin** - Commit saved changes to the repository. Use ```--name``` to tag.

  ```wib checkin "why I am saving this version"```

  ```wib checkin --name v0.3 "a release with cool new features"```

* **checkout** - Revert changed files back to the version in the repository

  ```wib checkout myfile```

* **upload/download** - Synchronise local repository to remote repository (and vice versa)

  ```wib upload```

  ```wib download```

  ```wib download git@github.com:myname/myrepo.git```

* **status** - See which files are changed, checked in, and uploaded.

  ```wib status```

* **log** - See history

  ```wib log```

* **diff** - See changes that occurred since last check in.

  ```wib diff myfile```

### References
This package is just a wrapper on top of:
* ```git```
* ```hg```  (TODO)
* ```git lfs```  (TODO)
* Mercurial large files extension  (TODO)

The unified interface is motivated by:
* [gitless.com](gitless.com), and paper by Santiago Perez De Rosso and Daniel Jackson, Purposes, Concepts, Misfits, and a Redesign of Git, OOPSLA, 2016
* [repo](http://source.android.com/source/using-repo.html)
* binary handling in [subversion]( \url{http://svnbook.red-bean.com/en/1.6/svn.forcvs.binary-and-trans.html)
