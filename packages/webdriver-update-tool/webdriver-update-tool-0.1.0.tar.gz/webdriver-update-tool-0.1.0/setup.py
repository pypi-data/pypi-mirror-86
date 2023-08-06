import setuptools

with open("README.md", 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="webdriver-update-tool",
    version="0.1.0",
    author="cjz25",
    description="A tool for updating the webdriver automatically",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        'selenium >= 3.141.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
    ],
    python_requires='>=3.5',
)
