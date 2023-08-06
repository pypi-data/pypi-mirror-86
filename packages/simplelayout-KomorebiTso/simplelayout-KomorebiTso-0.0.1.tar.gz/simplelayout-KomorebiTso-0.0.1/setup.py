import pathlib
from setuptools import setup, find_packages
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")
setup(
    name="simplelayout-KomorebiTso",
    version="0.0.1",
    author="KomorebiTso",
    author_email="Komorebi0216@163.com",
    url='https://github.com/idrl-\
        assignment/3-simplelayout-package-KomorebiTso',
    description="simplelayout package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages("src"),
    package_dir={'': 'src'},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy", "matplotlib", "scipy", "pytest"
    ],
    entry_points={
        'console_scripts': [
            'simplelayout=simplelayout.__main__:main'
        ]
    }
)
