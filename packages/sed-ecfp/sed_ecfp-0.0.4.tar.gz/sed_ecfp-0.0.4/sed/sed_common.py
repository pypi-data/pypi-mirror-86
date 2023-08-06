import numpy as np
import math

def sll_opts(opts: dict) -> dict:
    '''
     Notice:
    If one or several (even all) keys are empty, sll_opts shall assign the
    default settings.

     If some fields of opts have been defined, sll_opts shall check the fields
     for possible errors.

     Table of Options.  * * indicates default value.

     -------------------------------------
      Starting point

     .x0                Starting point of x.
                        Initialized according to .init.

     .c0                 Starting point for the intercept c (for Logistic Loss)
                        Initialized according to .init.

     .init              .init specifies how to initialize x.
                        * 0 => .x0 is set by the function initFactor *
                          1 => .x0 and .c0 are defined
                          2 => .x0= zeros(n,1), .c0=0

     -------------------------------------
     Termination
     .maxIter          Maximum number of iterations.
                           *1e4*

     .tol              Tolerance parameter.
                           *1e-4*

     .tFlag            Flag for termination.
                           * 0 => abs( funVal(i)- funVal(i-1) ) <= .tol *
                             1 => abs( funVal(i)- funVal(i-1) )
                                  <= .tol max( funVal(i-1), 1)
                             2 => funVal(i) <= .tol
                             3 => norm( x_i - x_{i-1}, 2) <= .tol
                             4 => norm( x_i - x_{i-1}, 2) <=
                                  <= .tol max( norm( x_{i-1}, 2), 1 )
                             5 => Run the code for .maxIter iterations

     --------------------------------------
       Normalization
     .nFlag            Flag for implicit normalization of A.
                           * 0 => Do not normalize A *
                             1 => A=(A-repmat(mu, m, 1))*diag(nu)^{-1}
                             2 => A=diag(nu)^{-1}*(A-repmat(mu,m,1)

     .mu               Row vector to be substracted from each sample.
                               (.mu is used when .nFlag=1 or 2)
                            If .mu is not specified, then
                                * .mu=mean(A,1) *

     .nu               Weight (column) vector for normalization
                               (.mu is used when .nFlag=1 or 2)
                           If .nu is not specified, then
                           * .nFlag=1 => .nu=(sum(A.^2, 1)'/m.^{0.5} *
                           * .nFlag=2 => .nu=(sum(A.^2, 2)/n.^{0.5} *

     --------------------------------------------
      Regularization

     .rFlag            Flag for regularization
                               (.rFlag is used for the functions with "R")
                            * 0 => lambda1 is the regularization parameter *
                              1 => lambda1 = lambda1 * lambda1_{max}
                                   where lambda1_{max} is the maximum lambda1
                                   that yields the zero solution
     .rsL2              Regularization parameter value of the squared L2 norm
                               (.rsL2 is used only for l1 regularization)
                            *.rsL2=0*
                        If .rFlag=0, .rsL2 is used without scaling
                           .rFlag=1, .rsL2=.rsL2 * lambda1_{max}

     ----------------------------------------------
      Method & Line Search
     .lFlag

     -----------------------------------------------
      Grooup & Others
     .ind              Indices for k groups (a k+1 row vector)
                       For group lasso only
                       Indices for the i-th group are (ind(i)+1):ind(i+1)

     .q                Value of q in L1/Lq regularization
                          *.q=2*

     .sWeight          The sample (positive and negative) weight
                       For the Logistic Loss only
                       Positive sample: .sWeight(1)
                       Negative sample: sWeight(2)
                       *1/m for both positive and negative samples*

     .gWeight          The weight for different groups
                          *.gWeight=1*

     .fName            The name of the function

    '''

    # Starting point
    if 'init' in opts:    # 原代码中判断'init'是否是opts的成员
        if (opts['init'] != 0) and (opts['init'] != 1) and (opts['init'] != 2):
            opts['init'] = 0
        if ('x0' not in opts) and (opts['init'] == 1):  # 原代码用的是if 不确定是if还是elif
            opts['init'] = 0
    else:
        opts['init'] = 0

    # Termination
    if 'maxIter' in opts:
        if opts['maxIter'] < 1:
            opts['maxIter'] = 10000
    else:
        opts['maxIter'] = 10000

    if 'tol' not in opts:
        opts['tol'] = 1e-3

    if 'tFlag' in opts:
        if opts['tFlag'] < 0:
            opts['tFlag'] = 0
        elif opts['tFlag'] > 5:
            opts['tFlag'] = 5
        else:
            opts['tFlag'] = math.floor(opts['tFlag'])
    else:
        opts['tFlag'] = 0

    # Normalization
    if 'nFlag' in opts:
        if(opts['nFlag'] != 1)and(opts['nFlag'] != 2):
            opts['nFlag'] =0
    else:
        opts['nFlag'] = 0

     # Regularization
    if 'rFlag' in opts:
        if(opts['rFlag'] != 1):
            opts['rFlag'] = 0
    else:
        opts['rFlag'] = 0

    #  Method (Line Search)
    if 'lFlag' in opts:
        if opts['lFlag'] != 1:
            opts['lFlag'] = 0
    else:
        opts['lFlag'] = 0

    if 'mFlag' in opts:
        if opts['mFlag'] != 1:
            opts['mFlag'] = 0
    else:
        opts['mFlag'] = 0

    return opts


def init_factor(x_norm: float, Ax: np.ndarray, y: np.ndarray, z: np.ndarray, fun_name: str, rsL2: float,
                x_2norm: float):    # 将fun_name由字符串改成了字典
    '''

    :param x_norm:the norm of the starting point
    :param Ax:A*x, with x being the initialization point
    :param y: the response matrix
    :param z:the regularization parameter or the ball
    :param fun_name:the name of the function
    :param rsL2:
    :param x_2norm:
    :return: the computed optimal initialization point is ratio*x

    '''


    def leastc():
        ratio_max = z/x_norm
        ratio_optimal = (np.matmul(Ax.T,y))/(np.matmul(Ax.T,Ax)+rsL2*x_2norm)  # 返回None？ 原码：ratio_optimal = Ax'*y / (Ax'*Ax + rsL2 * x_2norm)
        if abs(ratio_optimal) <= ratio_max:
            ratio = ratio_optimal
        elif ratio_optimal < 0:
            ratio = -ratio_max
        else:
            ratio = ratio_max
        return ratio[0][0]
        # fprintf('\n ratio=%e,%e,%e',ratio,ratio_optimal,ratio_max) ???? ratio_max不是矩阵吗

    def leastr():
        ratio = (np.dot(Ax.T,y)-z*x_norm)/(np.dot(Ax.T,Ax)+rsL2*x_2norm)
        #print('ratio=', ratio[0][0])
        return ratio[0][0]

    def glleastr():
        ratio = (np.matmul(Ax.T,y)-z*x_norm)/np.matmul(Ax.T,Ax)
        # fprintf('\n ratio=%e', ratio)
        return ratio[0][0]

    def mclLeastr():
        ratio = (np.matmul((Ax.T).reshape(1,-1),(y.T).reshape(-1,1))-z*x_norm)/(np.linalg.norm(Ax)^2)
       # fprintf('\n ratio=%e', ratio)
        return ratio[0][0]

    def mtleastr():
        ratio = (np.matmul(Ax.T,y)-z*x_norm)/(np.matmul(Ax.T,Ax))
        # fprintf('\n ratio=%e',ratio)
        return ratio[0][0]

    def nnleastr():
        ratio = (np.matmul(Ax.T,y)-z*x_norm)/(np.matmul(Ax.T,Ax)+rsL2*x_2norm)
        ratio = max(0,ratio)
        return ratio[0][0]

    def nnleastc():
        ratio_max = z/x_norm
        ratio_optimal = (np.matmul(Ax.T,y))/(np.matmul(Ax.T,Ax)+rsL2*x_2norm)
        if ratio_optimal < 0:
            ratio=0
        elif ratio_optimal<=ratio_max:
            ratio = ratio_optimal
        else:
            ratio = ratio_max
        # fprintf('\n ratio=%e,%e,%e',ratio,ratio_optimal,ratio_max)
        return ratio

    def mcleastc():
        ratio_max = z/x_norm
        ratio_optimal = (np.matmul((Ax.T).reshape(1,-1),(y.T).reshape(-1,1)))/(np.linalg.norm(np.matmul(Ax.T,Ax))^2)
        if abs(ratio_optimal) <= ratio_max:
            ratio = ratio_optimal
        elif ratio_optimal < 0:
            ratio = -ratio_max
        else:
            ratio = ratio_max
        return ratio

    # def fprintf():
    #     print('\n The specified funName is not supprted')  # 原码fprintf('\n The specified funName is not supprted');

    fun_dict = {'LeastC': leastc, 'least_r': leastr,'glLeastR': glleastr,'mcLeastR': mclLeastr,
                'mtLeastR': mtleastr, 'nnLeastR': nnleastr,'nnLeastC': nnleastc,'mcLeastC': mcleastc}

    return fun_dict.get(fun_name)()



