import pandas as pd 
import numpy as np


def frequency_encoding(df,feature):
	map_dict=df[feature].value_counts().to_dict()
	df[feature]=df[feature].map(map_dict)


def target_guided_encoding(df,feature,target):
	order=df.groupby([feature])[target].mean().sort_values().index
	map_dic={k:i for i,k in enumerate(order,0)}
	df[feature]=df[feature].map(map_dic)	



def mean_encoding(df,feature,target):
	map_dict=df.groupby([feature])[target].mean().to_dict()
	df[feature]=df[feature].map(map_dict)



def probability_ratio_encoding(df,feature,target):
	order=df.groupby([feature])[target].mean()
	prob_df=pd.DataFrame(order)
	prob_df['temp']=1-prob_df[target]
	prob_df['encoding']=prob_df[target]/prob_df['temp']
	map_dict=prob_df['encoding'].to_dict()
	df[feature]=df[feature].map(map_dict)


def one_hot(df,feature):
	dummies=pd.get_dummies(df[feature],drop_first=True)
	df=pd.concat([df,dummies],axis=1)


def kdd_cup(df,feature,k=10):
	lst_feature=df[feature].value_counts().sort_values(ascending=False).head(k).index
	lst_10=list(lst_feature)
	for categories in lst_10:
		df[categories]=np.where(df[feature]==categories,1,0)

