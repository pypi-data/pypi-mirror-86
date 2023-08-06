import os
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

    def find_packages(where='.'):
        # os.walk -> list[(dirname, list[subdirs], list[files])]
        return [folder.replace("/", ".").lstrip(".")
                for (folder, _, fils) in os.walk(where)
                if "__init__.py" in fils]

from cvpoc import __version__, __author__, __author_email__, __license__


setup(
    name='cvpoc',
    version=__version__,
    url='',
    description='CvPoc is an open-sourced remote vulnerability testing framework developed by the CV Team.',
    long_description="""\
CvPoc is an open-sourced remote vulnerability testing and proof-of-concept development framework developed by the CV Team. """,
    keywords='PoC,Exp,CvPoc',
    author=__author__,
    author_email=__author_email__,
    maintainer='cvpoc developers',
    platforms=['any'],
    license=__license__,
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.4',
    entry_points={
        "console_scripts": [
            "cvpoc = cvpoc.poc:main",
        ]
    },
    install_requires=[
        'requests',
        'requests-toolbelt',
        'termcolor'
    ],
)