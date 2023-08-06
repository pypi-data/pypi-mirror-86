from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='hop-file-browser',
    version='1.0.2',
    author='hop by benrruter + pip installation script by Elsoleiro',
    description='Python-written terminal based file explorer with support for windows/unix',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/benrrutter/hop',
    packages=['hop'],
    extras_require={'unix':['getch']},
    entry_points={
        'console_scripts':[
            'hop = hop.hop:main',
        ],
    },
) 
