import r_setup as r
import pandas as pd
from ergm import pyERGM
from simulator import Simulator
from rpy2.robjects import NA_Real
from data_transformer import DataTransformer
import rpy2.robjects as robjects
import numpy as np
if __name__ == "__main__":
    ################
    ## Load pacakges
    ################
    #rpackages = ['statnet', 'ergm','igraph','texreg']
    rpackages = ['statnet', 'ergm','texreg', 'base', 'grDevices'] # removing igraph because it causes issues with ergm native functions
    renv = r.intializeRenv(mirror=1, r_packages= rpackages)
    installed_packages = renv.setup_renv()

    ################
    ## Load data
    ################
    # use index_col to specify which columns to use as an index
    data = pd.read_csv("/Users/Mowafak/Documents/NU_research/SONIC/pyERGM/data/project_red/adj_matrix.csv",index_col=0)#hera_c4_sna_ergm_demo.csv")
    # pandas to edgelist
    #  G=nx.from_pandas_edgelist(graph_df,'source','target',create_using=nx.DiGraph())
    # pulling adjacency matrix

    #adjacency matrix to edgelist 
    # edgelist = data.stack().reset_index().rename(columns={"level_0":"Source", "level_1": "Target", 0:"edge"})
    # edgelist = edgelist[edgelist['Source'].astype(str)!=edgelist['Target'].astype(str)] # to remove self-loops (1-->1)
    # edgelist = edgelist[edgelist['edge']==1].drop(columns='edge').reset_index(drop=True) # keeping all rows with edge equals to 1 then dropping the column
    # print(edgelist)

    ################
    ## Data processing
    ################
    dt = DataTransformer()
    team = dt.rdf_to_list(dt.to_rdf(pd.read_csv("data/project_red/hera_c4_sna_ergm_demo.csv",usecols=["hera_mag"])), "hera_mag")
    r_buyInFromYouEdgelist = dt.to_rdf(data)

    ###
    # maybe refactor the following two lines to be a single python function to take either adjacency matrix or edgelist and returns a matrixs
    asmatrix = renv.load_robject('as.network.matrix')
    buyIn = asmatrix(r_buyInFromYouEdgelist, **{"matrix.type":"adjacency"}) # unpacks parameters from python to R in this case user can specify either an adjacency or edgelist
    ###
    
    set_vertex_att = renv.load_robject('set.vertex.attribute')
    buyIn = set_vertex_att(buyIn, "hera_mag", team) 

    ################################
    ## Calculate network metrics
    ################################
    # load network functions
    summary = renv.load_robject('summary')(buyIn)
    network_size = renv.load_robject('network.size')(buyIn)
    betweeness = renv.load_robject('betweenness')(buyIn)
    isolates = renv.load_robject('isolates')(buyIn)

    ################################
    ## Building ERGM
    ################################
    formula = "buyIn ~ edges + mutual + nodemix('hera_mag',base=2)" #fix formual
    vars = {"buyIn": buyIn, "hera_mag":team}
    
    # model definition and parameters
    ergm = pyERGM(installed_packages['ergm'], formula, vars)
    params = dict({"formula":ergm.formula}) # make sure to include = for parameters that require = vs parameters that can be upacked such as formula
    model = ergm.ergm(**params)
    summary = ergm.summary(model)
    
    ################################
    ## Goodness of fit analysis 
    ################################
    filename, mcmc_results = ergm.mcmc_summary(model)

    simulate_parms = {"burnin=":100000, "interval=":100000, "verbose=":"T", "seed=":10}
    sim = Simulator(model, simulate_parms)
    sim_results = sim.simulate()

    gof_params = dict({"verbose=":"T","burnin=":1e+5,"interval=":1e+5})
    gof = ergm.gof(model, gof_params, n=100)
    # print(filename)
    print(summary)
    # print(gof)
    print("======")
    print(len(sim.get_triangles()))