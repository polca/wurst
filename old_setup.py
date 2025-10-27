from setuptools import setup, find_packages


setup(
    name="wurst",
    version=version,
    packages=find_packages(include=["wurst", "wurst.*"],),
    author="Chris Mutel",
    author_email="cmutel@gmail.com",
    license="BSD 3-clause",
    package_data={"wurst": ["IMAGE/metadata/*.*", "REMIND/metadata/*.*",]},
    install_requires=[
        "appdirs",
        "constructive_geometries>=0.9.4",
        "docopt",
        "numpy",
        "pandas",
        "python-json-logger",
        "toolz",
        "tqdm",
        "wrapt",
    ],
    entry_points={"console_scripts": ["wurst-cli = wurst.bin.wurst_cli:main",]},
    url="https://github.com/polca/wurst",
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    description=(
        "Wurst is a python package for linking and modifying "
        "industrial ecology models"
    ),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
)
