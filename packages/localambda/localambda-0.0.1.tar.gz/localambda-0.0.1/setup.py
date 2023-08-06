from setuptools import find_packages, setup

from pathlib import Path


def strip_comments(l):
    return l.split('#', 1)[0].strip()


def _pip_requirement(req, *root):
    if req.startswith('-r '):
        _, path = req.split()
        return reqs(*root, *path.split('/'))
    return [req]


def _reqs(*f):
    path = (Path.cwd() ).joinpath(*f)
    with path.open() as fh:
        reqs = [strip_comments(l) for l in fh.readlines()]
        return [_pip_requirement(r, *f[:-1]) for r in reqs if r]


def reqs(*f):
    return [req for subreq in _reqs(*f) for req in subreq]


setup(
    name='localambda',
    version='0.0.1',
    description='A utility to easily test lambdas locally.',
    url='https://github.com/tree-schema/localambda',
    author='Grant Seward',
    author_email='grant@treeschema.com',
    packages=find_packages(),
    zip_safe=False,
    install_requires=reqs('requirements.txt'),
    entry_points={
        'console_scripts': [
            'lola = localambda.cli.cli:entry',
        ],
    }
)
