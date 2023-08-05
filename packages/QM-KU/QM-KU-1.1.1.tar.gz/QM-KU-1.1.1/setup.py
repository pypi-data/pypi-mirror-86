from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    f.read()
    long_description = f.read()

setup(
    name='QM-KU',
    version='1.1.1',
    scripts=['__init__.py','QM.py'],
    description='QM library introducing vector-like and matrix like bra, ket, and operator classes',
    license="cc-by-sa-4.0",
    long_description=long_description,
    author='Rasmus Skytte Eriksen',
    author_email='rasmus.eriksen@nbi.ku.dk',
    packages=[''],
    install_requires=['numpy'], #external packages as dependencies
)
