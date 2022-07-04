#TODO: check if modelObject can be removed from the init params.

from rpy2.robjects import Formula
from rpy_infterace import intializeRenv
from helper import timer_func
import logging

class pyERGM:
    """python interface to statnet ERGM model
    """

    def __init__(self, modelObject, model_def, vars):
        """
        Args:
            modelObject (R object): ERGM model object in R
            model_def (string): ERGM model definition in a formual per R implementation DV ~ IV1 + IV2 + IV3 etc.
            vars (dict): keys are terms defined in model_def and values are their correspodning objects
        """
        self.model = modelObject.ergm
        self.formula = Formula(model_def)
        self.ergm_params = self.formula.environment
        self._renv = intializeRenv()
        # populate values used in formula as env variables
        for key, val in vars.items():
            self.ergm_params[key] = val
    
    @timer_func
    def fit_model(self, params):
        """Fitting ERGM model over params

        Args:
            params (dict): formula defining ERGM model

        Returns:
            R-Object: ERGM fitted model
        """
        logging.info("Fitting ERGM model...")
        return self.model(**params)

    @timer_func
    def summary(self, model):
        """Summarize ERGM model

        Args:
            model (R object): ERGM model object

        Returns:
            R-Object: summary statistics of the ERGM model
        """
        logging.info("Summarizing model...")
        texreg = self._renv.package_importer(['texreg'])['texreg']
        model_summary = texreg.screenreg(self._renv.load_robject('list')(model))
        return model_summary


class ModelDiagnostics:
    """ModelDiagnostics class provides auxiliary functions for model diagnostics
    """
    def __init__(self, renv):
        """
        Args:
            renv (R Object): R environment object
        """
        self._renv = renv

    @timer_func
    def run_mcmc(self, model, to_pdf = True, pdf_path = "./output/"):
        """function to run MCMC simulations and generate MCMC diagnostic report

        Args:
            model (R-Object): ERGM model object
            to_pdf (bool, optional): option to generate MCMC diagnostic report in PDF format. Defaults to True.
            pdf_path (str, optional): path to write the diagnostic report to. Defaults to "./".

        Returns:
            string: MCMC diagnostics
            string: path to where diagnostic file is written to
        """
        logging.info("Running MCMC diagnostics...")
        if not to_pdf:
            return self._renv.load_robject('mcmc.diagnostics')(model), None

        filepath = pdf_path + "mcmc_diagnostics.pdf"
        self._renv.load_robject('pdf')(filepath)
        mcmc_results = self._renv.load_robject('mcmc.diagnostics')(model)
        self._renv.load_robject('dev.off')()
        return filepath, mcmc_results
    
    @timer_func
    def gof (self, model, params, path= "./output/", n=200):
        """ERGM goodness of fit test and report

        Args:
            model (R-Object): ERGM model object
            params (dict): simulation parameters
            path (str, optional): Path to write goodness of fit report to. Defaults to "./".
            n (int, optional): Number of simulations. Defaults to 200.

        Returns:
            R-Object: goodness of fit R object
        """
        #TODO: check if params has control as a key otherwise assign the value of n to control
        logging.info("Running goodness of fit test...")
        filepath = path + "gof_report.png"
        gof_params =  params
        gof_params["control"] = self._renv.load_robject('control.gof.ergm')(nsim=n)
        imported_pkg = self._renv.package_importer(['grDevices'])
        gof = self._renv.load_robject('gof')(model, **gof_params)
        imported_pkg['grDevices'].png(filepath)
        self._renv.load_robject('plot')(gof)
        imported_pkg['grDevices'].dev_off()
        return gof