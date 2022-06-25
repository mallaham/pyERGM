from rpy2.robjects.conversion import localconverter 
from rpy2.robjects import pandas2ri
import rpy2.robjects as robjects

class DataTransformer:
    def __init__(self):
        pass

    def to_rdf (self, df):
        with localconverter(robjects.default_converter + pandas2ri.converter):
            r_df = robjects.conversion.py2rpy(df)
            return r_df

    
    def rdf_to_list(self, df, colname=None):
        df_to_list = robjects.r['list'] # returns the list as an element of a list (a list within a list)
        unlist_rlist= robjects.r['unlist'] # returns the actual list
        if colname:
            return unlist_rlist(df_to_list(df.rx2(colname)))
        return unlist_rlist(df_to_list(df))