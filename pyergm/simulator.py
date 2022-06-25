from r_setup import intializeRenv
import rpy2.robjects as robjects
from rpy2.robjects import Formula

class Simulator:

    def __init__(self, model, params):
        # TODO: allow users to set seed 
        # R: set.seed(314159)
        self._model = model
        self._params = params
        self._renv = intializeRenv()
        self._sims = None

    def simulate(self, n=1000):
        # TODO check if self._params is empty what would ** return.
        self._sims = self._renv.load_robject('simulate')(self._model, nsim=n, **self._params)
        return self._sims

    def get_triangles(self):
        robjects.globalenv['sim_data']= self._sims
        tri = []
        for index, _ in enumerate(self._sims):
            formula = Formula("sim_data[[i]]~ triangle")
            formula.environment['i'] = index+1
            val = self._renv.load_robject('summary')(formula)[0]
            tri.append(val)
        return tri