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

### Start app in dev mode

```sh
make run-dev
```

### Run tests

```sh
make test
```

#### TODO

- More tests

- react or vuejs front-end

- remove toml package, unused

- make run-prod

- fix link to non static dir images
