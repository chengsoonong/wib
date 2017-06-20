import pypandoc
import os
import sys
# pypandoc.core.PANDOC_PATH = '/usr/local/bin/pandoc'


def register(location):
    """Generate a ReStructuredText file from the Markdown readme and register"""
    doc = pypandoc.Document()
    doc.markdown = open('README.md').read()
    f = open('README.rst', 'w+')
    f.write(doc.rst)
    f.close()
    os.system('setup.py register -r {}'.format(pypi))
    os.remove('README.rst')


if __name__ == '__main__':
    pypi = sys.argv[1]
    if pypi in ['pypi', 'pypitest']:
        register(pypi)
