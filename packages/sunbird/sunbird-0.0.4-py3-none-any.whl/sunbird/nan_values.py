import pandas as pd
import numpy as np
from scipy.stats import mode
import seaborn as sns


#1
def median_imputation(df,variable,plot=False):
    median=df[variable].median()
    df[variable+"_median"]=df[variable].fillna(median)
    if plot==True:
        sns.kdeplot(df[variable+"_median"])
        sns.kdeplot(df[variable])
    df[variable]=df[variable+"_median"]
    df=df.drop([variable+"_median"],axis=1,inplace=True)



#2
def random_sampler(df,variable,plot=False):
    df[variable+'_random']=df[variable]
    rs=df[variable].dropna().sample(df[variable].isnull().sum(),random_state=0)
    rs.index=df[df[variable].isnull()].index
    df.loc[df[variable].isnull(),variable+'_random']=rs
    if plot==True:
        sns.kdeplot(df[variable+"_random"])
        sns.kdeplot(df[variable])
    df[variable]=df[variable+"_random"]
    df=df.drop([variable+"_random"],axis=1,inplace=True)




#3
def mean_imputation(df,variable,plot=False):
	mean=df[variable].mean()
	df[variable+"_mean"]=df[variable].fillna(mean)
	if plot==True:
		sns.kdeplot(df[variable+"_mean"])
		sns.kdeplot(df[variable])
	df[variable]=df[variable+"_mean"]
	df=df.drop([variable+"_mean"],axis=1,inplace=True)




#4
def mode_imputation(df,variable,plot=False):
	mode=df[variable].mode()
	df[variable+"_mode"]=df[variable].fillna(mode)
	if plot==True:
		sns.kdeplot(df[variable+"_mode"])
		sns.kdeplot(df[variable])
	df[variable]=df[variable+"_mode"]
	df=df.drop([variable+"_mode"],axis=1,inplace=True)




#5
def capture_nan(df,variable):
	df[variable+'_nan']=np.where(df[variable].isnull(),1,0)
	df[variable].median()
	df[variable].fillna(df.variable.median(),inplace=True)




#6
def endof_distribution(df,variable,plot=False):
	extr=df[variable].mean()+3*df[variable].std()
	df[variable+'_enddist']=df[variable].fillna(extr)
	if plot==True:
		sns.kdeplot(df[variable+"_enddist"])
		sns.kdeplot(df[variable])
	df[variable]=df[variable+"_enddist"]
	df=df.drop([variable+"_enddist"],axis=1,inplace=True)




#7
def arbitrary_imputation(df,variable,arbit,plot=False):
	df[variable+'_arbitrary']=df[variable].fillna(arbit)
	if plot==True:
		sns.kdeplot(df[variable+"_arbitrary"])
		sns.kdeplot(df[variable])
	df[variable]=df[variable+"_arbitrary"]
	df=df.drop([variable+"_arbitrary"],axis=1,inplace=True)




#8
def frequent(df,variable):
    most_frequent_category=df[variable].mode()[0]
    df[variable].fillna(most_frequent_category,inplace=True)




#9
def add_variable(df,variable):
	df[variable]=np.where(df[variable].isnull(),1,df[variable])
	frequent=df[variable].mode()[0]
	df[variable].fillna(frequent,inplace=True)




#10
def fill_missing(df,variable):
	df[variable]=np.where(df[variable].isnull(),'Missing',df[variable])