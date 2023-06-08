from setuptools import setup


with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="youtube_py", 
    version="0.1",
    packages=["."],
    install_requires=requirements,
)