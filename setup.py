from setuptools import setup
setup(
    name = 'mountebank-python',
    packages = ['mountebank'],
    version = '0.1.3',
    description = 'A thin convenience wrapper for interacting with Mountebank from Python',
    author = 'Alex Holyoke',
    author_email = 'aholyoke@uwaterloo.ca',
    license = "MIT",
    url = 'https://github.com/aholyoke/mountebank-python',
    download_url = 'https://github.com/aholyoke/mountebank-python/tarball/0.1',
    keywords = ['testing', 'mountebank'],
    classifiers = [],
    install_requires = ['requests>=2.5.3'],
)