"""Installation script."""
from setuptools import setup
from pkg_resources import parse_version


name = 'pycflow2dot'
description = (
    'Create C call graphs from multiple source files '
    'using Cflow, producing linked PDF.')
long_description = open('README.md').read()
url = 'https://github.com/johnyf/{name}'.format(name=name)
VERSION_FILE = '{name}/_version.py'.format(name=name)
MAJOR = 0
MINOR = 2
MICRO = 3
VERSION = '{major}.{minor}.{micro}'.format(
    major=MAJOR, minor=MINOR, micro=MICRO)
VERSION_TEXT = (
    '# This file was generated from setup.py\n'
    "version = '{version}'\n")
install_requires = [
    'networkx >= 2.0',
    'pydot >= 1.2.3']
tests_require = ['nose >= 1.3.4']
classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    ('License :: OSI Approved :: '
     'GNU General Public License v3 or later (GPLv3+)'),
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Topic :: Software Development']
keywords = [
    'c', 'call graph', 'control flow', 'dot',
    'latex', 'cflow']


def git_version(version):
    """Return version with local version identifier."""
    import git
    repo = git.Repo('.git')
    repo.git.status()
    # assert versions are increasing
    latest_tag = repo.git.describe(
        match='v[0-9]*', tags=True, abbrev=0)
    assert parse_version(latest_tag) <= parse_version(version), (
        latest_tag, version)
    sha = repo.head.commit.hexsha
    if repo.is_dirty():
        return '{v}.dev0+{sha}.dirty'.format(
            v=version, sha=sha)
    # commit is clean
    # is it release of `version` ?
    try:
        tag = repo.git.describe(
            match='v[0-9]*', exact_match=True,
            tags=True, dirty=True)
    except git.GitCommandError:
        return '{v}.dev0+{sha}'.format(
            v=version, sha=sha)
    assert tag == 'v' + version, (tag, version)
    return version


def run_setup():
    # version
    try:
        version = git_version(VERSION)
    except:
        print('No git info: Assume release.')
        version = VERSION
    s = VERSION_TEXT.format(version=version)
    with open(VERSION_FILE, 'w') as f:
        f.write(s)
    setup(
        name=name,
        version=version,
        description=description,
        long_description=long_description,
        long_description_content_type='text/markdown',
        author='Ioannis Filippidis',
        author_email='jfilippidis@gmail.com',
        url=url,
        license='GPLv3',
        install_requires=install_requires,
        tests_require=tests_require,
        packages=[name],
        package_dir={name: name},
        entry_points={
            'console_scripts': ['cflow2dot = pycflow2dot.pycflow2dot:main']},
        classifiers=classifiers,
        keywords=keywords)


if __name__ == '__main__':
    run_setup()
