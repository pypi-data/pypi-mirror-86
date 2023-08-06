import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="terminal_colours-michaelstickler",
    version="1.0.0",
    author="Michael Stickler",
    author_email="contact@MGSTechArt.com",
    description="Add helpful ANSI tools for printing funky text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RedMoikle/terminal_colours",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
