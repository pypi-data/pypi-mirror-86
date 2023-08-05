import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
        name="tictactoe-abhay",
        version="0.0.5",
        author="Abhay Vashist",
        author_email="avashist98@tamu.edu",
        description="A small package that provide the backend for tictactoe",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/Avashist1998/tictactoe-abhay",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            ],
        python_requires='>=3.6',
        )