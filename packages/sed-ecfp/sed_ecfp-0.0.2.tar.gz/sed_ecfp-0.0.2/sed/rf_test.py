import numpy as np
# import matplotlib.pyplot as plt
import csv
from sklearn import datasets, ensemble
from sklearn.model_selection import train_test_split
#Section 3: Evaluate model performance via MSE and R2_Score
from sklearn.metrics import mean_squared_error,r2_score
#from demo_new import selected_file

def load_csv(filename):
	res = []
	with open(filename,'r') as f:
		reader = csv.reader(f)
		for l in reader:
			if len(l) != 0:
				res.append(list(map(float,l)))
				# print(l)
	return np.array(res,dtype=np.float32) #list转ndarray

# 集成学习随机森林RandomForestRegressor回归模型
def test_RandomForestRegressor(*data):
	X_train, X_test, y_train, y_test = data
	regr = ensemble.RandomForestRegressor()
	regr.fit(X_train, y_train)
	y_train_pred = regr.predict(X_train)
	y_test_pred = regr.predict(X_test)

	print("MSE Train: %.3f, Test: %.3f" % (mean_squared_error(y_train, y_train_pred),
										   mean_squared_error(y_test, y_test_pred)))
	print("R2_Score Train: %.3f, Test: %.3f" % (r2_score(y_train, y_train_pred),
												r2_score(y_test, y_test_pred)))
	# print("Traing Score:%f" % regr.score(X_train, y_train))
	# print("Testing Score:%f" % regr.score(X_test, y_test))

if __name__=='__mian__':
	# 获取分类数据
	gpcr_name = 'P28335'
	data = load_csv('E:/sed_v0/inputdate/'+gpcr_name+'_ECFP12_1024_Top300.csv')
	target = load_csv('E:/sed_v0/data/'+gpcr_name+'/Response.csv')
	print('data:',data.shape)
	print('target:',target.shape)
	# 拆分成训练集和测试集，测试集大小为原始数据集大小的 1/4
	X_train, X_test, y_train, y_test = train_test_split(data, target.reshape(-1), test_size=0.25, random_state=0)
	# 调用 test_RandomForestRegressor
	test_RandomForestRegressor(X_train, X_test, y_train, y_test)

# final = np.array([[1,2],[3,4],[5,6]])
# sel = final[:, 0]
# t = 3
# print(sel)
# print(type(sel))
# print(sel[1])
