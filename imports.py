import os
import dis
import sys
from pathlib import Path

import pip
import re
from collections import defaultdict


def _load_local_env(env_path='.env'):
    env_content = dict()

    with open(env_path, 'r') as env_file:
        content = [x.strip() for x in env_file.readlines()]
        env_content = dict(line.split('=') for line in content)

    return env_content


def _list_installed_packages():
    packages = [f"{i.key}" for i in pip.get_installed_distributions()]

    return set(packages)


def _list_dependencies(packages_list):
    with_dependencies = {}
    no_dependencies = []
    for package in sorted(packages_list):
        req = pip._vendor.pkg_resources.working_set.by_key[package].requires()

        if req:
            with_dependencies[package] = [r.name for r in req]
        else:
            no_dependencies.append(package)

    return with_dependencies, no_dependencies


def _find_modules(python_file):
    with open(python_file, 'r') as s:
        statements = s.read()

        instructions = dis.get_instructions(statements)
        imports = [__ for __ in instructions if 'IMPORT' in __.opname]

        grouped = defaultdict(list)
        for instr in imports:
            grouped[instr.opname].append(instr.argval.split('.')[0])

    return grouped['IMPORT_NAME']


def _iter_modules(location):
    all_imports = []

    root_dir = Path(location)

    for python_file in root_dir.glob('**/*.py'):
        all_imports += _find_modules(str(python_file))

    return set(all_imports)


def _load_requirements(requirements_location):

    root_dir = Path(requirements_location) / 'requirements.txt'

    requirements = []
    with open(str(root_dir), 'r') as f:
        for line in f:
            requirements.append(re.match(r'^(\w+(-\w+)*)', line).group(0))

    return requirements


def _usage():
    print("Usage: python imports.py <PATH_TO_PROJECT_FOLDER>")
    print("For more information, please see README file.")
    sys.exit(1)


def check(path_dir):
    requirements = _load_requirements(path_dir)
    imported_modules = _iter_modules(path_dir)
    installed_packages = _list_installed_packages()

    config = _load_local_env()

    imported_modules.update(config['EXCLUDED_IMPORTS'])

    diff = {lib for lib in installed_packages if lib not in imported_modules}
    with_dependencies, _ = _list_dependencies(diff)
    unused_dependencies = sorted([d for d in diff if d in requirements])

    print(f'\n\nList of installed libs and your dependencies added on project'
           '\nrequirements that are not being used:\n')

    for unused_dependency in unused_dependencies:
        if with_dependencies.get(unused_dependency):
            print(f'    - {unused_dependency}')
            for dependency in with_dependencies.get(unused_dependency):
                print(f'\t - {dependency}')
        else:
            print(f'    - {unused_dependency}')

    print("\nWARNING: Uninstall libs it's at your own risk!")
    print('\nREMINDER: After uninstall libs, update your requirements file.'
          '\nFor that, use the command: `pip freeze > requirements.txt`')


if __name__ == '__main__':
    if len(sys.argv) != 2 or str(sys.argv[1]) == '--help':
        _usage()
    else:
        path_dir = str(sys.argv[1])

    check(path_dir)
