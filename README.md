# pyERGM
---------

pyERGM is a Python library that allows users to build ERGM models in Python.


## Installation
----------------
Following installation steps below will create a conda virtual environment and install pyERGM. It is recommended to install pyERGM in a conda virtual environment to avoid 
any conflicts between pyERGM requirements and pre-existing configurations on your machine.

1. Create a conda virtual environment
```
conda create --name pyergm_venv python=3.9
```

2. Activate conda virtual environment
```
conda activate pyergm_venv
```

3. Install pyERGM
```
pip install git+https://github.com/mallaham/pyERGM
```

## Using pyERGM
---------------
In order to use pyERGM, you first must import the library:
```python
from pyERGM import ergm
```
This will create an instance of pyERGM which allows you to build your model. For additiona information/example, check the examples folder.

