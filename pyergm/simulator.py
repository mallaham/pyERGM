from .rpy_interface import intializeRenv
import rpy2.robjects as robjects
from rpy2.robjects import Formula
import logging 

class Simulator:
    """Simulator simulates networks and calcuate statistics on simulated networks for comparison with observed networks
    """

    def __init__(self, model, params, seed=340):
        # TODO: allow users to set seed 
        # R: set.seed(314159)
        self._model = model
        self._params = params
        self._renv = intializeRenv()
        self._sims = None
        self._seed = seed

    def simulate(self, n=1000):
        """function to simulate networks

        Args:
            n (int, optional): number of networks to simulate Defaults to 1000.

        Returns:
            R-Object: an object referencing simulated networks
        """
        # TODO check if self._params is empty what would ** return.
        logging.info("Simulating {} networks with seed vale {}...".format(n, self._seed))
        self._renv.load_robject('set.seed')(self._seed)
        self._sims = self._renv.load_robject('simulate')(self._model, nsim=n, **self._params)
        return self._sims

    def get_triangles(self):
        """Count the number of triangles in simulated networks

        Returns:
            list: number of triangles per simulated network
        """
        logging.info("Counting the number of triangles in the simulated networks...")
        robjects.globalenv['sim_data']= self._sims
        tri = []
        for index, _ in enumerate(self._sims):
            formula = Formula("sim_data[[i]]~ triangle")
            formula.environment['i'] = index+1
            val = self._renv.load_robject('summary')(formula)[0]
            tri.append(val)
        return tri