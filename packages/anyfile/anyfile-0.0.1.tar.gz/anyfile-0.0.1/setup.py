from importlib.machinery import SourceFileLoader
from pathlib import Path

from setuptools import setup


description = 'Load (almost) any structured file parse its data with pydantic'
THIS_DIR = Path(__file__).resolve().parent
try:
    long_description = (THIS_DIR / 'README.md').read_text() + '\n\n' + (THIS_DIR / 'HISTORY.md').read_text()
except FileNotFoundError:
    long_description = description + '.\n\nSee https://anyfile.helpmanual.io/ for documentation.'

# avoid loading the package before requirements are installed:
version = SourceFileLoader('version', 'anyfile/version.py').load_module()


setup(
    name='anyfile',
    version=version.VERSION,
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX :: Linux',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet',
    ],
    author='Samuel Colvin',
    author_email='s@muelcolvin.com',
    url='https://github.com/samuelcolvin/anyfile',
    license='MIT',
    packages=['anyfile', 'anyfile.formats'],
    package_data={'anyfile': ['py.typed']},
    python_requires='>=3.7',
    zip_safe=False,  # https://mypy.readthedocs.io/en/latest/installed_packages.html
    # install_requires=[],
    extras_require={
        'all': [],
    },
)
