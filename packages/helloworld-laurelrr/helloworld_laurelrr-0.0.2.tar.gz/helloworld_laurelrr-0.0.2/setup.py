from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    url="https://github.com/laurelrr/helloworld_laurelrr",
    author="Laurel Keyes",
    author_email="laurelrr@gmail.com",
    name='helloworld_laurelrr',   # this is the name you will pip install
    version='0.0.2',          # 0.0.X implies unstable branch
    description='Say hello!',    
    py_modules=["helloworld_laurelrr"], # list of actual python code modules
    package_dir={'':'src'}, # tells setuptools your code is in a source directory.
    classifiers=[                # see https://pypi.org/classifiers
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    extras_require = {    
        "dev": [
            "pytest>3.3",   # allows you to test the install using pytest
        ]
    },
)