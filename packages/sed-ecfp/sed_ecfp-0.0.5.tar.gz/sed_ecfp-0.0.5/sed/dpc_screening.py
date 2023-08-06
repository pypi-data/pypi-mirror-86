import numpy as np
from sed.slep import least_r

def dpc_nnLasso():
    pass
def edpp_lasso(x: np.ndarray, y: np.ndarray, lambda1: list, opts: dict):
    """
    源代码位置： E:\SED\DPC\DPC\DPC_screening\EDPP_Lasso.m
    将其修改为python放入该函数

    :param x: the data matrix, each column corresponds to a feature each row corresponds to a data instance
    :param y: the response vector
    :param lambda1: the parameters sequence
    :param opts: settings for the solver
    :return:
    %         Sol:
    %              the solution; the ith column corresponds to the solution
    %              with the ith parameter in lambda1
    %
    %         ind_zf:
    %              the index of the discarded features; the ith column
    %              refers to the solution of the ith value in lambda1
    """
    p = x.shape[1]
    npar = len(lambda1)
    opts['init'] = 0
    sol = np.zeros((p,npar))
    ind_zf = np.zeros((p,npar))

    x_norm = np.sqrt(np.sum(x**2,0))
    x_norm.shape = (1,-1)
    xty = abs(np.dot(x.T,y))  # 矩阵对应位置相乘

    indmx = np.argmax(xty)
    lambda_max = xty[indmx]

    if opts['rFlag']==1:
        opts['rFlag'] = 0
        lambda1 = lambda1 * lambda_max

    lambdav = -np.sort(-lambda1)  #降序排序
    lambda_ind = np.argsort(-lambda1)
    rlambdav = 1/lambdav

# solve the Lasso problems sequentially with EDPP
    lambdap = lambda_max
    for i in range(npar):
        lambdac = lambdav[i]
        if lambdac>=lambda_max:
            sol[:,lambda_ind[i]] = 0
            ind_zf[:,lambda_ind[i]] = 1
        else:
            if lambdap==lambda_max:
                theta = y/lambdap
                v = x[:,indmx]
                v1 = np.sign(np.dot(v.T,theta))*v
            else:
                theta = (y - np.dot(x,sol[:,lambda_ind[i-1]].reshape(-1,1)))*rlambdap
                v1 = y*rlambdap - theta

            rlambdac = rlambdav[i]

            v1.shape=(-1,1)
            # temp = np.linalg.norm(v1)
            v1 = v1/np.linalg.norm(v1)
            v2 = y*rlambdac - theta
            print(i)
            pv2 = v2 - v1*np.dot(v1.T,v2)
            o = theta + 0.5*pv2
            phi = 0.5*np.linalg.norm(pv2)

            # screening by EDPP, remove the ith feature if T(i)=1
            T = (1 - phi*x_norm.T) > (abs(np.dot(x.T,o))+1e-8)
            T1 = np.array(T).reshape(-1)
            #T2 = np.array(~T).astype(int).reshape(-1)
            ind_zf[:,lambda_ind[i]] = T1
            xr = x[:,~T1]

            if lambdap == lambda_max:
                opts['x0'] = np.zeros((xr.shape[1],1))
            else:
                opts['x0'] = sol[~T1,lambda_ind[i-1]]

            x1,_,_ = least_r(xr,y,lambdac,opts)

            sol[~T1,lambda_ind[i]] = x1.reshape(-1)
            lambdap = lambdac
            rlambdap = rlambdac

    return sol,ind_zf

if __name__=="__main__":
    m = 250
    n = 10000
    x = np.random.normal(0.0,1.0,(m,n))
    y = np.random.normal(0.0,1.0,(m,1))

    opts = {}
    # termination criterion
    opts['tFlag'] = 5  # run .maxIter iterations
    opts['maxIter'] = 1000  # maximum number of iterations
    # when the improvement is small,
    # SLEP may stop without running opts.maxIter steps
    # normalization
    opts['nFlag'] = 0  # without normalization
    # regularization
    opts['rFlag'] = 1  # the input parameter 'lambda' is a ratio in (0, 1]
    opts['fName'] = 'LeastR'  # compute a sequence of lasso problems
    opts['mFlag'] = 0  # treating it as compositive function
    opts['lFlag'] = 0  # Nemirovski's line search

    ub = 1  # upper bound of the parameter values
    lb = 0.05  # lower bound of the parameter values
    npar = 100  # number of parameter values
    #delta_lambda = (ub - lb) / (npar - 1)
    lambda1 = np.linspace(lb, ub, num=npar, endpoint=True)  # the parameter sequence
    #lambda1 = lambda1.reshape(1,-1) #reshape完要赋值
    sol,ind_zf = edpp_lasso(x,y,lambda1,opts)