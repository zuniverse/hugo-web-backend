# Hugo Web BackEnd Interface

## Simplistic custom back end interface to a Hugo website content

This is a simplistic custom back end interface to manage a Hugo website content online or locally, as opposed to the regular cli and file system.

This is largely an editor to files containing a toml set of key-values header, and a text body.

It does not hold a wsgi interface because it is not supposed to face the public, and usage is for now limited to a few users.

### Tech stack

- Python

- Flask

- Jinja

- Bootstrap

### First setup

- Setup virtualenv as venv

### Start app in dev mode

```sh
./start_backend.sh
```

#### TODO

- Tests

- react or vuejs front-end

- remove toml package, unused

- make run-prod

- fix link to non static dir images

#### checklist

- list content directory

- list image directory

- list archetypes directory

- read a file with toml header and a text body

- edit that file

- take toml header and parse as key value fields when appropriate

- display images when editing file

- write the file with edits in the appropriate directory

- launch script to run bash shell for git and Hugo create site

- delete content files
