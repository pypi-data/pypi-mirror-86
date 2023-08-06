from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='kenworthy',
    url='https://github.com/mkenworthy/kenworthy',
    author='Matthew Kenworthy',
    author_email='matthew.kenworthy@gmail.com',
    # Needed to actually package something
    packages=['kenworthy'],
    # Needed for dependencies
    install_requires=['numpy','astropy'],
    # *strongly* suggested for sharing
    version='0.1.2',
    # The license can be anything you like
    license='MIT',
    description='Astronomy routines for extrasolar planets, exorings and dust scattering',
    # We will also need a readme eventually (there will be a warning)
    long_description=open('README.md').read(),
)
