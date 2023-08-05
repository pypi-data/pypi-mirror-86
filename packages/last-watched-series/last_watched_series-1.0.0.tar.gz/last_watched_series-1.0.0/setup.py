from setuptools import setup, find_packages
from os import path
from io import open
import pathlib

# Directory containing this file
HERE = pathlib.Path(__file__).parent

# Get README for long description
README = (HERE / "README.md").read_text()


# Load all required modules
with open(path.join(HERE, "requirements.txt"), encoding="utf-8") as f:
    all_requirements = f.read().split("\n")
install_requires = [x.strip() for x in all_requirements if ('git+' not in x)
                    and (not x.startswith('#')) and (not x.startswith('-'))]
dependency_links = [x.strip().replace('git+', '') for x in all_requirements if 'git+' not in x]

# Setup
setup(
    author="Qyutou",
    name="last_watched_series",
    description="A simple commandline application to memorizing the last watched series",
    version="1.0.0",
    packages=find_packages(),
    install_requires=install_requires,
    entry_points="""
        [console_scripts]
        last_watched_series=last_watched_series.main:main
        """,
    long_description=README,
    long_description_content_type="text/markdown",
    author_email="qyutou@gmail.com",
    license="MIT",
    url="https://github.com/Qyutou/last_watched_series"
)
