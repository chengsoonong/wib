"""
Common interfacte to git and hg
"""
from setuptools import find_packages, setup

dependencies = ['click']

short_description = 'Simplified common interface to git and hg'
with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='wib',
    version='0.2.10',
    url='https://github.com/chengsoonong/wib',
    license='GPLv3',
    author='Cheng Soon Ong',
    author_email='chengsoon.ong@anu.edu.au',
    description=short_description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=['click'],
    entry_points='''
        [console_scripts]
        wib=wib.cli:main
        ''',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
