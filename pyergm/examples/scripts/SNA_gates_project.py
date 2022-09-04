# local testing
# import rpy_interface as rpyInterface
# from data_transformer import DataTransformer
# from simulator import Simulator
# from ergm import pyERGM, ModelDiagnostics
# from network_statistics import NetworkStats
from pyergm import rpy_interface as rpyInterface
from pyergm.data_transformer import DataTransformer
from pyergm.simulator import Simulator
from pyergm.ergm import pyERGM, ModelDiagnostics
from pyergm.network_statistics import NetworkStats
import pandas as pd
from rpy2.robjects import NA_Real
import rpy2.robjects as robjects
import numpy as np
import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

if __name__ == "__main__":
       
    ################
    ## Load pacakges
    ################
    # possibly move this section to be part of renv
    #rpackages = ['statnet', 'ergm','igraph','texreg']
    rpackages = ['statnet', 'ergm','texreg', 'base', 'grDevices'] # removing igraph because it causes issues with ergm native functions
    renv = rpyInterface.intializeRenv(mirror=1, r_packages= rpackages)
    installed_packages = renv.setup_renv()

    ################
    ## Load data
    ################
    data = pd.read_csv("/Users/Mowafak/Documents/NU_research/SONIC/pyERGM/data/project_gates/GA_female_network_q44_free_time_together.csv")
    attributes = pd.read_csv("/Users/Mowafak/Documents/NU_research/SONIC/pyERGM/data/project_gates/attributes datafile.csv")
    # select rows that only have ties
    data = data.query("free_time==1")
    # build a nother model to include q122 (education), q118 (have a child), and q117 (marital status)
    survey_data = pd.merge(data,attributes, how='left',left_on='id1',right_on='id')
   
    ####################
    ## Data processing
    ####################
    dt = DataTransformer(renv)
    rdf_fromEdgeList = dt.to_rdf(data)
    education = dt.rdf_to_list(dt.to_rdf(survey_data['q122'].to_frame(name="education")), "education")
    have_child = dt.rdf_to_list(dt.to_rdf(survey_data['q118'].to_frame(name="have_child")), "have_child")
    marital_status = dt.rdf_to_list(dt.to_rdf(survey_data['q117'].to_frame(name="marital_status")), "marital_status")

    ####################
    ## Consutring network
    ####################
    time_together = dt.edgelist_to_matrix(rdf_fromEdgeList)
    # essential to construct a covariance matrix for the attribute you want to include as a covariate
    # TODO: ask what happens if we have more than a single covariate? Do we generate a matrix per covariate?
    education_covMatrix = dt.cov_matrix(survey_data, 'id1','id2','q122', 1309,1309)
    
    ################################
    ## Calculate network metrics
    ################################
    # ns = NetworkStats(renv)
    # summary = ns.summary(time_together)
    # print(summary)
    # network_size = ns.network_size(time_together)
    # print(network_size)
    # betweeness = ns.betweeness(time_together)
    # print(betweeness)
    # isolates = ns.isolates(time_together)
    # print(isolates)
    
    ################################
    ## Building ERGM
    ################################
    # list of ergm terms
    # https://statnet.org/nme/d2-ergmterms.html
    # Note: edgecov require constructing a matrix
    # TODO: check all vars are in formula and vice versa
    formula = "time_together ~ edges + mutual + edgecov(education)" # this model has converged
    vars = {"time_together": time_together, "education": education_covMatrix}
    
    # model definition and parameters
    ergm = pyERGM(installed_packages['ergm'], formula, vars)
    params = dict({"formula": ergm.formula}) # make sure to include = for parameters that require = vs parameters that can be upacked such as formula
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