"""
% ECFP_12_1024
% This is a demo for integrating EDPP screening rule with SLEP to
% solve the Lasso problem at a given sequence of parameter values:
%
% min  1/2 || X * beta - y||^2 + lambda * ||beta||_1
"""
import os
import csv
import numpy as np
from scipy.stats import zscore
from sklearn.model_selection import train_test_split
#from xgboost import XGBRegressor
from sed.dpc_screening import edpp_lasso
from sed.gen_ecfp import gen_ecfps
from sklearn.metrics import r2_score,mean_squared_error
# set your input
from sed.rf_test import load_csv, test_RandomForestRegressor


def select_feature(File_name,gpcr_name,t,resfile):
    """
    对ECFP指纹做特征筛选
    :param File_name: 待筛选的ECFP指纹的csv文件
    :param t: 筛选后特征向量的长度
    :return:
    """

    def csv_read(filename):
        '''
        :param filename:
        :return: np.ndarray
        '''
        res = []
        with open(filename, 'r') as fr:
            reader = csv.reader(fr)
            for line in reader:
                res.append(float(line[0]))
        return np.array(res).reshape(-1,1)

    def csv_write(filename,data):
        with open(filename,'w') as fw:
            writer = csv.writer(fw)
            for l in data:
                writer.writerow(l)
    # X = double(X)
    X = np.load(File_name + '.npy')
    X1 = zscore(X) #标准化
    np.nan_to_num(X1,nan=0,copy=False) #将ndarray中的nan替换成0,copy=False直接更改X1
    local_path = os.getcwd()
    y = csv_read(local_path+'/data/'+gpcr_name+'/Response.csv')
    # load(strcat('number', str(gpcr_length), '.mat'))


    # set up the solver from SLEP, can leave as default
    opts={}
    # termination criterion
    opts['tFlag']=5       # run .maxIter iterations
    opts['maxIter']=1000    # maximum number of iterations
                            # when the improvement is small,
                            # SLEP may stop without running opts.maxIter steps
    # normalization
    opts['nFlag']=0       # without normalization
    # regularization
    opts['rFlag']=1       # the input parameter 'lambda' is a ratio in (0, 1]
    opts['fName'] = 'LeastR'  # compute a sequence of lasso problems
    opts['mFlag']=0       # treating it as compositive function
    opts['lFlag']=0       # Nemirovski's line search

    # set the regularization paramter values
    # if the parameter values are the ratios of lambda/lambda_max; if use the
    # absolute value, please set opts.rFlag = 0

    ub = 0.5 # upper bound of the parameter values
    lb = 0.05 # lower bound of the parameter values
    npar = 100 # number of parameter values
    delta_lambda = (ub - lb)/(npar-1)
    lambda1 = np.arange(lb,ub,delta_lambda) # the parameter sequence
    #print(lambda1)
    # solve the Lasso problems along the sequence of parameter values


    Sol, ind_zf = edpp_lasso(X1, y, lambda1, opts)
    T=ind_zf[:,0].astype(bool)
    Xr = X1[:,~T]
    ind=np.sum(~ind_zf.astype(bool),axis=0)
    intx=np.sum(~ind_zf.astype(bool),axis=1).reshape(-1,1)
    fn = np.arange(1024).reshape(-1,1)
    final=np.concatenate((fn,intx),axis=1)
    I=np.lexsort((final[:,0],-final[:,1]))
    final=final[I,:]

    # select key features
    # t=0
    # sel = []
    # for i in range(300):
    #     sel.append(final[i,0])
    #     t=t+1
    sel = final[:,0]

    select = np.zeros((X.shape[0],t))
    for j in range(X.shape[0]):
        for k in range(t):
            select[j,k]=X[j,sel[k]]

    #resfile = os.getcwd()+'/inputdate/'+File_name+'_Top300'+'.csv'
    print("筛选出来的特征保存在：", resfile)
    # 保存挑选出来的特征
    csv_write(resfile,select)

def demo(gpcr_name,gpcr_length,gpcr_radius,t,resfile):
    ecfp_file = gen_ecfps(gpcr_name,gpcr_length,gpcr_radius)

    select_feature(ecfp_file,gpcr_name,t,resfile)

    data = load_csv(resfile)
    target = load_csv('data/' + gpcr_name + '/Response.csv')
    print('data:', data.shape)
    print('target:', target.shape)
    # 拆分成训练集和测试集，测试集大小为原始数据集大小的 1/4
    X_train, X_test, y_train, y_test = train_test_split(data, target.reshape(-1), test_size=0.25, random_state=0)
    # 调用 test_RandomForestRegressor
    test_RandomForestRegressor(X_train, X_test, y_train, y_test)
    # model = XGBRegressor(n_estimators=2000)
    # model.fit(X_train,y_train,eval_set=[(X_test,y_test)],verbose=True,early_stopping_rounds=20)
    # y_pred = model.predict(X_test)
    # print('rmse:',np.sqrt(mean_squared_error(y_pred,y_test)),'r2:',r2_score(y_pred,y_test))

if __name__=='__main__':
    gpcr_name = 'P08908'
    gpcr_length = 1024
    gpcr_radius = 6
    t = 300
    resfile = gpcr_name + '_ECFP12_1024_Top300.csv'
    demo(gpcr_name,gpcr_length,gpcr_radius,t,resfile)