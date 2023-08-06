# Python project bootstrap

Basic scaffolding for python3 CLI projects

## Init

Init the project:
```
$ make init project=myapp
```
This automatically rename references to `pyboot`. Check `setup.cfg` to adjust descriptions.

Reset the versioning:
```
$ rm -rf .git
$ git init
$ git add .
$ git commit -m "Init project from bootstraper"
```

## Test

```
$ pip install .[dev]
$ tox
```

## Release

```
$ python setup.py sdist bdist_wheel
$ twine upload dist/*
```

## Todo

* Waiting for a editable standardization before moving to PEP517 (See: https://discuss.python.org/t/specification-of-editable-installation/1564/40)
