from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='travislint',
    version='0.1',
    long_description=readme(),
    description='An application to simplify linting of travis-ci config files.',
    author='Paul D.Smith',
    author_email='paul@pauldsmith.org.uk',
    url='https://github.com/papadeltasierrra/travislint',
    packages=['travislint'],
    install_requires=[
        'requests',
        'PyYaml'        
    ],
    entry_points = {
        'console_scripts': ['travislint=travislint.travislint:main'],
    },
    include_package_data=True
)
