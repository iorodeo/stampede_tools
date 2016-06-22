from setuptools import setup, find_packages
import os.path
import platform


setup( 
        name='stampede_tools', 
        version='0.1',
        description = 'simple python library tracking flies for the stampede assay',
        author = 'William Dickson, IO Rodeo Inc.',
        author_email = 'will@iorodeo.com',
        packages=find_packages(),
        #scripts=[ os.path.join('bin','stampede-tools')],
        entry_points = {
            'console_scripts' : [
                'stampede-tools = stampede_tools.commandline_app:main',
                ]
            },
        license='LICENSE.txt'
        )

