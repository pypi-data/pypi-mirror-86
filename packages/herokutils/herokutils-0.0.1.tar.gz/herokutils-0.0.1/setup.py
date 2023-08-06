from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup(
    name='herokutils',
    version='0.0.1',
    description='utilities for heroku deployment',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    author='Sebastien Villard',
    author_email='sebastien.villard@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=['pandas>=1.1.0', 'nltk>=3', 'numpy>=1.19', 'scikit-learn>=0.23']
)
