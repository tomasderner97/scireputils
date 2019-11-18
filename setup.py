from setuptools import setup, find_packages

setup(
    name='scireputils',
    version='0.1.1',
    url='https://github.com/tomasderner97/scireputils.git',
    author='Tomáš Derner',
    packages=['scireputils'],
    install_requires=[
        'numpy',
        'matplotlib',
        'pandas'
    ],
)
