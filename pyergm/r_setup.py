import logging
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import StrVector
import rpy2.robjects.packages as rpackages
from rpy2.robjects import Formula
import rpy2.robjects as robjects

class intializeRenv:
    def __init__(self, mirror=1, r_packages=None) -> None:
        # r mirror
        self.mirror = mirror
        self.packages = r_packages if r_packages else []
        self._rpackages_dict = {}

    def setup_renv(self):
        utils = importr('utils')
        utils.chooseCRANmirror(ind=self.mirror)
        rpackage_list = self.setup_packages(utils)
        self._rpackages_dict = self.package_importer(rpackage_list)
        return self._rpackages_dict

    def package_importer(self, rpackages):
        rpackages_dict = {}
        for pname in rpackages:
            rpackages_dict.update({pname: importr(pname)})
        return rpackages_dict

    def setup_packages(self, utils):
        if len(self.packages) > 0:
            for pname in self.packages:
                if not rpackages.isinstalled(pname):
                    utils.install_packages(StrVector(pname))
                    logging.info("Successfully installed {} package".format(pname))
        return self.packages
 
    def load_robject(self, robject_name):
       return robjects.r[robject_name]

