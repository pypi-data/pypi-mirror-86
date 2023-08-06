from setuptools import setup


def generate_requirements():
    requirements = []
    with open("requirements.txt", "r") as f:
        requirements = f.read().split("\n")

    return requirements


setup(
    name="merger",
    author="Nicholas Young",
    author_email="nick@bolted.io",
    description="Package used for merging branches, squashing them and saying who reviewed them",
    version="0.1",
    py_modules=["main"],
    install_requires=generate_requirements(),
    scripts=["./bin/merger"],
)
