from setuptools import setup


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name='PythonPals',
    version='2.0.30',
    packages=['PythonPals'],
    url='https://github.com/nathanhilton/PythonPals/tree/development',
    author='Sheamus Cooper',
    author_email='sheamus.cooper@ufl.edu',
    description='Production Release',
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=["Programming Language :: Python :: 3"],
    entry_points={
        "console_scripts": [
            "python-pals=PythonPals.main:main",
        ]
    },
)
