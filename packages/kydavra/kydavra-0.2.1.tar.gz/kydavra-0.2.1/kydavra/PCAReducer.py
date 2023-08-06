'''
Created with love by Sigmoid

@Author - Păpăluță Vasile - vpapaluta06@gmail.com
@Author - Stojoc Vladimir - stojoc.vladimir@gmail.com
'''
import pandas as pd
from .errors import NotBetweenZeroAndOneError
from sklearn.decomposition import PCA

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

class PCAReducer():
    def __init__(self, min_corr : float = 0.5, max_corr : float = 0.8, correlation_type : str = "pearson"):
        '''
            Setting up the algorithm
        :param min_corr: float, between 0 and 1, default = 0.5
            The minimal positive correlation value that must the feature have with y_column
        :param max_corr: float, between 0 and 1, default = 0.8
            The maximal positive correlation value that must the feature have with y_column
        :param correlation_type: str, default = "pearson" 
        '''
        try:
            if min_corr < 0 or max_corr > 1:
                raise NotBetweenZeroAndOneError
        except NotBetweenZeroAndOneError:
            print("Min or Max Correlations are not seted between 0 and 1!")
            quit()
        finally:
            self.max_corr = max_corr
            self.min_corr = min_corr
            self.correlation_type = correlation_type

    def index_to_cols(self, index_list):
        '''
            Converting the list of indexes in a list of features that will be picked by the model
        :param index_list: list
            A list of Indexes that should be converted into a list of feature names
        :return: list
            A list with feature names
        '''
        return [self.X_columns[i] for i in index_list]
        

    def reduce(self,dataframe : pd.DataFrame, y_column : str):
        '''
            Reducing the dimensionality of the data
        :param dataframe: pandas DataFrame
             Data Frame on which the algorithm is applied
        :param y_column: string
             The column name of the value that we have to predict
        '''
        #Setting variables
        self.dataframe = dataframe
        self.X_columns = [col for col in dataframe.columns if col != y_column]
        correlated_indexes = []
        #Getting index of label column
        y_column_index = list(dataframe.columns).index(y_column)
        #Creating correlation table
        self.corr_table = dataframe.corr()
        corr_matrix = self.corr_table.values
        #Choosing most important columns
        for i in range(len(corr_matrix[y_column_index])):
            if abs(corr_matrix[y_column_index][i]) > self.min_corr and abs(corr_matrix[y_column_index][i]) < self.max_corr:
                correlated_indexes.append(i)
        self.correlated_cols = self.index_to_cols(correlated_indexes)
        #Creating correlation table for selected columns
        correlated_features_df = dataframe[self.correlated_cols]
        correlated_featurs_matrix = correlated_features_df.corr()
        self.correlated_features = []
        #Selecting most important correlations between features and creting lists of correlations
        for i in range(len(correlated_featurs_matrix)):
            cols = []
            for j in range(len(correlated_featurs_matrix)):
                if abs(correlated_featurs_matrix[self.correlated_cols[i]][self.correlated_cols[j]]) > self.min_corr and abs(correlated_featurs_matrix[self.correlated_cols[i]][self.correlated_cols[j]]) < self.max_corr :  # I also select the col on diagonal because it is also a part of correlation and should be in my array 
                    cols.append(self.correlated_cols[j])
            if len(cols)!=0 :
                cols.append(self.correlated_cols[i])
                cols.sort()
                self.correlated_features.append(cols) 
        #Cleaning selected columns and ordering them by length
        self.correlated_features = [list(item) for item in set(tuple(row) for row in self.correlated_features)]  
        self.correlated_features = sorted(self.correlated_features, key=len, reverse=True)
        self.dictionary = {}
        self.correlated_columns = [] 
        #Creting main dictionary with PCA filters for different correlations
        for i in range(len(self.correlated_features)):
            flag = False
            key = tuple(self.correlated_features[i])
            for j in range(len(self.correlated_features[i])):
                if self.correlated_features[i][j] not in dataframe.columns:
                    flag = True
            if flag:
                continue
            #Creating algorithm for every correlation
            self.correlated_columns.append(self.correlated_features[i]) # addding realy changed columns
            correlated_features_PCA_df = dataframe[self.correlated_features[i]].values
            pca = PCA(n_components = 1)
            pca.fit(correlated_features_PCA_df)
            X_pca = pca.transform(correlated_features_PCA_df)
            #Creating new column and adding it to dataframe
            column_name = "|".join(key)
            dataframe[column_name] = X_pca
            self.dictionary[key] = pca
            #Deleting correlated columns
            for j in range(len(self.correlated_features[i])):
                dataframe = dataframe.drop(self.correlated_features[i][j],1)
        return dataframe
    
    def apply(self, dataframe : pd.DataFrame, y_column : str):
        '''
            Reducing the dimensionality of the data
            based on an already existed filter
        :param dataframe: pandas DataFrame
             Data Frame on which the algorithm is applied
        :param y_column: string
             The column name of the value that we have to predict
        '''
        for i in range(len(self.correlated_columns)):
            correlated_features_PCA_df = dataframe[self.correlated_columns[i]].values
            column_name = "|".join(self.correlated_columns[i])
            pca = self.dictionary[column_name]
            X_pca = pca.transform(correlated_features_PCA_df)
            dataframe[column_name] = X_pca
            for j in range(len(self.correlated_features[i])):
                dataframe = dataframe.drop(self.correlated_columns[i][j],1)
        return dataframe