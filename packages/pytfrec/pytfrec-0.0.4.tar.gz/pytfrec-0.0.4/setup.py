import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytfrec", # Replace with your own username
    version="0.0.4",
    author="dAriush Bahrami",
    author_email="dariush.bahrami@ut.ac.ir",
    description="Pythonic tools for TFRecord files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dariush-bahrami/pytfrec",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)