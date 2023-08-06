import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pretty_errors",
    version="1.2.19", # remember to also update __version__ in __init__.py!
    author="Iain King",
    author_email="iain.king@gmail.com",
    description="Prettifies Python exception output to make it legible.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/onelivesleft/PrettyErrors/",
    packages=setuptools.find_packages(),
    install_requires=[
        "colorama",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
