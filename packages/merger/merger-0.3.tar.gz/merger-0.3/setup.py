import os

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
    version="0.3",
    py_modules=["main"],
    install_requires=[
        "click==7.1.2",
        "click-completion==0.5.2",
        "colored==1.4.2",
        "gitdb==4.0.5",
        "GitPython==3.1.11",
        "Jinja2==2.11.2",
        "MarkupSafe==1.1.1",
        "prompt-toolkit==3.0.8",
        "pyfiglet==0.8.post1",
        "sh==1.14.1",
        "shellingham==1.3.2",
        "six==1.15.0",
        "smmap==3.0.4",
        "wcwidth==0.2.5",
    ],
    scripts=[
        "./bin/merger",
        "./autocomplete/merger-zsh-complete.sh",
        "./autocomplete/merger-bash-complete.sh",
        "./autocomplete/merger-fish-complete.sh",
    ],
    include_package_data=True,
    package_data={"autocomplete": ["autocomplete/*"]},
)
