# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['synecure']

package_data = \
{'': ['*']}

install_requires = \
['coleo>=0.2.0,<0.3.0']

entry_points = \
{'console_scripts': ['sy = synecure.cli:entry_sy',
                     'sy-bsync = synecure.cli:entry_bsync',
                     'sy-config = synecure.cli:entry_sy_config']}

setup_kwargs = {
    'name': 'synecure',
    'version': '0.1.9',
    'description': 'File sync utility',
    'long_description': '\n# Synecure\n\nSynecure provides a command line program called `sy` that allows easy synchronization of files and directories over SSH between different machines. It is mostly a wrapper around [bsync](https://github.com/dooblem/bsync), which is itself based on the standard UNIX tool `rsync`.\n\nThis is beta software and comes with **NO GUARANTEES** that it will keep your data safe. It should not be used as backup solution.\n\n\n## Install\n\n```bash\npip install synecure\n```\n\n\n## Usage\n\n```bash\n# Sync local ~/directory with remote $HOME/directory on me@awesome.person\nsy ~/directory -r me@awesome.person\n\n# Sync current directory with the same path on me@awesome.person, port 2222\nsy -r me@awesome.person -p 2222\n\n# Register a remote under a short name\nsy-config add me me@awesome.person -p 2222\n\n# Synchronize to a named remote\nsy -r me\n\n# Synchronize the current directory to the last used remote (for that directory)\nsy\n```\n\nBy default, `sy` can take on any path within your `$HOME` and will set the corresponding path on the remote\'s `$HOME`. It is possible to change this behavior or synchronize paths outside of `$HOME` using the `sy-config path` command.\n\n`sy` with no argument will sync the current directory using the last remote for that directory (you will need to use the -r flag the first time, but not subsequently).\n\n\n## Howto\n\n\n### Ignore files\n\nAdd a `.bsync-ignore` file in the root directory to sync with a filename or glob pattern on each line, and they will be ignored. It works more or less like `.gitignore`.\n\nPutting `.bsync-ignore` files in subdirectories to ignore files in these subdirectories will unfortunately not work, so `sy ~/x` and `sy ~/x/y` may synchronize the contents of `~/x/y` differently if both directories contain different `.bsync-ignore` files, or if one has an ignore file and the other does not.\n\n\n### Customize synchronization paths\n\nTo synchronize local `/etc` to remote `/etcetera`, for named remote `desktop`:\n\n```bash\nsy-config path add desktop /etc /etcetera\n```\n\nObviously, this will only work if the remote user has the permissions to write to `/etcetera`. You can have multiple remotes for the same host with different users, if that helps.\n\nTo synchronize local `~/hello` to remote `~/bonjour`:\n\n```bash\nsy-config path add desktop ~/hello bonjour\n```\n\nDon\'t use `~` for the remote path, it will complete to the wrong thing.\n\nTo list available paths:\n\n```bash\nsy-config list\n```\n\n### Sync local directories\n\n```bash\nsy-config add dropbox ~/Dropbox\n```\n\n### Dry run\n\nUse the `-n` flag to perform a "dry run": `sy` (well, `bsync`) will report all the transfers that would occur but it will not perform them.\n\nUse `--show-plan` to get the sequence of commands that `sy` will run.\n',
    'author': 'Olivier Breuleux',
    'author_email': 'breuleux@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/breuleux/synecure',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
