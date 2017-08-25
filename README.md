# Imports

__WARNING:__ Remove packages listed by this helper it's at your own risk

## Usage

> NOTE: Before start, it's expected that there is a `requirements.txt` file on the project root folder and your virtualenv is active as well.

Download `imports.py` and use the command below passing the path to the root folder of project that'll be checked. After that, the helper will list all the possible packages that aren't being used in your project:

```python
python imports.py PATH_TO_PROJECT_FOLDER
```

Here a small example:

![Input](https://raw.githubusercontent.com/joaopcanario/imports/master/media/input.png)

the output:

![Output](https://raw.githubusercontent.com/joaopcanario/imports/master/media/output.png)


After this, I suggest the use of [pip-autoremove package](https://github.com/invl/pip-autoremove) to uninstall the wrong entries listed.
