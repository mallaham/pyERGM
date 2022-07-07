from setuptools import setup

with open("requirements.txt") as f:
    requirements = f.readlines()

setup(
    name='pyERGM',
    version='0.1.0',    
    description='Python interface to statnet ERGM object to build ERGM models in Python',
    python_requires="~=3.6",
    install_requires=requirements,
    url='https://github.com/mallaham/pyERGM.git',
    author='Mowafak Allaham',
    author_email='mowafakallaham2021@u.northwestern.edu',
    packages=['pyERGM']
)