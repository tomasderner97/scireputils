from setuptools import setup, find_packages

setup(
    name='scireputils',
    version='0.1.1',
    url='https://github.com/tomasderner97/scireputils.git',
    author='Tomáš Derner',
    packages=['scireputils'],
    include_package_data=True,
    install_requires=[
        'numpy',
        'matplotlib',
        'pandas', 'scipy', 'jinja2'
    ],
)
