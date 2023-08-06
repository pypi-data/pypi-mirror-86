import pandas as pd
import numpy as np
from scipy.stats import mode



def  flooring_capping(df,variable):
	a=df[variable].quantile(0.10)
	b=df[variable].quantile(0.90)
	df[variable]=np.where(df[variable]<a,a,df[variable])
	df[variable]=np.where(df[variable]>b,b,df[variable])



def trimming(df,variable):
	index = df[(df[variable] >= max(df[variable]))|(df[variable] <= df[variable])].index
	df.drop(index, inplace=True)




def iqr(df,variable):
	Q1=df[variable].quantile(0.25)
	Q3=df[variable].quantile(0.75)
	IQR=Q3-Q1
	df_out = df[~((df[variable] < (Q1 - 1.5 * IQR)) |(df[variable]> (Q3 + 1.5 * IQR)))]
	



def logarithem(df,variable):
	df[variable] = df[variable].map(lambda i: np.log(i) if i > 0 else 0) 



def median(df,variable):
	a=df[variable].quantile(0.50)
	b=df[variable].quantile(0.95)
	df[variable]=np.where(df[variable]>b,a,df[variable])

