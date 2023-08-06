from scipy.stats import boxcox
import seaborn as sns 


def log_transform(df,feature):
	bx=np.log(df[feature]+1)
	return pd.DataFrame(bx)


def reciprocal_transform(df,feature):
	bx=1/(df[feature]+1)
	return pd.DataFrame(bx)


def square_root_transform(df,feature):
	bx=df[feature]**(1/2)
	return pd.DataFrame(bx)


def exponential_transform(df,feature):
	bx=df[feature]**(1/5)
	return pd.DataFrame(bx)


def boxcox_transform(df,feature):
	bx,parameter=boxcox(df[feature])
	return bx


def box_plot(df,feature):
	sns.boxplot(df[feature])



def MinMaxScaler(df):
	for i in df:
		min1=min(df[i])
		max1=max(df[i])
		for j in df[i]:
			scale=(j-min1)/(max1-min1)
			df[i]=np.where(df[i]==j,scale,df[i])



def StandardScaler(df):
	for i in df:
		mean=df[i].mean()
		std=df[i].std()
		for j in df[i]:
			scale=(j-mean)/std
			df[i]=np.where(df[i]==j,scale,df[i])


