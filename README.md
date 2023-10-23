# mbedmgr

v0.0.1 doesn't work yet. I'm just reserving the package name...

## Deploy to PyPI

```
python3 -m venv deploy
source deploy/bin/activate
python3 -m pip install -r deploy-requirements.txt
python3 -m build
python3 -m twine upload dist/*
deactivate
```
