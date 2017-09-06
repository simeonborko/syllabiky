from distutils.core import setup

setup(name='syllabiky', version='1.0',
    packages=['syllabiky'],
    package_dir={'syllabiky': 'src/syllabiky'},
    package_data={'syllabiky': ['data/*.txt']})
