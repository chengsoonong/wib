"""
Common interfacte to git and hg
"""
from setuptools import find_packages, setup

dependencies = ['click']

short_description = 'Simplified common interface to git and hg'
# Hack to convert Markdown to ReStructuredText
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except:
    long_description = short_description

setup(
    name='wib',
    version='0.2.6',
    url='https://github.com/chengsoonong/wib',
    license='BSD',
    author='Cheng Soon Ong',
    author_email='chengsoon.ong@anu.edu.au',
    description=short_description,
    long_description=long_description,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=['click'],
    entry_points={
        'console_scripts': [
            'wib = wib.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
