import r_setup as r
import pandas as pd
from ergm import pyERGM
from simulator import Simulator
from rpy2.robjects import NA_Real
from data_transformer import DataTransformer
import rpy2.robjects as robjects

if __name__ == "__main__":
    
    #rpackages = ['statnet', 'ergm','igraph','texreg']
    rpackages = ['statnet', 'ergm','texreg', 'base', 'grDevices'] # removing igraph because it causes issues with ergm native functions
    renv = r.intializeRenv(mirror=1, r_packages= rpackages)
    installed_packages = renv.setup_renv()

    # import data
    # edge list
    buyInFromYouEdgelist = pd.read_csv("data/buyInFromYouEdgelist.csv")

    dt = DataTransformer()
    department = dt.rdf_to_list(dt.to_rdf(pd.read_csv("data/departmentNode.csv")), "department")
    leader = dt.rdf_to_list(dt.to_rdf(pd.read_csv("data/leaderNode.csv")),"leader")
    tenure = dt.rdf_to_list(dt.to_rdf(pd.read_csv("data/tenureNode.csv")), "tenure")
    office = dt.rdf_to_list(dt.to_rdf(pd.read_csv("data/officeNode.csv")), "office")
    female = dt.rdf_to_list(dt.to_rdf(pd.read_csv("data/femaleNode.csv")), "female")
    messageEdgeList = pd.read_csv("data/messageEdgelist.csv")
    # converting pandas dataframe to r
    r_buyInFromYouEdgelist = dt.to_rdf(buyInFromYouEdgelist)


    # loading R objects and functions
    asmatrix = renv.load_robject('as.network.matrix')
    # transforming r dataframe to a matrix
    buyIn = asmatrix(r_buyInFromYouEdgelist, **{"matrix.type":"edgelist"}) # unpacks parameters from python to R

    # set network attributes
    set_vertex_att = renv.load_robject('set.vertex.attribute')
    buyIn = set_vertex_att(buyIn, "department", department) # Categorical variable for department
    buyIn = set_vertex_att(buyIn, "leader", leader) # Indicator variable for department leader
    buyIn = set_vertex_att(buyIn, "tenure",tenure) # Years tenure
    buyIn = set_vertex_att(buyIn, "office", office) # Indicator variable for whether they are located in the main or secondary office
    buyIn = set_vertex_att(buyIn, "female",female) # Indicator

    # create a matrix
    matrix = installed_packages['base'].matrix(NA_Real, nrow=66, ncol=66)

    # filling matrix with values (possibly add a function to do it to create a matrix
    # by accepting nrows, ncols, and df to edge list)
    for index, row in messageEdgeList.iterrows():
        s_idx = int(row['SenderId'])
        r_idx = int(row['ReceiverId'])
        matrix.rx[renv.load_robject('cbind')(s_idx,r_idx)] = float(row['MessagesSent']/100)

    # load network functions
    summary = renv.load_robject('summary')(buyIn)
    network_size = renv.load_robject('network.size')(buyIn)
    betweeness = renv.load_robject('betweenness')(buyIn)
    isolates = renv.load_robject('isolates')(buyIn)

    ################ Network Visualization (optional)############
    # # igraph functions (for viz)
    # asmatrix_network = renv.load_robject('as.matrix.network')
    # graph_adj = renv.load_robject('graph.adjacency')
    # set_vertex_attr = renv.load_robject('set_vertex_attr')
    # layout_with_fr = renv.load_robject('layout_with_fr')
    # v_function = renv.load_robject('V')

    # buyIn_igraph = graph_adj(asmatrix_network(buyIn))
    # buyIn_igraph = set_vertex_attr(buyIn_igraph,"female",value=female)
    # netlayout = layout_with_fr(buyIn_igraph)

    # # load igraph for network visualization
    # igraph_options = renv.load_robject['igraph_options']
    # igraph_options(**{"vertex.size":9, "vertex.color": 'grey', "edge.color":'gray80', "edge.arrow.size":0.4, "vertex.label": "NA"})
    ############################################################
    # ERGM model
    # formula and input variables
    formula = "buyIn ~ edges + mutual + edgecov(hundreds_messages) + nodemix('leader',base = 3)"
    vars = {"buyIn": buyIn, "hundred_messages": matrix, "hundreds_messages": matrix}
    
    # model definition and parameters
    ergm = pyERGM(installed_packages['ergm'], formula, vars)
    params = dict({"formula":ergm.formula, "constraints=":"~bd(maxout=5)"}) # make sure to include = for parameters that require = vs parameters that can be upacked such as formula
    model = ergm.ergm(**params)
    summary = ergm.summary(model)
    filename, mcmc_results = ergm.mcmc_summary(model)

    # running simulations
    simulate_parms = {"burnin=":100000, "interval=":100000, "verbose=":"T", "seed=":10}
    sim = Simulator(model, simulate_parms)
    sim_results = sim.simulate()

    # goodness of fit
    gof_params = dict({"verbose=":"T","burnin=":1e+5,"interval=":1e+5})
    gof = ergm.gof(model, gof_params, n=100)
    # print(filename)
    print(summary)
    # print(gof)
    print("======")
    print(len(sim.get_triangles()))

# ergm-users
# add summary function of the data before running ergm
# print t-values as part of ergm
# print(gof) object to give you statistics, and extract the p-value
