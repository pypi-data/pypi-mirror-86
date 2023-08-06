# Bronotes

Basically a wrapper to access notes in a directory on your system anywhere from the commandline.
Still in development but the basic functionality is there.

Functionality so far:
  * Create a note directory on your system on first start
  * Add new notes
  * Remove notes
  * Move notes and directories around
  * Edit notes with your $EDITOR
  * List notes dir in a tree
  * Generate autocompletions for zsh
  * Sync with git
  * Show and edit search for a note if no path to an existing file is given

## Todo

  * Create a git subcommand that basically just wraps the git cmd utility for more user control.
  * A lot of new tests need to be done, big chances ugly non-caught errors are present.
    * Especially git-related

## Installation

```bash
$ pip install bronotes
```

On first command a folder to be used is asked.

### Completions

For now there's no built-in completions.
ZSH completions can be generated so you can place them where needed:
```bash
$ bnote completions | tee ~/.oh-my-zsh/completions/_BRONOTES
```

## Usage

```bash
$ bnote -h
usage: bnote [-h] action ...

positional arguments:
  action       Bronote actions.
    add        Add a note or directory.
    rm         Delete a note or directory.
    list       Show the notes structure as a tree.
    edit       Edit a note.
    mv         Move a note or directory.
    set        Set config options.
    completions
               Generate zsh autocompletions.
    show       Show the contents of a note.
    sync       Sync the notes dir with git.

optional arguments:
  -h, --help   show this help message and exit
```

Subcommands have their own help pages.
When using the edit or show subcommand, it falls back on the -s option if the path to your note is not valid.

### Git

You can use the sync command to keep a repo in sync with git. Using basic pull/push on master.
If you want to have more control simply don't use this.
If the repo isn't a git repo yet you will be asked to initialize an empty one and set up remotes.
When quit halfway through this process it's probably better to either start over or just fix it manually.

Autosyncing is possible, but will do so after every edit or add action. So figure out if you want that yourself.
