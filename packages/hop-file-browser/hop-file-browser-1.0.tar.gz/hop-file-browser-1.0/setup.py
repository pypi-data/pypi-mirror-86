import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hop-file-browser",
    version="1.0",
    author="Ben Rutter",
    author_email="benrrutter@gmail.com",
    description="Hop is a TUI file browser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/benrrutter/hop",
    packages=setuptools.find_packages(),
    entry_points ={
        "console_scripts": [
            "hop = run_hop.hop:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
