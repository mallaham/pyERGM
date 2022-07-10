from mimetypes import init
from rpy2.robjects.conversion import localconverter 
from rpy2.robjects import pandas2ri
import rpy2.robjects as robjects
import logging

class DataTransformer:
    """DataTransformer handles data transofrmation between R and Python, and vice versa.
    """

    def __init__(self, renv):
        """
        Args:
            renv (Robject): instance of an R-object used to load R objects
        """
        self._renv = renv

    def to_rdf (self, df):
        """transform a pandas dataframe to an R dataframe

        Args:
            df (DataFrame): dataframe containing data

        Returns:
            R DataFrame: dataframe in R containing the same data as in df
        """

        logging.info("Converting pandas DataFrame to R dataframe...")
        with localconverter(robjects.default_converter + pandas2ri.converter):
            r_df = robjects.conversion.py2rpy(df)
            return r_df

    def rdf_to_list(self, df, colname=None):
        """transform an R dataframe to an R list by flattening the dataframe on colname. 
        This is useful when setting network attributes.

        Args:
            df (R DataFrame): R dataframe containing network data
            colname (string, optional): Column name on which to faltten the dataframe on. Defaults to None.

        Returns:
            R-list: R list containing df values falttened on colname
        """

        logging.info("Converting R dataframe to R list...")
        # returns the list as an element of a list (a list within a list)
        df_to_list = robjects.r['list']
        # returns the actual list
        unlist_rlist= robjects.r['unlist']
        if colname:
            return unlist_rlist(df_to_list(df.rx2(colname)))
        return unlist_rlist(df_to_list(df))

    def edgelist_to_matrix(self, rdf):
        """convert an edgelist to a matrix. Useful when generating a 
        covariance matrix from an edgelist as part of an ergm model

        Args:
            rdf (R DataFrame): R DataFrame containing edgelist

        Returns:
            R-Matrix: R matrix representing the passed edgelist 
        """

        logging.info("Generating a matrix from edgelist...")
        asmatrix = self._renv.load_robject('as.network.matrix')
        return asmatrix(rdf, **{"matrix.type":"edgelist"})
    
    def adjacency_to_matrix(self, rdf):
        """convert an adjacency matrix to a matrix. Useufl when generating
        a covariance matrix from an adjacency matrix

        Args:
            rdf (R DataFrame): dataframe containing adjacency matrix

        Returns:
            R-Matrix: R matrix represennting the passed adjacency matrix
        """
        
        logging.info("Generating a matrix from adjacency matrix...")
        asmatrix = self._renv.load_robject('as.network.matrix')
        return asmatrix(rdf, **{"matrix.type":"adjacency"})

    def cov_matrix(self, data, from_col, to_col, nrows, ncols, init_val=0.0, cov_col=None):
        """construct a covariance matrix based on a network attribute passed in cov_col.
        If cov_col is not passed, an initialzed matrix with values init_val will be returned. 

        Args:
            data (DataFrame): pandas DataFrame containing network ties in the data. Usually in the format senderId, receiverId,
             attribute(1/0)
            from_col (string): column name that represents the source of the nomination (sender)
            to_col (string): column name that represents the targe of the nomination (receiver)
            cov_col (string, optional): column to construct the covariance matrix on
            nrows (int): number of rows in the covariance matrix
            ncols (int): number of columns in the covariance matrix
            init_val (float, optional): values to initialize the matrix on. It can be either a zero matrix or of type NA_Real. 
             Defaults to 0.0 but can also be NA_Real.

        Returns:
            R Matrix: covariance matrix based on a network attribute 
        """

        logging.info("Generating covariance matrix for: {}".format(cov_col))
        base = self._renv.package_importer(['base'])['base']
        matrix = base.matrix(init_val, nrows, ncols)
        
        # used to initialize a matrix
        if not cov_col:
            logging.info("No covariance column was passed. Returning a matrix with populated values of {}".format(str(init_val)))
            return matrix

        for index, row in data.iterrows(): # make sure all columns are empty of strings or throw an error/execption
            try:
                s_idx = int(row[from_col].replace("G",""))
                r_idx = int(row[to_col].replace("G",""))
            except ValueError:
                print("make sure sender and receiver ids are numbers only")
                exit(1)
            isNan = robjects.r['as.integer'](self._renv.load_robject('is.nan')(row[cov_col]))
            if isNan[0]==1:
                matrix.rx[self._renv.load_robject('cbind')(s_idx,r_idx)] = float(0)
            else:
                matrix.rx[self._renv.load_robject('cbind')(s_idx,r_idx)] = float(row[cov_col])
        matrix_dim = self._renv.load_robject('dim')(matrix)
        if matrix_dim[0] != 0:
            print("covariance matrix has dimension: ", matrix_dim)
        return matrix

    def set_vertex_attribute(self, network, attribute_name, attribute_values):
        """function to set vertix as an attribute

        Args:
            network (R-Matrix): matrix representation of the adjacency matrix or edgelist in R
            attribute_name (string or list of strings): name of the attribute
            attribute_values (R-List or list of R-Lists): values associated with the attribute in an R-List format

        Returns:
            R-Object: network with attribute_name set as network attribute
        """
        #### examples
        # set attributes (options)
        # set_vertex_att = renv.load_robject('set.vertex.attribute')
        # buyIn = set_vertex_att(buyIn, "education", education) # Categorical variable for department
        # buyIn = set_vertex_att(buyIn, "have_child", have_child) # Indicator variable for department leader
        # buyIn = set_vertex_att(buyIn, "marital_status",marital_status) # Years tenure
        ###
        
        if (type(attribute_name)==list and type (attribute_name)==list):
            if len(attribute_name) != len(attribute_values):
                logging.error("Length of attribute names and values do not match. Exiting...")
                exit(1)
            logging.info("A list of attribute names and values was passed...")
            for index, _ in enumerate(attribute_name):
                logging.info("Setting vertex attribute to {}...".format(attribute_name[index]))
                set_vertex_r_func = self._renv.load_robject('set.vertex.attribute')
                network = set_vertex_r_func(network, attribute_name[index], attribute_values[index])
            return network
        
        logging.info("Setting vertex attribute to {}...".format(attribute_name))
        set_vertex_r_func = self._renv.load_robject('set.vertex.attribute')
        network = set_vertex_r_func(network,attribute_name, attribute_values)
        return network
