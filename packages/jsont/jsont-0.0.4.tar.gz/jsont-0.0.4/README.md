# jsont
JSON Transformer

## Build and Publish

```bash
pip install wheel twine
python setup.py sdist bdist_wheel
python -m twine upload dist/*
CURL_CA_BUNDLE="" python -m twine upload dist/*
```

```bash
pip install -e .
```