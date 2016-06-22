from setuptools import setup, find_packages

setup( 
        name='stampede_tools', 
        version='0.1',
        description = 'simple python library tracking flies for the stampede assay',
        author = 'William Dickson, IO Rodeo Inc.',
        author_email = 'will@iorodeo.com',
        packages=find_packages(),
        scripts=[ 'bin/stampede-tools'],
        license='LICENSE.txt'
        )

