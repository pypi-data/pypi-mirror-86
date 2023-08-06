#
# Copyright 2017 University of Southern California
# Distributed under the GNU GPL 3.0 license. See LICENSE for more info.
#

""" Installation script for deriva.qt
"""

from setuptools import setup, find_packages
import re
import io

__version__ = re.search(
    r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
    io.open('deriva/qt/__init__.py', encoding='utf_8_sig').read()
    ).group(1)


def get_readme_contents():
    with io.open('README.md') as readme_file:
        return readme_file.read()


url = 'https://github.com/informatics-isi-edu/deriva-qt'
author = 'USC Information Sciences Institute, Informatics Systems Research Division'
author_email = 'isrd-support@isi.edu'


setup(
    name='deriva-qt',
    description='Graphical User Interface tools for DERIVA built on PyQt5',
    long_description="For further information, visit the project [homepage](%s)." % url,
    long_description_content_type='text/markdown',
    url=url,
    author=author,
    author_email=author_email,
    maintainer=author,
    maintainer_email=author_email,
    version=__version__,
    python_requires='>3.5.2',
    packages=find_packages(),
    package_data={'deriva.qt': ['upload_gui/conf/config.json', '*/resources/images/*']},
    entry_points={
        'console_scripts': [
            'deriva-auth = deriva.qt.auth_agent.__main__:main',
            'deriva-upload = deriva.qt.upload_gui.__main__:main'
        ]
    },
    install_requires=[
        'deriva>=1.0.0'
    ],
    extras_require={
        'PyQt5': ["PyQt5==5.11.3"],
        'PyQtWebEngine': ["PyQtWebEngine>=5.12.1"]
    },
    license='GNU GPL 3.0',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)

