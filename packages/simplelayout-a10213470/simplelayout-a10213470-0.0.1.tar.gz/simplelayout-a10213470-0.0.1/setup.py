from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name="simplelayout-a10213470",  # Replace with your own username
    version="0.0.1",
    author="miraqiaox",
    author_email="miraqiaox@qq.com",
    description="a layout package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={'': 'src'},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "numpy", "matplotlib", "scipy"
    ],
    entry_points={
        'console_scripts': [
            'simplelayout=simplelayout.__main__:main'
        ]
    }
)
