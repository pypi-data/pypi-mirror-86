from setuptools import setup, find_packages

with open("README.md", "r") as stream:
    long_description = stream.read()

setup(
    name = 'DBSL.py',
    version = '0.0.5',
    url = 'https://github.com/wezacon/DBSL.py',
    download_url = 'https://github.com/wezacon/DBSL.py/tarball/master',
    license = 'MIT',
    author = 'Team Wezacon',
    author_email = 'wezacon.com@gmail.com',
    description = 'API wrapper for DBSL',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    keywords = [
        'DBSL',
        'DBSL-py',
        'wezacon',
        'official'
    ],
    install_requires = [
        'setuptools',
        'requests',
        'six',
        'ujson'
    ],
    setup_requires = [
        'wheel'
    ],
    packages = find_packages()
)
