"""Python-Marketman Package Setup"""

import os
import textwrap

import setuptools

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, 'python_marketman', '__version__.py'), 'r') as f:
    exec(f.read(), about)


setuptools.setup(
    name=about['__title__'],
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    maintainer=about['__maintainer__'],
    maintainer_email=about['__maintainer_email__'],
    url=about['__url__'],
    license=about['__license__'],
    description=about['__description__'],
    long_description=textwrap.dedent(open('README.rst', 'r').read()),
    keywords=about['__keywords__'],
    test_suite='pytest-runner',

    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    python_requires='>=3.6',
    setup_requires=['pytest-runner', 'flake8'],
    tests_require=['pytest', ],
)
