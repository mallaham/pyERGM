# local testing
import rpy_interface as rpyInterface
from network_statistics import NetworkStats
from ergm import pyERGM, ModelDiagnostics
from ergm import pyERGM
from simulator import Simulator
from data_transformer import DataTransformer
from rpy2.robjects import Formula
# from pyergm import rpy_interface as rpyInterface
# from pyergm.network_statistics import NetworkStats
# from pyergm.ergm import pyERGM, ModelDiagnostics
# from pyergm.simulator import Simulator
# from pyergm.data_transformer import DataTransformer
import pandas as pd
import os
from rpy2.robjects import NA_Real

if __name__ == "__main__":
    
    rpackages = ['statnet', 'ergm','texreg', 'base', 'grDevices'] # removing igraph because it causes issues with ergm native functions
    renv = rpyInterface.intializeRenv(mirror=1, r_packages= rpackages)
    installed_packages = renv.setup_renv()

    attributes = pd.read_csv("/Users/Mowafak/Downloads/nodes_q13_11.csv")
    edgelist = pd.read_csv("/Users/Mowafak/Downloads/matrix_q13_.csv",index_col=0)

    dt = DataTransformer(renv)
    attributes_rdf = dt.rdf_to_list(dt.to_rdf(attributes))
    edgelist_rdf = dt.to_rdf(edgelist)

    age_ego = renv.load_robject("as.numeric")(dt.rdf_to_list(dt.to_rdf(attributes['age_ego'].to_frame(name="age_ego")), "age_ego"))
    # education_ego = renv.load_robject("as.numeric")(dt.rdf_to_list(dt.to_rdf(attributes['education_ego'].to_frame(name="education_ego")), "education_ego"))
    education_ego = dt.rdf_to_list(dt.to_rdf(attributes['education_ego'].to_frame(name="education_ego")), "education_ego")
    nationality_ego = dt.rdf_to_list(dt.to_rdf(attributes['nationality_ego'].to_frame(name="nationality_ego")), "nationality_ego")
    # race_ego = renv.load_robject("as.numeric")(dt.rdf_to_list(dt.to_rdf(attributes['race_ego'].to_frame(name="race_ego")), "race_ego"))
    race_ego = dt.rdf_to_list(dt.to_rdf(attributes['race_ego'].to_frame(name="race_ego")), "race_ego")
    # sex_ego = renv.load_robject("as.numeric")(dt.rdf_to_list(dt.to_rdf(attributes['sex_ego'].to_frame(name="sex_ego")), "sex_ego"))
    sex_ego = dt.rdf_to_list(dt.to_rdf(attributes['sex_ego'].to_frame(name="sex_ego")), "sex_ego")
    ass_age_egonet_2 = dt.rdf_to_list(dt.to_rdf(attributes["ass_age_egonet_2"].to_frame(name="ass_age_egonet_2")), "ass_age_egonet_2")
    ass_race_egonet_2 = dt.rdf_to_list(dt.to_rdf(attributes["ass_race_egonet_2"].to_frame(name="ass_race_egonet_2")), "ass_race_egonet_2")
    ass_edu_egonet_2 = dt.rdf_to_list(dt.to_rdf(attributes["ass_edu_egonet_2"].to_frame(name="ass_edu_egonet_2")), "ass_edu_egonet_2")
    ass_sex_egonet_2 = dt.rdf_to_list(dt.to_rdf(attributes["ass_sex_egonet_2"].to_frame(name="ass_sex_egonet_2")), "ass_sex_egonet_2")
    Team_id = dt.rdf_to_list(dt.to_rdf(attributes["Team_id"].to_frame(name="Team_id")), "Team_id")

    buyIn = dt.adjacency_to_matrix(edgelist_rdf)

    buyIn = dt.set_vertex_attribute(buyIn,["age_ego","education_ego","nationality_ego","race_ego",
     "sex_ego","ass_age_egonet_2","ass_race_egonet_2", "ass_edu_egonet_2","ass_sex_egonet_2","Team_id"],
      age_ego, education_ego, nationality_ego, race_ego, sex_ego, ass_age_egonet_2, ass_race_egonet_2, ass_edu_egonet_2,
      ass_sex_egonet_2, Team_id)
    
    # buyIn = dt.set_vertex_attribute(buyIn, "age_ego",age_ego)
    # buyIn = dt.set_vertex_attribute(buyIn, "education_ego",education_ego)
    # buyIn = dt.set_vertex_attribute(buyIn, "nationality_ego",nationality_ego)
    # buyIn = dt.set_vertex_attribute(buyIn, "race_ego",race_ego)
    # buyIn = dt.set_vertex_attribute(buyIn, "sex_ego",sex_ego)
    # buyIn = dt.set_vertex_attribute(buyIn, "ass_age_egonet_2",ass_age_egonet_2)
    # buyIn = dt.set_vertex_attribute(buyIn, "ass_race_egonet_2",ass_race_egonet_2)
    # buyIn = dt.set_vertex_attribute(buyIn, "ass_edu_egonet_2",ass_edu_egonet_2)
    # buyIn = dt.set_vertex_attribute(buyIn, "ass_sex_egonet_2",ass_sex_egonet_2)
    # buyIn = dt.set_vertex_attribute(buyIn, "Team_id",Team_id)

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
    formula= "buyIn ~ edges + mutual + gwesp(0.5, fixed = TRUE) + absdiff('age_ego') + absdiff('education_ego') + nodemix('nationality_ego') + nodematch('race_ego') + nodematch('sex_ego', diff = F) + nodecov('ass_age_egonet_2') + nodecov('ass_race_egonet_2') + nodecov('ass_edu_egonet_2') +nodecov('ass_sex_egonet_2')"
    # formula = "buyIn ~ edges + mutual + edgecov(hundreds_messages) + nodemix('leader',base = 3)"
    vars = {"buyIn": buyIn, "age_ego":age_ego, "education_ego":education_ego, "nationality_ego":nationality_ego, "race_ego":race_ego, "sex_ego":sex_ego, "ass_age_egonet_2":ass_age_egonet_2, "ass_race_egonet_2":ass_race_egonet_2,"ass_edu_egonet_2":ass_edu_egonet_2,"ass_sex_egonet_2":ass_sex_egonet_2, "Team_id":Team_id}
    # vars = {"buyIn": buyIn}
    
    # model definition and parameters
    # x = renv.load_robject("as.formula")(formula+", constraints=~ blockdiag('Team_id') + bd(maxout=3, maxin=3), verbose=F")
    # ergm = pyERGM(installed_packages['ergm'], x , vars)
    ergm = pyERGM(installed_packages['ergm'], formula , vars, constraints="~blockdiag('Team_id') + bd(maxout=3, maxin=3)")
    params=dict({"formula":ergm.formula, "constraints": ergm.constraints})
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