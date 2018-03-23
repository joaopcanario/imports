from collections import defaultdict

import dis
import functools
import glob
import operator
import os
import pip
import re


'''Main module'''


def _excluded_imports(env_path='.env'):
    out = ['pip', 'setuptools']

    if not os.path.isfile(env_path):
        return out

    with open(env_path, 'r') as env_file:
        env = [x.strip() for x in env_file.readlines()]
        packages = [ln.split('=')[1].split(',') for ln in env]
        out = out + functools.reduce(operator.concat, packages)

    return out


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

    root_dir = os.path.join(location, '**/[!.]*.py')

    for python_file in glob.iglob(root_dir, recursive=True):
        all_imports += _find_modules(str(python_file))

    return set(all_imports)


def _load_requirements(requirements_name, path_dir):

    root_dir = os.path.join(path_dir, requirements_name)

    try:
        with open(root_dir, 'r') as f:
            requirements = [re.match(r'^(\w+(-\w+)*)', line).group(0)
                            for line in f]
    except FileNotFoundError:
        requirements = []

    return requirements


# def _usage():
#     print("Usage: imports <PATH_TO_PROJECT_FOLDER>")
#     print("For more information, please see README file.")
#     sys.exit(1)


def check(path_dir, requirements_name='requirements.txt'):
    '''Look for unused packages listed on project requirements'''
    requirements = _load_requirements(requirements_name, path_dir)
    imported_modules = _iter_modules(path_dir)
    installed_packages = _list_installed_packages()

    imported_modules.update(_excluded_imports())

    diff = {lib for lib in installed_packages if lib not in imported_modules}
    with_dependencies, _ = _list_dependencies(diff)
    unused_dependencies = sorted([d for d in diff if d in requirements])

    for unused_dependency in unused_dependencies:
        if with_dependencies.get(unused_dependency):
            print('    - {}'.format(unused_dependency))
            for dependency in with_dependencies.get(unused_dependency):
                print('\t - {}'.format(dependency))
        else:
            print('    - {}'.format(unused_dependency))
