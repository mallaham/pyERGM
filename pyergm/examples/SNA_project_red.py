# local testing
# import rpy_interface as rpyInterface
# from network_statistics import NetworkStats
# from ergm import pyERGM, ModelDiagnostics
# from simulator import Simulator
# from data_transformer import DataTransformer
from pyergm import rpy_interface as rpyInterface
from pyergm.network_statistics import NetworkStats
from pyergm.ergm import pyERGM, ModelDiagnostics
from pyergm.simulator import Simulator
from pyergm.data_transformer import DataTransformer
import pandas as pd
from rpy2.robjects import NA_Real
import logging 
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

if __name__ == "__main__":
    
    rpackages = ['statnet', 'ergm','texreg', 'base', 'grDevices'] # removing igraph because it causes issues with ergm native functions
    renv = rpyInterface.intializeRenv(mirror=1, r_packages= rpackages)
    installed_packages = renv.setup_renv()

    # import data
    # use index_col to specify which columns to use as an index
    data = pd.read_csv("/Users/Mowafak/Documents/NU_research/SONIC/pyERGM/data/project_red/adj_matrix.csv",index_col=0)#hera_c4_sna_ergm_demo.csv")
    
    dt = DataTransformer(renv)
    team = dt.rdf_to_list(dt.to_rdf(pd.read_csv("data/project_red/hera_c4_sna_ergm_demo.csv",usecols=["hera_mag"])), "hera_mag")
    
    # converting pandas dataframe to r
    team_rdf = dt.to_rdf(data)

    # loading adjancency as a matrix
    team_network = dt.adjacency_to_matrix(team_rdf)
    ###
    
    team_network = dt.set_vertex_attribute(team_network, "hera_mag", team) 

    ################################
    ## Calculate network metrics
    ################################
    ns = NetworkStats(renv)
    summary = ns.summary(team_network)
    print(summary)
    network_size = ns.network_size(team_network)
    print(network_size)
    betweeness = ns.betweeness(team_network)
    print(betweeness)
    isolates = ns.isolates(team_network)
    print(isolates)

    formula = "buyIn ~ edges + mutual + nodemix('hera_mag',base=2)" #fix formual
    vars = {"buyIn": team_network, "hera_mag":team}
    
    # model definition and parameters
    ergm = pyERGM(installed_packages['ergm'], formula, vars)
    params = dict({"formula":ergm.formula}) # make sure to include = for parameters that require = vs parameters that can be upacked such as formula
    model = ergm.fit_model(params)
    summary = ergm.summary(model)
    print(summary)

    #####################
    ## Model Diagnositics
    #####################
    ergm_diagnostics = ModelDiagnostics(renv)
    
    # MCMC
    filename, mcmc_results = ergm_diagnostics.run_mcmc(model)
    print(filename)

    ## Goodness of fit
    gof_params = dict({"verbose=":"T","burnin=":1e+5,"interval=":1e+5})
    gof = ergm_diagnostics.gof(model, gof_params, n=100)
    print(gof)
    
    ###############
    ## Simulations
    ###############
    sim_parms = {"burnin=":100000, "interval=":100000, "verbose=":"T", "seed=":10}
    simulator = Simulator(model, sim_parms)
    sim_results = simulator.simulate()
    print(len(simulator.get_triangles()))