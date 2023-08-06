import numpy as np
from scipy.sparse import issparse
from sed.sed_common import sll_opts,init_factor

def least_r(A: np.ndarray,y,z,opts):
    """
    函数内变量名同原MATLAB程序
    :param A:
    :param y:
    :param z:
    :param opts:
    :return:
    """

    m, n = A.shape
    if y.shape[0]!=m:
        raise Exception('check the length of y!')
    if z<0:
        raise Exception('z should be nonnegative!')

    opts = sll_opts(opts)

    # Detailed initialization
    """
    %% Normalization
    
    % Please refer to sll_opts for the definitions of mu, nu and nFlag
    %
    % If .nFlag =1, the input matrix A is normalized to
    %                     A= ( A- repmat(mu, m,1) ) * diag(nu)^{-1}
    %
    % If .nFlag =2, the input matrix A is normalized to
    %                     A= diag(nu)^{-1} * ( A- repmat(mu, m,1) )
    %
    % Such normalization is done implicitly
    %     This implicit normalization is suggested for the sparse matrix
    %                                    but not for the dense matrix
    """
    if opts['nFlag']!=0:
        if 'mu' in opts:
            mu = opts['mu']
            if mu.shape[1]!=n:
                raise ('check the input .mu')
        else:
            mu = np.mean(A,axis=1)
        
        if opts['nFlag']==1:
            if 'nu' in opts:
                nu = opts['nu']
                if nu.shape[0]!=n:
                    raise('check the input nu')
            else:
                nu = (np.sum(A**2,0)/m)**0.5
                nu = nu.T
        else: #nFlag=2
            if 'nu' in opts:
                nu = opts['nu']
                if nu.shape[0]!=m:
                    raise('check the input nu')
            else:
                nu = (np.sum(A**2,1)/n)**0.5
        ind_zero = np.abs(nu)<=1e-10
        nu[ind_zero] = 1

    if (not issparse(A)) and opts['nFlag']!=0:
        print('The data is not sparse or not stored in sparse format')
        print('The code still works')
        print('But we suggest you to normalize the data directly')
        print('for achieving better efficiency')

    """ Starting point initialization"""
    # compute ATy
    if opts['nFlag']==0:
        ATy = np.dot(A.T,y)
    elif opts['nFlag']==1:
        ATy = np.dot(A.T,y) - np.dot(np.sum(y),mu.T)
        ATy = ATy/nu
    else:
        invNu = y/nu
        ATy = np.dot(A.T,invNu)-np.dot(np.sum(invNu),mu.T)

    # process the regularization parameter
    # L2 normn regularization
    if 'rsL2' in opts:
        rsL2 = opts['rsL2']
        if rsL2<0:
            raise("opts['rsL2'] should be nonnegative")
    else:
        rsL2 = 0
    #L1 norm regularization
    if opts['rFlag']==0:
        lambda1 = z
    else: # z here is the scaling factor lying in [0,1]
        if z<0 or z>1:
            raise ("opts['rFlag']=1,and z should be in [0,1]")
        if 'lambda_max' in opts:
            lambda_max = opts['lambda_max']
        else:
            lambda_max = np.max(np.abs(ATy))
        lambda1 = np.dot(z,lambda_max)
        rsL2 = np.dot(rsL2,lambda_max)

    # initialize a starting point
    if opts['init']==2:
        x = np.zeros((n,1))
    else:
        if 'x0' in opts:
            x = opts['x0'].reshape(-1,1)
            if x.shape[0]!=n:
                raise ('Check the input x0')
        else:
            x = ATy

    #compute A x
    if opts['nFlag']==0:
        Ax = np.dot(A,x)
    elif opts['nFlag']==1:
        invNu = x/nu
        mu_invNu = np.dot(mu,invNu)
        Ax = np.dot(A,invNu) - mu_invNu.reshape(m,1)
    else:
        Ax = np.dot(A,x) - np.dot(mu,x).reshape(m,1)
        Ax = Ax/nu      #? ./

    if opts['init']==0:
        x_norm = np.sum(abs(x))
        x_2norm = np.dot(x.T,x)
        if x_norm>=1e-6:
            ratio = init_factor(x_norm,Ax,y,lambda1,'least_r',rsL2,x_2norm) #????
            x = ratio*x
            Ax = ratio*Ax

    """The main program"""
    """The Armiho Goldstein line search scheme + accelearted gradient descent"""
    if opts['mFlag']==0 and opts['lFlag']==0:
        bFlag = 0  # this flag tests whether the gradient step only changes a little
        L = 1+rsL2  # we assume that the maximum eigenvalue of A'A is over 1
        # assign xp with x, and Axp with Ax
        xp = x
        Axp = Ax
        xxp = np.zeros((n,1))
        #alphap and alpha are used for computing the weight in forming search point
        alphap = 0
        alpha = 1
        ValueL = []  # ??????????
        funVal = []
        for iterStep in range(opts['maxIter']):
            #step 1  compute search point s based on xp and x(with beta)
            beta = (alphap-1)/alpha
            s = x + beta*xxp

            As = Ax + beta*(Ax-Axp)

            if opts['nFlag']==0:
                ATAs = np.dot(A.T,As)
            elif opts['nFlag']==1:
                ATAs = np.dot(A.T,As) - (np.sum(As)*mu.T)
                ATAs = ATAs/nu
            else:
                invNu = As/nu
                ATAs = np.dot(A.T,invNu) - np.sum(invNu)*mu.T   ####

            #obtain the gradient g
            g = ATAs - ATy + np.dot(rsL2,s)

            xp = x
            Axp = Ax

            while(True):
                v = s - g/L
                #L1-norm regularized projection
                x = np.sign(v)*np.maximum((abs(v)-lambda1/L),np.zeros((v.shape)))

                v = x - s

                # compute A x
                if opts['nFlag']==0:
                    Ax = np.dot(A,x)
                elif opts['nFlag']==1:
                    invNu = x/nu
                    mu_invNu = np.dot(mu,invNu)
                    Ax = np.dot(A,invNu) - mu_invNu.reshape(m,1)
                else:
                    Ax = np.dot(A,x) - np.dot(mu,x).reshape(m,1)
                    Ax = Ax/nu


                Av = Ax - As
                r_sum = np.dot(v.T,v)
                l_sum = np.dot(Av.T,Av)
                #print(x.shape, s.shape, Ax.shape, As.shape, ATy.shape, opts['x0'].shape,r_sum[0][0],l_sum[0][0])
                if r_sum[0][0]<=1e-20:
                    bFlag = 1
                    break

                # the condition is ||Av||_2^2 <= (L-rsL2)*||v||_2^2
                if l_sum[0][0]<=np.dot(r_sum,(L-rsL2))[0][0]:
                    break
                else:
                    L = max(2*L,l_sum/r_sum + rsL2)


            ValueL.append(int(L))

            # step 3
            # update alpha and alphap, and check whether converge
            alphap = alpha
            alpha = (1+np.sqrt(4*alpha*alpha + 1))/2
            xxp = x-xp
            Axy = Ax-y
            # funVal[iterStep] = np.dot(Axy.T,Axy)/2 + rsL2/2*np.dot(x.T,x) + sum(abs(x))*lambda1
            funVal.append((np.dot(Axy.T,Axy)/2 + rsL2/2*np.dot(x.T,x) + sum(abs(x))*lambda1)[0][0])
            #print(funVal)
            if bFlag:
                print('the program terminates as the gradient step changes the solution very small')
                break

            if opts['tFlag'] == 0:
                if iterStep>=2:
                    if abs(funVal[iterStep] - funVal[iterStep-1])<= opts['tol']:
                        break
            elif opts['tFlag'] == 1:
                if iterStep>=2:
                    if abs(funVal[iterStep]-funVal[iterStep-1]) <= opts['tol']* funVal[iterStep-1]:
                        break
            elif opts['tFlag'] ==2:
                if funVal[iterStep] <= opts['tol']:
                    break
            elif opts['tFlag'] == 3:
                norm_xxp = np.sqrt(np.dot(xxp.T,xxp))
                if norm_xxp<=opts['tol']:
                    break
            elif opts['tFlag'] == 4:
                norm_xp = np.sqrt(xp.T,xp)
                norm_xxp = np.sqrt(xxp.T,xxp)
                if norm_xxp<=opts['tol']*np.max(norm_xp,1):
                    break
            elif opts['tFlag'] == 5:
                if iterStep>= opts['maxIter']:
                    break

    """Reformulated problem +Nemirovski's scheme
    % .mFlag=1, and .lFlag=0
    %  refomulate the problem as the constrained convex optimization
    %  problem, and then apply Armijo Goldstein line search scheme
    
    % Problem:
    %    min  1/2 || A x - y||^2 + 1/2 rsL2 * ||x||_2^2 + z * t' * 1
    %    s.t.   |x| <= t    
    """
    if opts['mFlag']==1 and opts['lFlag']==0:
        print(10)
        bFlag = 0
        L = 1+rsL2
        xp = x
        Axp = Ax
        xxp = np.zeros((n,1))
        t = abs(x)
        tp = t
        alphap = 0
        alpha = 1

        for iterStep in range(opts['maxIter']):
            #step 1 compute search point s based on xp and x(with beta)
            beta = (alphap-1)/alpha
            s = x + beta*xxp
            s_t = t + beta*(t-tp)
            # step 2 line search for L and compute the new approximate solution x
            # compute the gradient(g) at s
            As = Ax + beta*(Ax-Axp)
            if opts['nFlag']==0:
                ATAs = np.dot(A.T,As)
            elif opts['nFlag']==1:
                ATAs = np.dot(A.T,As) - np.dot(sum(As),mu.T)
                ATAs = ATAs/nu
            else:
                invNu = As/nu
                ATAs = np.dot(A.T,invNu) - np.dot(sum(invNu),mu.T)

            g = ATAs - ATy + np.dot(rsL2,s)

            xp = x
            Axp = Ax
            tp = t

            while(True):
                u = s-g/L
                v = s_t - lambda1/L

                x,t = ep1R(u,v,n)

                v = x-s
                v_t = t - s_t

                if opts['nFlag']==0:
                    Ax = np.dot(A,x)
                elif opts['nFlag']==1:
                    invNu = x/nu
                    mu_invNu = np.dot(mu,invNu)
                    Ax = np.dot(A,invNu) - mu_invNu.reshape(m,1)
                else:
                    Ax = np.dot(A,x) - np.dot(mu,x).reshape(m,1)
                    Ax = Ax/nu

                Av = Ax - As
                r_sum = np.dot(v.T,v) + np.dot(v_t.T,v_t)
                l_sum = np.dot(Av.T,Av) + np.dot(np.dot(v.T,v),rsL2)
                if r_sum[0][0]<=1e-20:
                    bFlag = 1
                    break

                if l_sum[0][0]<=r_sum[0][0]*L:
                    break
                else:
                    L = max(2*L,l_sum/r_sum)
            ValueL[iterStep] = L
            #step 3 update alpha and alphap, and check whether converge
            alphap = alpha
            alpha = (1+np.sqrt(4*alpha*alpha+1))/2
            xxp = x-xp
            Axy = Ax - y
            funVal[iterStep] = np.dot(Axy.T,Axy)/2 + rsL2/2 * np.dot(x.T,x) + sum(t)*lambda1
            if bFlag:
                break

            if opts['tFlag']==0:
                if iterStep>=2:
                    if abs(funVal[iterStep] - funVal[iterStep-1]) <= opts['tol']:
                        break
            elif opts['tFlag']==1:
                if iterStep>=2:
                    if abs(funVal[iterStep]-funVal[iterStep-1]) <= opts['tol']*funVal[iterStep-1]:
                        break
            elif opts['tFlag']==2:
                if funVal[iterStep] <= opts['tol']:
                    break
            elif opts['tFlag'] == 3:
                norm_xxp = np.sqrt(np.dot(xxp.T,xxp) + np.linalg.norm(t-tp)**2)
                if norm_xxp <= opts['tol']:
                    break
            elif opts['tFlag'] == 4:
                norm_xp = np.sqrt(np.dot(xp.T,xp) + np.dot(tp.T,tp))
                norm_xxp = np.sqrt(np.dot(xxp.T,xxp) + np.linalg.norm(t-tp)**2)
                if norm_xxp <= opts['tol']*max(norm_xp,1):
                    break
            elif opts['tFlag'] == 5:
                if iterStep >= opts['maxIter']:
                    break

    """
    adaptive line search
    % .mFlag=1, and .lFlag=1
    %  refomulate the problem as the constrained convex optimization
    %  problem, and then apply adaptive line search scheme
    
    % Problem:
    %    min  1/2 || A x - y||^2 + 1/2 rsL2 * ||x||_2^2 + z * t' * 1
    %    s.t.   |x| <= t
    """
    if opts['mFlag']==1 and opts['lFlag']==1:  # 519行
        print(11)
        bFlag = 0
        L = 1 + rsL2
        gamma = 1
        xp = x
        Axp = Ax
        xxp = np.zeros((n,1))
        t = abs(x)
        tp = t
        # t is the upper bound of absolute value of x
        # compute AT Ax
        if opts['nFlag']==0:
            ATAx = np.dot(A.T,Ax)
        elif opts['nFlag']==1:
            ATAx = np.dot(A.T,Ax) - sum(Ax)*mu.T
            ATAx = ATAx/nu
        else:
            invNu = Ax/nu
            ATAx = np.dot(A.T,invNu) - sum(invNu)*mu.T

        for iterStep in range(opts['maxIter']):
            ATAxp = ATAx
            if (iterStep!=0):
                if opts['nFlag']==0:
                    ATAx = np.dot(A.T,Ax)
                elif opts['nFlag']==1:
                    ATAx = np.dot(A.T,Ax) - sum(Ax)*mu.T
                    ATAx = ATAx/nu
                else:
                    invNu = Ax/nu
                    ATAx = np.dot(A.T,invNu) - sum(invNu)*mu.T
            # line seardch for L begins
            while(True):
                if iterStep!=0:
                    alpha = (-gamma + np.sqrt(gamma*gamma + 4*L*gamma))/(2*L)
                    beta = (gamma - gamma*alphap) / (alphap*gamma + alphap*L*alpha)
                    # beta is the coefficient for generateing search point s
                    s = x + beta*xxp
                    s_t = t + beta*(t-tp)
                    As = Ax + beta*(Ax-Axp)
                    ATAs = ATAx + beta*(ATAx-ATAxp)
                    #compute the search point s, A*s, and A'*A*s
                else:
                    alpha = (-1 + np.sqrt(5))/2
                    beta = 0
                    s = x
                    s_t = t
                    As = Ax
                    ATAs = ATAx

                g = ATAs - ATy + rsL2*s  # compute the gradient g

                # let s walk in a step in the antigradient of s
                u = s - g/L
                v = s_t - lambda1/L

                # projection
                xnew, tnew = ep1R(u,v,n)
                
                v = xnew - s
                v_t = tnew - s_t
                #compute A xnew
                if opts['nFlag']==0:
                    Axnew = np.dot(A,xnew)
                elif opts['nFlag']==1:
                    invNu = xnew/nu
                    mu_invNu = mu * invNu
                    Axnew = np.dot(A,invNu) - mu_invNu.reshape(m,1)
                else:
                    Axnew = np.dot(A,xnew) - (mu*xnew).reshape(m,1)
                    Axnew = Axnew / nu

                Av = Axnew - As
                r_sum = np.dot(v.T,v) + np.dot(v_t.T,v_t)
                l_sum = np.dot(Av.T,Av) + np.dot(v.T,v)*rsL2

                if r_sum[0][0] <=1e-20:
                    bFlag = 1
                    break
                # the condition is | | Av | | _2 ^ 2 + rsL2 * | | v | | _2 ^ 2 <= L * (| | v | | _2 ^ 2 + | | v_t | | _2 ^ 2)
                if (l_sum[0][0] <= r_sum[0][0] * L):
                    break
                else:
                    L = max(2 * L, l_sum / r_sum)
            # Line Search for L ends
            gamma = L*alpha*alpha
            alphap = alpha
            #update gamma, and alphap
            ValueL[iterStep] = L
            tao = L * r_sum / l_sum
            if tao>=5:
                L = L*0.8
            # decrease the value of L
            xp = x
            x = xnew
            xxp = x - xp
            Axp = Ax
            Ax = Axnew
            #update x and Ax with xnew and Axnew
            tp = t
            t = tnew
            #update tp and t
            Axy = Ax - y
            funVal[iterStep] = np.dot(Axy.T,Axy)/2 + rsL2/2*np.dot(x.T,x) + lambda1*sum(t)
            #compute function value

            if bFlag:
                #print("The program terminates as the gradient step changes the solution very small")
                break

            if opts['tFlag']==0:
                if iterStep >= 2:
                    if abs(funVal[iterStep] - funVal[iterStep-1]) <= opts['tol']:
                        break
            elif opts['tFlag']==1:
                if iterStep >= 2:
                    if abs(funVal[iterStep] - funVal[iterStep-1]) <= opts['tol'] * funVal[iterStep-1]:
                        break
            elif opts['tFlag']==2:
                if funVal[iterStep] <= opts['tol']:
                    break
            elif opts['tFlag']==3:
                norm_xxp = np.sqrt(np.dot(xxp.T,xxp) + np.linalg.norm(t-tp)**2)
                if norm_xxp <= opts['tol']:
                    break
            elif opts['tFlag']==4:
                norm_xp = np.sqrt(np.dot(xp.T,xp) + np.dot(tp.T,tp))
                norm_xxp = np.sqrt(np.dot(xxp.T,xxp) + np.linalg.norm(t-tp)**2)
                if norm_xxp <= opts['tol'] * max(norm_xp,1):
                    break
            elif opts['tFlag'] == 5:
                if iterStep>=opts['maxIter']:
                    break

    if opts['mFlag']==0 and opts['lFlag']==1:
        raise ("The function does not support opts.mFlag=0 & opts.lFlag=1")

    return x, funVal, ValueL

"""def sll_opts(opts: dict) -> dict:
    return opts

def init_factor(x_norm: float, Ax: np.ndarray, y: np.ndarray, z: np.ndarray, fun_name: str, rsL2: float, x_2norm: float):

    pass"""

