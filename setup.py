import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="PyChanter",
    version="0.0.1",
    author="Hariharan",
    author_email="hari.haran849@example.com",
    description="A small Scintilla based python editor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hariharan849/PyChanter",
    packages=setuptools.find_packages('resources'),
    include_package_data=True,
    package_data={
        'resources': ['*.qss', '*.png', '*.stylesheet', '*.ui'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)