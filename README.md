Synctron
========

Synctron is a simple home directory backup tool built on top of rsync.

[![Build Status: GitHub Actions](https://github.com/rovellipaolo/synctron/actions/workflows/ci.yml/badge.svg)](https://github.com/rovellipaolo/synctron/actions)
[![Test Coverage: Coveralls](https://coveralls.io/repos/github/rovellipaolo/synctron/badge.svg)](https://coveralls.io/github/rovellipaolo/synctron)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

![Synctron](docs/images/synctron.gif "Screencast of Synctron")



## Overview

Synctron uses `rsync` to back up home directories.

Note that, at present, this is not designed to be a generic rsync frontend but just to serve a specific use case.



## Build

The first step is cloning the Synctron repository, or downloading its source code.

```
$ git clone https://github.com/rovellipaolo/synctron
$ cd synctron
```

To execute Synctron, you need `Python 3.8` or higher installed.
Just launch the following commands, which will install all the needed Python dependencies and add a `synctron` symlink to `/usr/local/bin/`.

```
$ make build
$ make install
$ synctron --help
```



## Test

Once you've configured it (see the _"Installation"_ section), to run the tests and checkstyle manually launch the following command:
```shell
$ make test
$ make checkstyle
```

You can also run the tests with coverage by launching the following command:
```shell
$ make test-coverage
```

And/or configure the checkstyle to run automatically at every git commit by launching the following command:
```shell
$ make install-githooks
```



## Usage

The following is an example of running Synctron against a sample directory.
```
$ synctron -s tests/data/home/user/ -d tests/data/backup/user/

? Select the source subdirectories to be backed up:  (<up>, <down> to move, <space> to select, <a> to toggle, <i> to invert)
  ○ .hidden.txt
  ● new.txt
  ● NEW
  ● MOVED
  ○ .hidden
  ○ excluded
Output: sending incremental file list
*deleting   moved.txt
*deleting   deleted.txt
.d..t...... ./
>f+++++++++ new.txt
cd+++++++++ MOVED/
>f+++++++++ MOVED/moved.txt
cd+++++++++ NEW/
>f+++++++++ NEW/inner.txt

sent 278 bytes  received 64 bytes  684.00 bytes/sec
total size is 16  speedup is 0.05 (DRY RUN)

? Are you sure to continue?  Yes
Output: sending incremental file list
*deleting   moved.txt
*deleting   deleted.txt
.d..t...... ./
>f+++++++++ new.txt
cd+++++++++ MOVED/
>f+++++++++ MOVED/moved.txt
cd+++++++++ NEW/
>f+++++++++ NEW/inner.txt

sent 414 bytes  received 112 bytes  1.05K bytes/sec
total size is 16  speedup is 0.03
```



## Licence

Synctron is licensed under the GNU General Public License v3.0 (http://www.gnu.org/licenses/gpl-3.0.html).

