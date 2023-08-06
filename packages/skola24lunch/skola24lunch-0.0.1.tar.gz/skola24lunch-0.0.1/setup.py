import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="skola24lunch", # Replace with your own username
    version="0.0.1",
    author="Pontus Norrström",
    author_email="donran@protonmail.com",
    description="Library to handle Skola24's obscure API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/donran/skola24lunch",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
