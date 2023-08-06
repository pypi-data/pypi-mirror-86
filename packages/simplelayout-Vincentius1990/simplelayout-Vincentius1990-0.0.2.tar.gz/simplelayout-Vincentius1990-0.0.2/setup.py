import setuptools
import pathlib

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="simplelayout-Vincentius1990",
    version="0.0.2",
    author="Vincentius1990",
    author_email="vincent1990@126.com",
    description="A small example package",
    # long_description=long_description,
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    entry_points={
        'console_scripts': [
            "simplelayout = simplelayout.__main__:main",
        ],
    },
    install_requires=['matplotlib', 'numpy', 'scipy']
)
