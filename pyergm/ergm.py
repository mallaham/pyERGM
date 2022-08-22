from rpy2.robjects import Formula
from .rpy_interface import intializeRenv
from .helper import timer_func
# from rpy_interface import intializeRenv
# from helper import timer_func
import pandas as pd
import rpy2.robjects as robjects
import logging


class pyERGM:
    """python interface to statnet ERGM model
    """

    def __init__(self, modelObject, model_def, vars, constraints=None):
        """
        Args:
            modelObject (R object): ERGM model object in R
            model_def (string): ERGM model definition in a formual per R implementation DV ~ IV1 + IV2 + IV3 etc.
            vars (dict): keys are terms defined in model_def and values are their correspodning objects
            constraints (string): ergm constraints to include and consider as part of modeling
        """
        self.model = modelObject.ergm
        self.formula = Formula(model_def)
        self.constraints = Formula(constraints) if constraints else None
        self.ergm_params = self.formula.environment
        self._renv = intializeRenv()
        # populate values used in formula as env variables
        for key, val in vars.items():
            self.ergm_params[key] = val
        self.model_descriptive_summary(self.formula)
        
    def model_descriptive_summary(self, formula):
        """describing model summary before fitting

        Args:
            formula (R-object): ERGM model equation which consists of model terms that will be used to fit the ERGM model.
        """
        logging.info("Model summary before fitting ERGM...")
        summary=robjects.r['as.data.frame'](self._renv.load_robject('summary')(self.formula))
        summary_df = robjects.pandas2ri.rpy2py(summary)
        logging.info(summary_df)
        return summary_df

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
        """ERGM model after fitting

        Args:
            model (R object): ERGM model object or a list of models to compare

        Returns:
            R-Object: summary statistics of the ERGM model
        """
        logging.info("ERGM model summary...")
        texreg = self._renv.package_importer(['texreg'])['texreg']
        model_summary =  texreg.screenreg(model) if type(model)==list else texreg.screenreg(self._renv.load_robject('list')(model))
        return model_summary


class ModelDiagnostics:
    """ModelDiagnostics class provides auxiliary functions for model diagnostics
    """
    def __init__(self, renv, seed=321):
        """
        Args:
            renv (R Object): R environment object
        """
        self._renv = renv
        self._seed = seed

    @timer_func
    def run_mcmc(self, model, to_pdf = True, pdf_path = "./"):
        """function to run MCMC simulations and generate MCMC diagnostic report

        Args:
            model (R-Object): ERGM model object
            to_pdf (bool, optional): option to generate MCMC diagnostic report in PDF format. Defaults to True.
            pdf_path (str, optional): path to write the diagnostic report to. Defaults to "./".

        Returns:
            string: MCMC diagnostics
            string: path to where diagnostic file is written to
        """
        logging.info("Running MCMC diagnostics with seed {}...".format(self._seed))
        self._renv.load_robject('set.seed')(self._seed)
        if not to_pdf:
            return self._renv.load_robject('mcmc.diagnostics')(model), None

        filepath = pdf_path + "mcmc_diagnostics.pdf"
        self._renv.load_robject('pdf')(filepath)
        mcmc_results = self._renv.load_robject('mcmc.diagnostics')(model)
        self._renv.load_robject('dev.off')()
        logging.info("MCMC diagnostic report can be accessed in the following path: {}".format(filepath))
        return filepath, mcmc_results
    
    @timer_func
    def gof (self, model, params, path= "./", n=200):
        """ERGM goodness of fit test and report

        Args:
            model (R-Object): ERGM model object
            params (dict): simulation parameters
            path (str, optional): Path to write goodness of fit report to. Defaults to "./".
            n (int, optional): Number of simulations. Defaults to 200.

        Returns:
            R-Object: goodness of fit R object
        """
        logging.info("Running goodness of fit test...")
        filepath = path + "gof_report.png"
        gof_params =  params
        gof_params["control"] = self._renv.load_robject('control.gof.ergm')(nsim=n)
        imported_pkg = self._renv.package_importer(['grDevices'])
        gof = self._renv.load_robject('gof')(model, **gof_params)
        imported_pkg['grDevices'].png(filepath)
        self._renv.load_robject('plot')(gof)
        imported_pkg['grDevices'].dev_off()
        logging.info("Goodness of fit report can be accessed in the following path: {}".format(filepath))
        return gof