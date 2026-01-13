This README contains instructions for creating and running the documentation website locally using **mkdocs.yml**.  
It is a **temporary document**, as is the mkdocs YAML file.

## 0. Create a virtual environment

```bash
python3 -m venv documentation_env
```

## 1. Activate your virtual environment

```bash
source documentation_env/bin/activate
```

## 2. Install required libraries

```bash
pip install mkdocs mkdocs-material mkdocs-redirects
```

## 3. Run the site locally

Open your terminal in the directory containing `mkdocs.yml`, then run:

```bash
mkdocs serve
```

The site will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## References

- [MkDocs Documentation](https://www.mkdocs.org/)
- [MkDocs Material Theme](https://squidfunk.github.io/mkdocs-material/)

## Quick run

```bash
python3 -m venv documentation_env
source documentation_env/bin/activate
pip install mkdocs mkdocs-material
mkdocs serve
```