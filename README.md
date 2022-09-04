# pyERGM
---------
pyERGM is a Python library that allows users to build Exponential Random Graph (ERGM) models in Python. Users can use pyERGM in either a `pacakge` or `dev` mode. Users accessing pyERGM in the `package` mode can install pyERGM from github similar to any other python library (as showin in step 3 of the installation) then use it in their local environment or run it in a Jupyter Notebook. The `dev` mode is for users who have an interest in contributing to pyERGM or modifying any of its existing functions or features. More information on running pyERGM in a `dev` mode will be added soon.


## Installation
----------------

`package` mode:
---------------
Regardless of the mode you plan on accessing pyERGM, it is highly recommended to create a conda virtual environment to install pyERGM and use the library in that newly created conda environment. This will avert the possibility of having any conflicts between pyERGM requirements and pre-existing configurations on your machine. The following steps will create a conda virtual environment and install pyERGM.

1. Create a conda virtual environment
```
conda create --name pyergm_venv python=3.9
```

2. Activate conda virtual environment
```
conda activate pyergm_venv
```

3. Launch a jupyter notebook in conda virtural environment
```
jupyter notebook
```
If you do not have a jupyter notebook installed in the previously created conda environemnt in step 2, run the following pip command `pip install notebook`. For an additional reference on how to install jupyter notebook, please refer to [jupyter.org/install](https://jupyter.org/install#jupyter-notebook)

4. Install pyERGM in the first cell of your notebook
```
pip install git+https://github.com/mallaham/pyERGM
```


## Using pyERGM
---------------
In order to use pyERGM, you first must import the library:
```python
from pyERGM import ergm
```
This will allow you to create an instance of pyERGM object to build your model. Please feel free to refer to the `/examples/scripts/` or `/examples/notebooks/` folders for additional details.


## pyERGM output:
-----------------

### Statistics:
In order to unify the Python and R user experiences when interpreting ERGM models, pyERGM outputs the following details:
- Network Attributes
- Vertex Attributes
- Network Size
- Model Summary
- ERGM iterations details (including convergance p-values and log-likelihood)
- Number of bridges related to bridge sampling
- Fitted ERGM model results (i.e., p-values, AIC, BIC, and log-likelihood)
- MCMC diagnositcs details
- Goodness of fit details for model parameters
- Goodness of fit for model statistics

### Simulations
If the user run any simulations, pyERGM also outputs the simulation results. Below is an example of such output:
```
Simulating 1000 networks with seed vale 340...
Counting the number of triangles in the simulated networks...
1000
```

### Reports
pyERGM outputs an MCMC diagnostics pdf report and a png image showing goodness of fit diagnostics to the output directory a user specifies in `run_mcmc()` function (please check function documentation in `ergm.py` for additional details).

You can also view the output of pyERGM in action by checking the sample notebook under `/examples/notebooks` folder.


## Sample pyERGM output
-----------------------
This is a sample of some of pyERGM output:

1. Network Attributes
```
Network attributes:
  vertices = 66
  directed = TRUE
  hyper = FALSE
  loops = FALSE
  multiple = FALSE
  bipartite = FALSE
 total edges = 225 
   missing edges = 0 
   non-missing edges = 225 
 density = 0.05244755 
```

2. Vertex Attributes
```
Vertex attributes:

 department:
   character valued attribute
   attribute summary:
   BE    ME     O     P     S Sales    TI    WB    WF 
   10    18     2    13     5     1     9     1     7 

 female:
   integer valued attribute
   66 values

 leader:
   integer valued attribute
   66 values

 office:
   integer valued attribute
   66 values

 tenure:
   integer valued attribute
   66 values
  vertex.names:
   character valued attribute
   66 valid vertex names

No edge attributes
```
3. Network Size
```
Calculating network size...
[1] 66
```

4. Model Summary:
```
ader.1.0 = 8, mix.leader.1.1 = 12)
edges                                                                 225.00                                                                           
mutual                                                                 12.00                                                                           
edgecov.hundreds_messages                                              56.69                                                                           
mix.leader.0.0                                                         94.00                                                                           
mix.leader.1.0                                                          8.00                                                                           
mix.leader.1.1                                                         12.00
```

5. Iterations details including convergance p-values and log-likelihood:
```
R[write to console]: Iteration 1 of at most 60:
R[write to console]: Convergence test P-value:2.7e-290
R[write to console]: The log-likelihood improved by 1.62.
R[write to console]: Iteration 2 of at most 60:
R[write to console]: Convergence test P-value:9.2e-231
R[write to console]: The log-likelihood improved by 1.541.
R[write to console]: Iteration 3 of at most 60:
R[write to console]: Convergence test P-value:2.9e-84
R[write to console]: The log-likelihood improved by 0.3439.
....
R[write to console]: Convergence test p-value: < 0.0001. 
R[write to console]: Converged with 99% confidence.
R[write to console]: Finished MCMLE.
```

6. Number of bridges related to bridge sampling:
```
R[write to console]: Evaluating log-likelihood at the estimate. 
R[write to console]: Setting up bridge sampling...
R[write to console]: Using 16 bridges: 
R[write to console]: 1 
R[write to console]: 2 
R[write to console]: 3 
R[write to console]: 4 
R[write to console]: 5 
R[write to console]: 6 
R[write to console]: 7 
R[write to console]: 8 
R[write to console]: 9 
R[write to console]: 10 
R[write to console]: 11 
R[write to console]: 12 
R[write to console]: 13 
R[write to console]: 14 
R[write to console]: 15 
R[write to console]: 16 
```
7. ERGM model results
```
======================================
                           Model 1    
--------------------------------------
edges                        -0.67 ***
                             (0.13)   
mutual                        1.10 ** 
                             (0.43)   
edgecov.hundreds_messages     0.35 ***
                             (0.09)   
mix.leader.0.0               -2.79 ***
                             (0.15)   
mix.leader.1.0               -3.43 ***
                             (0.51)   
mix.leader.1.1               -0.14    
                             (0.45)   
--------------------------------------
AIC                        -718.76    
BIC                        -680.57    
Log Likelihood              365.38    
======================================
*** p < 0.001; ** p < 0.01; * p < 0.05
```

7. MCMC diagnositcs
```
Iterations = 290816:5726208
Thinning interval = 4096 
Number of chains = 1 
Sample size per chain = 1328 

1. Empirical mean and standard deviation for each variable,
   plus standard error of the mean:

                              Mean     SD Naive SE Time-series SE
edges                     -1.14383 10.792  0.29614        0.32112
mutual                    -0.04518  2.966  0.08139        0.08760
edgecov.hundreds_messages -0.01139 11.519  0.31611        0.46364
mix.leader.0.0            -0.08735  8.800  0.24148        0.24148
mix.leader.1.0            -0.21009  2.467  0.06771        0.06771
mix.leader.1.1            -0.10693  2.736  0.07507        0.09937

2. Quantiles for each variable:

                             2.5%    25%    50%   75% 97.5%
edges                     -22.825 -8.000 -1.000 6.000 20.00
mutual                     -6.000 -2.000  0.000 2.000  6.00
edgecov.hundreds_messages -21.987 -8.158  0.265 8.452 22.59
mix.leader.0.0            -18.000 -6.000  0.000 6.000 16.00
mix.leader.1.0             -4.000 -2.000  0.000 1.000  5.00
mix.leader.1.1             -5.825 -2.000  0.000 2.000  5.00
```

8. Goodness of fit details for model parameters
```
Goodness-of-fit for out-degree 

         obs min  mean max MC p-value
odegree0   2   0  0.96   5       0.44
odegree1   7   1  4.24  11       0.22
odegree2  12   4 10.24  18       0.66
odegree3  11   9 16.82  24       0.14
odegree4   9   8 18.81  28       0.04
odegree5  25   7 14.93  27       0.02
```

9. Goodness of fit for model statistics
```
                             obs   min     mean   max MC p-value
edges                     225.00 185.0 225.0700 255.0       0.98
mutual                     12.00   4.0  11.9000  18.0       1.00
edgecov.hundreds_messages  56.69  30.6  56.1774  80.5       0.96
mix.leader.0.0             94.00  71.0  93.3100 120.0       0.94
mix.leader.1.0              8.00   3.0   7.4900  13.0       1.00
mix.leader.1.1             12.00   7.0  12.8400  21.0       0.90
```