import rpy_infterace as rpyInterface
from network_statistics import NetworkStats
from ergm import pyERGM, ModelDiagnostics
import pandas as pd
from ergm import pyERGM
from simulator import Simulator
from rpy2.robjects import NA_Real
from data_transformer import DataTransformer
import logging 
######
# writing std output to a file
# import sys
# sys.stdout = open('pyergm/output/log.txt', 'w')
# or 
# logging.basicConfig(filename="log.txt", level=logging.DEBUG)
######
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

if __name__ == "__main__":
    
    rpackages = ['statnet', 'ergm','texreg', 'base', 'grDevices'] # removing igraph because it causes issues with ergm native functions
    renv = rpyInterface.intializeRenv(mirror=1, r_packages= rpackages)
    installed_packages = renv.setup_renv()

    buyInFromYouEdgelist = pd.read_csv("data/ergm_SNA_lab/buyInFromYouEdgelist.csv")

    dt = DataTransformer(renv)
    department = dt.rdf_to_list(dt.to_rdf(pd.read_csv("data/ergm_SNA_lab/departmentNode.csv")), "department")
    leader = dt.rdf_to_list(dt.to_rdf(pd.read_csv("data/ergm_SNA_lab/leaderNode.csv")),"leader")
    tenure = dt.rdf_to_list(dt.to_rdf(pd.read_csv("data/ergm_SNA_lab/tenureNode.csv")), "tenure")
    office = dt.rdf_to_list(dt.to_rdf(pd.read_csv("data/ergm_SNA_lab/officeNode.csv")), "office")
    female = dt.rdf_to_list(dt.to_rdf(pd.read_csv("data/ergm_SNA_lab/femaleNode.csv")), "female")
    messageEdgeList = pd.read_csv("data/ergm_SNA_lab/messageEdgelist.csv")
    
    # converting pandas dataframe to r
    r_buyInFromYouEdgelist = dt.to_rdf(buyInFromYouEdgelist)

    # loading edgelist as a matrix
    buyIn = dt.edgelist_to_matrix(r_buyInFromYouEdgelist)

    # set network attributes
    buyIn = dt.set_vertex_attribute(buyIn, ["department","leader","tenure","office","female"], [department, leader, tenure, office, female])
    # alternative method
    # buyIn = dt.set_vertex_attribute(buyIn, "department", department) # Categorical variable for department
    # buyIn = dt.set_vertex_attribute(buyIn, "leader", leader) # Indicator variable for department leader
    # buyIn = dt.set_vertex_attribute(buyIn, "tenure",tenure) # Years tenure
    # buyIn = dt.set_vertex_attribute(buyIn, "office", office) # Indicator variable for whether they are located in the main or secondary office
    # buyIn = dt.set_vertex_attribute(buyIn, "female",female) # Indicator

    cov_matrix = dt.cov_matrix(messageEdgeList, 'SenderId',' ReceiverId', 66, 66, NA_Real)

    # filling matrix with values 
    for index, row in messageEdgeList.iterrows():
        s_idx = int(row['SenderId'])
        r_idx = int(row['ReceiverId'])
        cov_matrix.rx[renv.load_robject('cbind')(s_idx,r_idx)] = float(row['MessagesSent']/100)

    ################################
    ## Calculate network metrics
    ################################
    ns = NetworkStats(renv)
    summary = ns.summary(buyIn)
    print(summary)
    network_size = ns.network_size(buyIn)
    print(network_size)
    betweeness = ns.betweeness(buyIn)
    print(betweeness)
    isolates = ns.isolates(buyIn)
    print(isolates)
    
    # ERGM model
    # formula and input variables
    formula = "buyIn ~ edges + mutual + edgecov(hundreds_messages) + nodemix('leader',base = 3)"
    vars = {"buyIn": buyIn, "hundred_messages": cov_matrix, "hundreds_messages": cov_matrix}
    
    # model definition and parameters
    ergm = pyERGM(installed_packages['ergm'], formula, vars)
    params = dict({"formula":ergm.formula, "constraints=":"~bd(maxout=5)"}) # make sure to include = for parameters that require = vs parameters that can be upacked such as formula
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