import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Suluoya",
    version="1.2.1",
    author="Suluoya",
    author_email="1931960436@qq.com",
    description="All kinds of things written by Suluoya.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests',
                    'pandas',
                    'beautifulsoup4',
                    'translators',
                    'fuzzywuzzy',
                    'ngender',
                    'MyQR',
                    'pyforest',
                    'wget',
                    'urllib3',
                    ]
)
