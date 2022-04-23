import setuptools

from real_estate.__main__ import main

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="real_estate",
    version="0.1.0",
    author="kravtsov-dima",
    author_email="kravtsovdmitri@gmial.com",
    description="A simple real estate data analyzer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kravtsov-dima/real-estate",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts':[
            'real_estate_analyser = real_estate.__main__:main'
        ],
    }
)
