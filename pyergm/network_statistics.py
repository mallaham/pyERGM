from rpy_interface import intializeRenv
import logging 

class NetworkStats:
    """NetworkStats offers methods to calculate network statistics
    """
    def __init__(self, renv):
        self._renv = renv

    # def get_network_stats(self,network):
    #    # call all defined functions in this class and put it in a table
    #     
    def summary(self, network):
        """summarize network statistics

        Args:
            network (R-Object): network represented in as a matrix 

        Returns:
            R-Object: summary statistics of the network
        """
        logging.info("Calculating network summary statistics...")
        return self._renv.load_robject('summary')(network)

    def network_size(self,network):
        """function to calculate network size

        Args:
            network (R-Matrix): R matrix representation of the network

        Returns:
            int: network size
        """
        logging.info("Calculating network size...")
        return self._renv.load_robject('network.size')(network)
    
    def betweeness(self,network):
        """Calculate betweeness score

        Args:
            network (R-Matrix): R matrix representation of the network

        Returns:
            R-Object: betweeness score for all nodes in the network
        """
        logging.info("Calculating network betweenness...")
        return self._renv.load_robject('betweenness')(network)

    def isolates(self, network):
        """Count the number of isolates in the network

        Args:
            network (R-Matrix): R matrix representation of the network

        Returns:
            R-Object: number of isolates in the network
        """
        logging.info("Calculating number of isolates in the network...")
        return self._renv.load_robject('isolates')(network)

    
