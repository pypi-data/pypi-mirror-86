import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="data_to_html-connosieurofdoom",
    version="0.0.0.1",
    author="Example Author",
    author_email="shreyasajitrajendra@gmail.com",
    description="Convert Dataframe to html elements",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/connosieurofdoom/data_to_html",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)