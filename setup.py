from setuptools import find_packages,setup
from typing import List

def get_requirements() -> List[str]:
    requirements_list = []
    try:
        with open("requirements.txt") as file_obj:
            lines = file_obj.readlines()
            for line in lines:
                requirement = line.strip()
                if requirement and requirement!='-e .':
                    requirements_list.append(requirement)
    except FileNotFoundError:
        print("requirements.txt does not exist")
    return requirements_list

setup(
    name="Employee Attrition",
    version='0.0.1',
    author='Smruti R',
    packages=find_packages(),
    install_requires = get_requirements()
)