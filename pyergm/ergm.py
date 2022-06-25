from rpy2.robjects import Formula
from r_setup import intializeRenv

class pyERGM:

    def __init__(self, modelObject, model_def, vars) -> None:
        self.ergm = modelObject.ergm
        self.formula = Formula(model_def)
        self.ergm_params = self.formula.environment
        self._renv = intializeRenv()
        # populate values used in formula as env variables
        for key, val in vars.items():
            self.ergm_params[key] = val
    
    def summary(self, model):
        texreg = self._renv.package_importer(['texreg'])['texreg']
        model_summary = texreg.screenreg(self._renv.load_robject('list')(model))
        return model_summary

    def mcmc_summary(self, model, to_pdf = True, pdf_path = "./"):
        # runs mcmc diagnostics
        if not to_pdf:
            return self._renv.load_robject('mcmc.diagnostics')(model), None

        filepath = pdf_path + "mcmc_diagnostics.pdf"
        self._renv.load_robject('pdf')(filepath)
        mcmc_results = self._renv.load_robject('mcmc.diagnostics')(model)
        self._renv.load_robject('dev.off')()
        return mcmc_results, filepath
    
    def gof (self, model, params, path= "./", n=200):
        #TODO: check if params has control as a key otherwise assign the value of n to control
        filepath = path + "gof_report.png"
        gof_params =  params
        gof_params["control"] = self._renv.load_robject('control.gof.ergm')(nsim=n)
        imported_pkg = self._renv.package_importer(['grDevices'])
        gof = self._renv.load_robject('gof')(model, **gof_params)
        imported_pkg['grDevices'].png(filepath)
        self._renv.load_robject('plot')(gof)
        imported_pkg['grDevices'].dev_off()
        return gof
