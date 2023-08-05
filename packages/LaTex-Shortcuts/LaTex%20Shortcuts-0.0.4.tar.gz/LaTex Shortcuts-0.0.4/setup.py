import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LaTex Shortcuts",  # Replace with your own username
    version="0.0.4",
    author="Aria Bagheri",
    author_email="ariab9342@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AriaBagheri/LatexShortcuts",
    packages=setuptools.find_packages(),
    py_modules=["keyboards", ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
