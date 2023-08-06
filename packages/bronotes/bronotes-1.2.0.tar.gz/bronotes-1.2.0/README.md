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

## Todo

  * Add something to keep folder in sync with git

## Installation and usage

```bash
$ pip install bronotes

$ bnote -h 
usage: bnote [-h] {add,rm,list,edit,mv,set,completions} ...

positional arguments:
  {add,rm,list,edit,mv,set,completions}
                        Bronote actions.
    add                 Add a note or directory.
    rm                  Delete a note or directory.
    list                Show the notes structure as a tree.
    edit                Edit a note.
    mv                  Move a note or directory.
    set                 Set config options.
    completions         Generate zsh autocompletions.

optional arguments:
  -h, --help            show this help message and exit

$ bnote -h
usage: bnote [-h] {add,rm,list,edit,mv,set} ...
```

On first command a folder to be used is asked.

### Completions

For now there's no built-in completions.
ZSH completions can be generated so you can place them where needed:
```bash
$ bnote completions | tee /home/jwiersma/.oh-my-zsh/completions/_BRONOTES
```
