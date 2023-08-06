import numpy as np
import nlopt
from scipy.interpolate import UnivariateSpline,LSQUnivariateSpline
from sklearn.isotonic import IsotonicRegression

class Tracker:
    def __init__(self,lb=-10,ub=10,
                 budget=100,
                 adapt_options={},
                 n_knots=-1,
                 K=1,
                 lam = 1E-2,
                 gamma=1E-2
    ):
        """
        An APP Tracker object. 

        Parameters: 

        lb (float): the lower bound for the range of possible STLE locations.
        ub (float): the upper bound for the range of possible STLE locations.
        budget (int): the number of dictionary data points. 
        adapt_options: dictionary of options to be passed to the nlopt optimizer. Options include 'xtol_rel', 'maxeval', 'maxtime', and 'algo'.
        n_knots (int): number of knots for adaptive pressure profile. Defaults to -1 which chooses knots adaptively. 
        K (int): degree of adaptive spline fit. Defaults to K=1. 
        lam (float): L2 penalization parameter. 
        gamma (float): Adaptive pressure profile spline fit smoothness parameter. 

        Returns: 
        
        An object of the Tracker class. 
        """
        # fixed parameters of algorithm
        self.lb=lb
        self.ub=ub
        self.budget=budget
        self.n_knots = n_knots
        self.K=K
        self.lam = lam
        self.gamma=gamma
        self.i = 0 # internal counter for num processed timepoints
        # estimated properties
        self.est_adapt = None
        self.p_mean=None
        self.p_std=None
        self.x1_d = None
        self.p_d = None
        self.delta_d = None
        self.time_d = None
        #optimizer
        self.adapt = None
        algo = nlopt.GN_CRS2_LM
        self.optim_params_init = {'maxeval':100, 'xtol_rel':1E-10, 'algo':algo,'maxtime':-1}
        self.adapt_opt = self.init_opt(adapt_options,1)
        self.adapt_opt.set_lower_bounds(self.lb)
        self.adapt_opt.set_upper_bounds(self.ub)

    def make_adapt_design(self,x,update=False):
        return x.reshape(-1) 

    def init_opt(self,new_options,npar):
        ret_options = self.optim_params_init.copy()
        for k,v in new_options.items():
            ret_options[k] = v
        opt = nlopt.opt(ret_options['algo'],npar)
        opt.set_xtol_rel(ret_options['xtol_rel'])
        opt.set_maxeval(ret_options['maxeval'])
        opt.set_maxtime(ret_options['maxtime'])
        return opt

    def predict(self,x,p,base_method=None,std_x=True):
        """
        Predict STLE location and update adaptive fit. 
        
        Parameters: 

        x (float): the streamwise locations of the pressure transducers. 
        p (float): the measure pressures.
        base_method (function): a base method to produce a weak estimate. Defaults to pressure ratio method. Function takes two arguments x and p and produces a weak estimate (and a measurement of uncertainty). 
        std_x (boolean): Should fitting be done using standardized streamwise locations. 
        """
        self.i = self.i+1

        x_mean=0
        x_std=1
        if std_x:
            x_mean = np.mean(x)
            x_std = np.std(x)
        x = (x - x_mean)/x_std

        if base_method is None:
            base_method = lambda x,p:self.pressure_ratio(x,p,pa=1)

        # run base learner
        x1_base, delta = base_method(x,p)

        # update adaptive fit
        self.update_adapt(x,p,x1_base,delta)

        #initial guess for adaptive optimization (x0)
        x0 = self.est_adapt
        if x0 is None or ~np.isfinite(x0):
            x0 = x1_base
            
        # adaptive estimate
        if self.adapt is not None:
            self.est_adapt, adapt_cov =  self.fit_adapt(x,p,x0)
        else:
            self.est_adapt = x0
            adapt_cov = float('inf')
    
        return {'est':self.est_adapt*x_std+x_mean, 'est_cov':adapt_cov*x_std**2, 'base':x1_base*x_std+x_mean, 'delta':delta}

    def update_adapt(self,x,p,x1_base,delta):
        # basic sanity check of input estimates
        # don't update if base estimate doesn't exist
        if ~np.isfinite(x1_base):
            return

        ## DICTIONARY management
        # add to dictionary
        if self.x1_d is None: # need to create dictionary
            self.x1_d = x-x1_base
            self.p_d = p
            self.delta_d = np.repeat(delta,len(x)) #uncertainty of base
            self.time_d = np.repeat(self.i,len(x)) #time of point
            self.x1_base = np.repeat(x1_base,len(x)) #base estimate of point
        else:
            self.x1_d = np.append(self.x1_d,x-x1_base)
            self.p_d = np.append(self.p_d,p)
            self.delta_d = np.append(self.delta_d,np.repeat(delta,len(x)))
            self.time_d = np.append(self.time_d,np.repeat(self.i,len(x)))
            self.x1_base = np.append(self.x1_base,np.repeat(x1_base,len(x)))

        # if over budget prune
        if self.p_d.shape[0] > self.budget:
            N_rmv = len(self.x1_d)-self.budget
            dff = np.diff(self.x1_d)
            mdff = .5 * (dff[1:len(dff)] + dff[0:(len(dff)-1)])
            mdff = np.concatenate([[dff[0]],mdff,[dff[len(dff)-1]]])
            eps = self.delta_d/mdff # accuracy of base estimate / closeness to nearby points
            rmv = np.where(np.logical_or(eps >= -np.sort(-eps)[N_rmv-1],~np.isfinite(eps)))[0]
            if len(rmv)>N_rmv:
                rmv = np.random.choice(a=rmv,size=N_rmv,replace=False)
            # remove pts from dictionary and assoc. information
            self.x1_d = np.delete(self.x1_d,rmv,axis=0)
            self.p_d = np.delete(self.p_d,rmv,axis=0)
            self.delta_d = np.delete(self.delta_d,rmv,axis=0)
            self.time_d = np.delete(self.time_d,rmv,axis=0)
            self.x1_base = np.delete(self.x1_base,rmv,axis=0)

        # sort and remove non-unique values (more stable fitting)
        # remove non-unique from dict
        ux,iux=np.unique(self.x1_d,return_index=True)
        self.x1_d = ux
        self.p_d = self.p_d[iux]
        self.delta_d = self.delta_d[iux]
        self.time_d = self.time_d[iux]
        self.x1_base = self.x1_base[iux]
        # sort dict
        ordx = np.argsort(self.x1_d,axis=0).reshape(-1)
        self.x1_d = self.x1_d[ordx]
        self.p_d = self.p_d[ordx]
        self.delta_d = self.delta_d[ordx]
        self.time_d = self.time_d[ordx]
        self.x1_base = self.x1_base[ordx]

        ## ADAPTIVE PROFILE fitting
        # need more data than knots
        if len(self.x1_d)<=self.K:
            return
        # determine location of knots based on some heuristics
        if len(self.x1_d) > 5 and self.n_knots > 0:
            l3len  = int(np.ceil(len(self.x1_d)//3))
            if self.n_knots is not None:
                qs = np.linspace(.25,.75,np.min([l3len,self.n_knots]))
            else:
                qs = np.linspace(.25,.75,l3len)
            kseq=np.quantile(self.x1_d,qs)
            self.kseq = kseq[1:(len(kseq)-1)]
        else:
            self.kseq = []

        self.x_design = self.make_adapt_design(self.x1_d,update=True)

        self.p_mean = np.mean(self.p_d)
        self.p_std = np.std(self.p_d)
        self.p_z = (self.p_d-self.p_mean)/self.p_std

        # fit model and its derivative
        #just make sure everything is monotonic (for stability)
        mono_fit = IsotonicRegression().fit(self.x_design,self.p_z)
        mono_p = mono_fit.predict(self.x_design)
        if self.n_knots < 0:
            def err_mod(mod): #RSS for fit model
                return np.sum((mod(self.x1_d)-self.p_z)**2)/len(self.p_z)    
            smooth_spl = UnivariateSpline(self.x_design,mono_p,k=self.K,ext=0,s=len(self.p_z)*self.gamma)
            # some heuristics on what knots to keep 
            knts = smooth_spl.get_knots()
            keep_knts = ~np.logical_or(knts < np.quantile(self.x1_d,.1),knts > np.quantile(self.x1_d,.9))
            knts = knts[keep_knts]
            linear_mod = LSQUnivariateSpline(self.x_design,mono_p,k=self.K,ext=0,t=[])
            self.adapt  = LSQUnivariateSpline(self.x_design,mono_p,k=self.K,ext=0,t=knts)
            adapt_err = err_mod(self.adapt)
            lin_err = err_mod(linear_mod)
            #if its not twice as good as a simple linear model just use the latter
            if lin_err > 0 and adapt_err/lin_err > 0.5:
                self.adapt = linear_mod
        else: #n_knots > 0 
            self.adapt = LSQUnivariateSpline(self.x_design,mono_p,k=self.K,ext=0,t=self.kseq)
        self.adapt_deriv = self.adapt.derivative(1)

    def adapt_pred(self,x):
        x_basis = self.make_adapt_design(x)
        pred0 = self.adapt(x_basis)
        return pred0
    
    def fit_adapt(self,x,p,x0):
        # set up optimization
        obj = lambda par,grad: self.adapt_sqe(x,p,par)
        self.adapt_opt.set_min_objective(obj)
        x0 = np.max([self.lb,x0])
        x0 = np.min([self.ub,x0])
        # run optimization
        x_hat = self.adapt_opt.optimize([x0])[0]
        # calculate fitting sensitivity 
        drv1 = self.adapt_deriv(x-x_hat)
        d2 = np.mean(drv1**2)
        d2 += self.lam
        sig2 = self.adapt_sqe(x,p,[x_hat],pen=False)/(len(x)-1)
        cov = .5*sig2/d2
        return x_hat,cov

    def adapt_sqe(self,x,p,cent,pen=True):
        xc = x-cent
        ft = self.adapt_pred(xc).reshape(-1)
        p_z = (p - self.p_mean)/self.p_std
        val = np.mean((p_z-ft)**2)
        penalty = 0
        if pen:
            penalty = self.lam * np.abs(cent[0])**2
        return val+penalty

    # other helper functions
    def pressure_rise(self,x,p,pct=.5):
        try:
            pmin = np.min(p)
            delta = np.max(p)-pmin
            p_q = pmin+delta*pct
            i = np.min(np.where(np.diff((p>=p_q).astype(int)))[0])+1
            a=(p[i]-p[i-1])/(x[i]-x[i-1])
            b=p[i]-a*x[i]
            x_q = (p_q-b)/a
            rat = np.max(p)/np.min(p)
            if rat<2:
                x_q = float('Inf')
            return x_q, rat
        except Exception:
            return float('Inf'),float('Inf')

    def pressure_ratio(self,x,p,pa,ratio=2):
        p = p / pa
        p_q = ratio
        ii = np.where(np.diff((p>=p_q).astype(int)))[0]
        if len(ii)==0:
            return float('inf'), float('inf'), 
        i = np.min(ii)+1
        a=(p[i]-p[i-1])/(x[i]-x[i-1])
        b=p[i]-a*x[i]
        x_q = (p_q-b)/a
        delta = np.min(np.abs(x-x_q))
        return x_q, delta
