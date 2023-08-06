# Bronotes

Basically a wrapper to access notes in a directory on your system anywhere from the commandline.
Still in development. Not much configuration possible yet.

Functionality so far:
  * Create a note directory on your system on first start
  * Add new notes
  * Remove notes
  * Move notes and directories around
  * Edit notes with your $EDITOR
  * List notes dir in a tree

Todo:
  * Add -r flag where necessary, eg. file creation and rm on non empty folders
  * Stop forcing my chosen notes directory on the user
  * Add some intial configuration questions and possibly allow a user config yaml somewhere
  * Add some kind of 'set' action to manipulate the user config yml
  * Add something to keep folder in sync with git
  * ZSH completions
