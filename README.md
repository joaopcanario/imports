# Imports

__WARNING:__ Remove packages listed by this helper it's all uppon to you

## Usage

First, clone this repo and go the dowloaded folder:

```console
git clone https://github.com/joaopcanario/imports.git
cd imports
```

After this, with virtualenv of the project active, you can use the command below passing the path to project that'll be checked and the helper will list all the possible packages that aren't used in your project:

```python
python imports.py PATH_TO_PROJECT_FOLDER
```

Here a small example:



After this, I suggest the use of [pip-autoremove package](https://github.com/invl/pip-autoremove) to uninstall the wrong entries listed.
