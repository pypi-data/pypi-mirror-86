#!/usr/bin/env python3
import os
import sys

import setuptools


requires = [
    'certifi',
    'pyopenssl',
]

tests_require = [
]

here = os.path.abspath(os.path.dirname(__file__))


# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()

about = {}
with open(os.path.join(here, 'src', 'sslcheck', '__init__.py')) as f:
    exec(f.read(), about)

with open('README.md', 'r') as f:
    readme = '\n' + f.read()

setuptools.setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    download_url=about['__download_url__'],
    license=about['__license__'],
    packages=setuptools.find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=requires,
    tests_require=tests_require,
    python_requires='>=3.5',
    keywords='sslcheck',
    entry_points={
        'console_scripts': [
            'sslcheck = sslcheck:main'
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: POSIX :: Linux",
        "Natural Language :: English",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop", ] + [
        ('Programming Language :: Python :: %s' % x) for x in
        '3 3.5 3.6 3.7 3.8 3.9'.split()
    ],
    zip_safe=False,
)
