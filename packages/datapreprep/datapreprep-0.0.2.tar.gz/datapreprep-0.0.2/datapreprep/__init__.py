import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.impute import KNNImputer


def treat_mean(df):
    clean_df=(df.fillna(df.mean()))
    clean_df.fillna(clean_df.select_dtypes(include='object').mode().iloc[0], inplace=True)
    return clean_df


def info(df):
    num_col =list(df.select_dtypes(include='float64').columns)
    print("The Percenatge of Value Missing in Given Data is : {:.3f}%".format((df.isna().sum().sum())/(df.count().sum())*100))
    print("\nThe Percenatge of Value Missing  in each column of  Given Data is :\n{}".format((df.isnull().sum()*100)/df.shape[0]))
    print('')
    print('Shape of dataframe (Rows, Columns): ',df.shape) # df.shape returns number of row,number of columns in form of tuple for the imported dataset 
    print('')
    print('Data description :\n',df.describe()) 
    total_column=dict((df.dtypes))
    total_column_set=set(total_column.keys())
    numerical_column_set=set(dict(df.median()).keys())
    categorical_column=list(total_column_set-numerical_column_set)
    print("The Categorical Data we have :",categorical_column)
    print('')
    print('Shape of dataframe (Rows, Columns): ',df.shape)
    print('')
    
    
    
def treat_median(df):
    
    clean_df=(df.fillna(df.median()))
    clean_df.fillna(clean_df.select_dtypes(include='object').mode().iloc[0], inplace=True)
    return clean_df



def treat_mode(df):
    clean_df=(df.fillna(df.mode().iloc[0]))
    return clean_df



def treat_knn(df,n=1):
    num_col =list(df.select_dtypes(include='float64').columns)
    knn =KNNImputer(n_neighbors =n,add_indicator =True)
    knn.fit(df[num_col])
    knn_impute =pd.DataFrame(knn.transform(df[num_col]))
    df[num_col]=knn_impute.iloc[:,:df[num_col].shape[1]]
    clean_df= df
    return clean_df



def ot_iqr(df,column_name):
    q1 = df[column_name].quantile(0.25)
    q3 = df[column_name].quantile(0.75)
    IQR = q3 - q1
    lower_limit = q1 - 1.5*IQR
    upper_limit = q3 + 1.5*IQR
    removed_outlier = df[(df[column_name] > lower_limit) & (df[column_name] < upper_limit)] 
    return removed_outlier



def ot_zscore(df,column_name):
    df['z-score'] = (df[column_name]-df[column_name].mean())/df[column_name].std() #calculating Z-score
    outliers = df[(df['z-score']<-1) | (df['z-score']>1)]   #outliers
    removed_outliers = pd.concat([df, outliers]).drop_duplicates(keep=False)   #dataframe after removal
    return removed_outliers



def f_standardscalar(df):
    X = df.select_dtypes(include=np.number)
    mean_X = np.mean(X)
    std_X = np.std(X)
    Xstd = (X - np.mean(X))/np.std(X)
    return Xstd



def f_minmax(df):
    X = df.select_dtypes(include=np.number)
    min_X = np.min(X)
    max_X = np.max(X)
    Xminmax = (X - X.min(axis = 0)) / (X.max(axis = 0) - X.min(axis = 0))
    return Xminmax


def f_robustscalar(df):
    X = df.select_dtypes(include=np.number)
    median_X = np.median(X)
    q3=X.quantile(0.75)-X.quantile(0.25)
    Xrs =(X - np.median(X))/q3
    return Xrs


def f_maxabs(df):
    X = df.select_dtypes(include=np.number) 
    max_abs_X = np.max(abs(X)) 
    Xmaxabs = X /np.max(abs(X))
    return Xmaxabs


def missing_values(df,types):
    if types == mean:
        clean_df=(df.fillna(df.mean()))
        clean_df.fillna(clean_df.select_dtypes(include='object').mode().iloc[0], inplace=True)
        return clean_df
    
    if types == median:
        clean_df=(df.fillna(df.median()))
        clean_df.fillna(clean_df.select_dtypes(include='object').mode().iloc[0], inplace=True)
        return clean_df
        
        
    if types == mode:
        clean_df=(df.fillna(df.mode().iloc[0]))
        return clean_df
        
  
        
        
