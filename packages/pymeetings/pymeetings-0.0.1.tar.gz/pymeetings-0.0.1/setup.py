import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="pymeetings",
    version="0.0.1",
    author="Fabio Capela",
    author_email="capela625@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fregocap/PyMeeting",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data = True
)
