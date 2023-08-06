from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["telethon"]

setup(
    name="teleshell",
    version="0.0.6",
    author="EgTer",
    author_email="annom2017@mail.ru",
    description="A shell for telethon",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://notabug.org/EgTer/teleshell",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)