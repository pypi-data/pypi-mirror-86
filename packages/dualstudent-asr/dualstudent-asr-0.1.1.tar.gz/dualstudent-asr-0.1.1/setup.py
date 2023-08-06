from setuptools import setup, find_packages

setup(
    name='dualstudent-asr',
    version='0.1.1',
    description='Dual Student for Automatic Speech Recognition',
    author='Franco Ruggeri, Andrea Caraffa, Kevin Dalla Torre Castillo, Simone Porcu',
    author_email='fruggeri@kth.se, caraffa@kth.se, kevindt@kth.se, porcu@kth.se',
    license='GPL',
    packages=find_packages(include=['dualstudent', 'dualstudent.*']),
    include_package_data=True
)
