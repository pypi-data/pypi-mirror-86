from setuptools import setup, find_packages
import pathlib


here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')
setup(
    name="simplelayout-cium123",
    version='0.0.1',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=['numpy','matplotlib', 'scipy', 'pytest'],
    entry_points={
        'console_scripts': [
            'simplelayout=simplelayout:main',
        ],
    },
)
