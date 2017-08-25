from collections import defaultdict
from pathlib import Path

import sys
import dis
import pip
import re

EXCLUDED_IMPORTS = ['pip', 'setuptools']


def _list_installed_packages():
    packages = ["{}".format(i.key) for i in pip.get_installed_distributions()]

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


if __name__ == '__main__':
    if len (sys.argv) != 2:
        print("Usage: python imports.py <PATH_TO_PROJECT_FOLDER>")
        print("For more information, please see README")
        sys.exit(1)


    pathdir = str(sys.argv[1])

    requirements = _load_requirements(pathdir)
    imported_modules = _iter_modules(pathdir)
    installed_packages = _list_installed_packages()

    imported_modules.update(EXCLUDED_IMPORTS)

    diff = {lib for lib in installed_packages if lib not in imported_modules}
    with_dependencies, _ = _list_dependencies(diff)
    unused_dependencies = sorted([d for d in diff if d in requirements])

    print(f'\n\nList of installed libraries (and your dependencies) that are a\
\npotentially unused dependency that are added on requirements of \n\
the project {pathdir}:\n')

    for u in unused_dependencies:
        if with_dependencies.get(u):
            print(f'\t - {u}')
            for d in with_dependencies.get(u):
                print(f'\t\t - {d}')
        else:
            print(f'\t - {u}')

    print("\nWARNING: Remove listed libraries or your dependencies it's at \
your own risk")
