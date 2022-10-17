import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import StrVector
import rpy2.robjects.packages as rpackages
from rpy2.robjects import Formula
from mimetypes import init
import logging

class intializeRenv:
    """Setup and initialize R environment
    """
    
    def __init__(self, mirror=1, r_packages=['statnet', 'ergm','texreg', 'base', 'grDevices']):
        """_summary_

        Args:
            mirror (int, optional): _description_. Defaults to 1.
            r_packages (list, optional): R packages that must be installed. Defaults to ['statnet', 'ergm','texreg', 'base', 'grDevices'].
        """
        self.mirror = mirror
        self.packages = r_packages if r_packages else []
        self._rpackages_dict = {}

    def setup_renv(self):
        """helper function to setup R env

        Returns:
            dict: dictionary of R objects. Keys are package names and values are correspoding R objects
        """
        utils = importr('utils')
        utils.chooseCRANmirror(ind=self.mirror)
        rpackage_list = self.setup_packages(utils)
        self._rpackages_dict = self.package_importer(rpackage_list)
        return self._rpackages_dict

    def package_importer(self, rpackages):
        """Import R packages

        Args:
            rpackages (_type_): _description_

        Returns:
            dict: dictionary of R objects. Keys are package names and values are correspoding R objects
        """
        rpackages_dict = {}
        for pname in rpackages:
            logging.info("Importing package: {}".format(pname))
            if "=" in pname:
                rpackages_dict.update({pname.split("=")[0]: importr(pname.split("=")[0])})
            rpackages_dict.update({pname: importr(pname)})
        return rpackages_dict

    def setup_packages(self, utils):
        """helper function to setup R packages

        Args:
            utils (object): R object of package utils used to install pacakges

        Returns:
            list: installed pacakges
        """
        logging.info("Installing R packages...")
        if len(self.packages) > 0:
            for pname in self.packages:
                if not rpackages.isinstalled(pname):
                    if "=" in pname:
                        v = importr('devtools')
                        pname, version = pname.split("=")
                        print(pname)
                        v.install_version('package='.format(StrVector(pname)), StrVector(version))
                        logging.info("Successfully installed {} package".format(pname))
                        continue    
                    utils.install_packages(StrVector(pname))
                    logging.info("Successfully installed {} package".format(pname))
        return self.packages
 
    def load_robject(self, robject_name):
        """helper function to load R objects

        Args:
            robject_name (string): R package name

        Returns:
            R-object: R object that matches robject_name. 
            Note: this must match with package names in R
        """
        return robjects.r[robject_name]