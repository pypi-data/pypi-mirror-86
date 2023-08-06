from sklearn.feature_selection import SelectKBest,chi2,f_regression,f_classif
import pandas as pd


class SelectBest:
	def __init__(self,score_func,k):
		self.score_func=score_func
		self.k=k
		self.score=None
		self.X=None

	def fit(self,X,y):
		model=SelectKBest(score_func=self.score_func,k=self.k)
		model.fit(X,y)
		self.score=model.scores_
		self.X=X


	def best_feature(self):
		dfscore=pd.DataFrame(self.score)
		dfcolumn=pd.DataFrame(self.X.columns)
		best_rank_feature=pd.concat([dfcolumn,dfscore],axis=1)
		best_rank_feature.columns=["Features","Score"]
		print(best_rank_feature)



def RemoveCollinearity(dataset, threshold): 
    col_corr = set() # Set of all the names of correlated columns 
    corr_matrix = dataset.corr() 
    for i in range(len(corr_matrix.columns)):
        for j in range(i): 
            if abs(corr_matrix.iloc[i, j]) > threshold: # we are interested in absolute coeff value 
                colname = corr_matrix.columns[i]
                col_corr.add(colname) 
    return col_corr




def cor_selector(X, y):
	feature_name = X.columns.tolist()
    cor_list = []
    # calculate the correlation with y for each feature
    for i in X.columns.tolist():
        cor = np.corrcoef(X[i], y)[0, 1]
        cor_list.append(cor)
    # replace NaN with 0
    cor_list = [0 if np.isnan(i) else i for i in cor_list]
    # feature name
    cor_feature = X.iloc[:,np.argsort(np.abs(cor_list))[-100:]].columns.tolist()
    # feature selection? 0 for not select, 1 for select
    cor_support = [True if i in cor_feature else False for i in feature_name]
    
    cor_feature,cor_list,cor_support=cor_selector(X,y)
	features=pd.DataFrame(cor_feature)
	scores=pd.DataFrame(cor_list)
	cor_support=pd.DataFrame(cor_support)
	df_corr=pd.concat([features,scores,cor_support],axis=1)
	df_corr.columns=["Features","Scores","Support"]
	return df_corr
