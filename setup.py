from setuptools import setup


with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="youtube_py", 
    version="0.1",
    packages=["youtube_py"],
    package_dir={"youtube_py": "."},
    install_requires=requirements,
)