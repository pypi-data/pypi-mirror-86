import pickle
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score
from sklearn.model_selection import train_test_split

class SegmentData:

    def __init__(self, df) -> None:
        """Contructor

        Args:
            df (DataFrame): Pandas Dataframe
        """

        self.dataframe = df.copy()

    @property
    def len(self):
        return self.dataframe.len()

    @property
    def shape(self):
        return self.dataframe.shape

    def random_split_05(df, train_split, semilla):
        """ create 2 dataframes with random split for the percentage desired,  without replacement 
        to be used in optimize_sampling_train_and_test """
        a = df.sample(frac=train_split, replace=False, random_state = semilla)
        b = df.drop(a.index)  
        return a, b

    @staticmethod
    def delta_pc(a,b): 
    
        """ delta percentage calculator """
        
        if a!=None and b!=None and b!=0 : 
            return float(a - b)/float(b)
        else:
            return None # beware of division by 0

    def calculate_uplift_test_canal(self, df):
        """
        Cálculo del uplift dado un dataset para datos de test de canal:
        Utiliza la columna de CANAL_FINAL y sn_conv_digital

        """

        df_sms = df[df['CANAL_FINAL'] ==  "SMS"]
        df_email = df[df['CANAL_FINAL'] ==  "EMAILING"]

        a = len(df_sms[df_sms['sn_conv_digital'] == 1]) / len(df_sms)
        b = len(df_email[df_email['sn_conv_digital'] == 1]) / len(df_email)
        
        # compute delta uplift
        uplift = SegmentData.delta_pc(a,b)
        return uplift
        
    def optimize_sampling_train_and_test(self, df, number_of_trials, train_split, semilla):
        """ Balance and optimize split after n number_of_trials and keep homogenous train and test sets
        under double optimization index : 
        1/ abs(1 - abs(uplift_pc_train/uplift_pc_test)) -- minimize difference in uplift percentage
        2/ abs(1 - abs(uplift_eg_train/uplift_eg_test)) -- minimize difference in uplift in generated production
         """   
        # Define trials objects dictionnaries with keys as the trial index
        sets = {} # to save all intermediaire split sets
        deltas_u_pc = {} # Optimization obj : First step values to minimize
        deltas_u_eg = {} # Optimization obj : Second step values to minimize
        df_train = pd.DataFrame()
        df_test = pd.DataFrame()

        for i in range(number_of_trials) : # number of trials 
            df_train, df_test = SegmentData.random_split_05(df, train_split, semilla)
            sets[i] = df_train, df_test
            # - calculate respective uplifts in percentage and generated production & compute ratio differences to minimize

            deltas_u_pc[i] = abs(1 - abs(self.calculate_uplift_test_canal(df_train) / self.calculate_uplift_test_canal(df_test)))
            #deltas_u_eg[i]  = abs(1 - abs(calculate_uplift_EG(df_train, criterion, offer, eg)/calculate_uplift_EG(df_test, criterion, offer, eg))) 
    
        # 1st STEP -- select 2% of best trials on minimal delta_ratio_uplift_pc (percentage)  
        delta_min_upc = sorted([deltas_u_pc[i] for i in range(number_of_trials)])[:int(0.02*number_of_trials)]
        delta_min_upc_index = [list(deltas_u_pc.values()).index(i) for i in delta_min_upc]
        
        # 2nd STEP -- select the best delta_ratio_uplift_eg (generated production) of the above selection  
        #delta_min_ueg = min([deltas_u_eg[i] for i in delta_min_upc_index])
        #delta_min_Index = list(deltas_u_eg.values()).index(delta_min_ueg)
        # RESULTS : datasets to keep
        #df_train, df_test = sets[delta_min_Index]

        # Summary 
        # ---------------------------------------------------------------------------------
        S = [df, df_train, df_test]
        summary = pd.DataFrame({'00_rows': ['Full_dataset', 'Train_dataset', 'Test_dataset'], 
                                '01_number_of_rows': [len(i) for i in S], 
                                '02_uplifts_pc': [self.calculate_uplift_test_canal(i) for i in S]
                                })
        
        #print('Best balanced sample split at trial : ' + str(delta_min_Index) + ' / ' + str(number_of_trials))
        print('-----------------------------------------------------------------')
        print(summary)
        return df_train, df_test



##################Funciones para obtener grupos que maximicen el uplift######################

    def _regressor_split_summary(self, df_train, df_test, explanatory_var, cutoff):
        # - SUMMARY - Training
        # ---------------------------------------------------------------------------------
        """ Base : df, GroupA : df[df[explanatory_var] < cutoff], GroupB : df[df[explanatory_var] >= cutoff]
            T : Test df """
        S = [df_train, df_train[df_train[explanatory_var] < cutoff], df_train[df_train[explanatory_var] >= cutoff]]
        summary = pd.DataFrame({'00_groups':['base', 'groupA_var<' + str(round(cutoff,2)), 'groupB_var>=' + str(round(cutoff,2))], 
                                '01_groups_vol_ratio': [float(len(i))/float(len(df_train)) for i in S], 
                                '02_uplifts_pc': [self.calculate_uplift_test_canal(i) for i in S]})
        
        # - SUMMARY - Cross-validation on test set
        # ---------------------------------------------------------------------------------   
        S_T = [df_test, df_test[df_test[explanatory_var] < cutoff], df_test[df_test[explanatory_var] >= cutoff]]
        summary_T = pd.DataFrame({'00_groups':['T_base', 'T_groupA_var<' + str(round(cutoff,2)), 'T_groupB_var>=' + str(round(cutoff,2))], 
                                '01_groups_vol_ratio': [float(len(i))/float(len(df_test)) for i in S_T], 
                                '02_uplifts_pc': [self.calculate_uplift_test_canal(i) for i in S_T]}) 
        o = summary.append(summary_T) 
        return o 

    def Manual_regressor(self, df_train, df_test, explanatory_var, cutoff) :
        """ Tests the split of two groups on manual cutoff value - uplift summary"""
        o = self._regressor_split_summary(df_train, df_test, explanatory_var, cutoff)
        return  o

    def SelfOptimize_regressor(self, df_train, df_test, explanatory_var, q = 0.3):
        """ Finds the optimal cutoff value and tests the two groups - uplift summary"""
        # ---------------------------------------------------------------------------------
        # Optimize on train test
        # ---------------------------------------------------------------------------------
        df = df_train
        
        """ Objective function"""
        def compute_uplift_group_difference_pc(cutoff):
            """ The objective function to be minimized :
            difference in uplift in percentage between two groups split """
            uplift_groupA = self.calculate_uplift_test_canal(df[df[explanatory_var] < cutoff])
            uplift_groupB = self.calculate_uplift_test_canal(df[df[explanatory_var] >= cutoff])
            ABS_delta_AB = abs(uplift_groupA - uplift_groupB)
            return -ABS_delta_AB # negative value to achieve minimization
        
        """ Constraints & bounds : select quantiles to bound the variable in order to avoid marginal niche splits"""
        b = (df[explanatory_var].quantile(q), df[explanatory_var].quantile(1-q))
        
        """ Minimization of scalar function of one variable.
        Method Bounded can perform bounded minimization. 
        It uses the Brent method to find a local minimum in the interval x1 < xopt < x2."""    
        from scipy.optimize import minimize_scalar
        res = minimize_scalar(compute_uplift_group_difference_pc, 
                            bounds= b, 
                            method='bounded',
                            options={'disp': True, 'maxiter': 1000,  'xatol': 1e-05})
        # Key results
        cutoff = res['x']
        
        o = self._regressor_split_summary(df_train, df_test, explanatory_var, cutoff)
        return o

    def SelfOptimize_regressor_under_stability_constraints(self, df_train, df_test, explanatory_var, q, s):
        def compute_uplift_group_difference_pc():
            """ The objective function to be maximize : difference in uplift in percentage between two groups split """
            ABS_delta_AB = abs(self.uplift_groupA - self.uplift_groupB)
            return ABS_delta_AB 
        def compute_uplift_group_difference_pc_T():
            """ The objective function to be maximize : difference in uplift in percentage between two groups split """
            ABS_delta_AB = abs(self.uplift_groupA_T - self.uplift_groupB_T)
            return ABS_delta_AB 

        def stability_uplift_pc():
            """ The constraint function makes sur a minimal stability exists between the train and test group :
                results of uplift in percentage must have positive product """ 
            delta_product = (self.uplift_groupA-self.uplift_groupB)*(self.uplift_groupA_T-self.uplift_groupB_T)
            return delta_product
        def stability_uplift_eg():
            """ The constraint function makes sur a minimal stability exists between the train and test group :
                results of uplift in volume have positive product """
            delta_product_eg = (self.uplift_eg_groupA-self.uplift_eg_groupB)*(self.uplift_eg_groupA_T-self.uplift_eg_groupB_T)
            return delta_product_eg
        def stability_uplift_cross_pc_eg():
            """ The constraint function makes sur a minimal stability exists between uplift in percentage and in volume :
                results have positive product """ 
            delta_product_cross_pc_eg = (self.uplift_groupA-self.uplift_groupB)*(self.uplift_eg_groupA-self.uplift_eg_groupB)
            return delta_product_cross_pc_eg
        """ Custom iterator """
        x_iterations             = df_train[explanatory_var].sort_values().unique().tolist() 
        """ Bounds on mini segment split """
        bounds                   = (df_train[explanatory_var].quantile(q), df_train[explanatory_var].quantile(1-q)) 
        x_iterations_bounded     = [x for x in x_iterations if x>=bounds[0] and x<=bounds[1]]

        """ Compute uplift KPIs """
        n_steps                  = range(1, len(x_iterations_bounded) +1)
        print("Number of iterations : " + str(len(n_steps)))
        """ Iterator outputs """
        n_steps_executed         = []
        n_cutoff_executed        = []
        n_uplift_diff_executed   = []
        n_uplift_diff_executed_T = []
        n_stability_product      = []

        for n in n_steps :
            cutoff =  x_iterations_bounded[n]  

            groupA, groupA_T = (df[df[explanatory_var] < cutoff] for df in (df_train, df_test))
            groupB, groupB_T = (df[df[explanatory_var] >= cutoff] for df in (df_train, df_test))

            uplift_groupA, uplift_groupA_T, uplift_groupB, uplift_groupB_T             = (self.calculate_uplift_test_canal(df) for df in (groupA, groupA_T, groupB, groupB_T))
        #  uplift_eg_groupA, uplift_eg_groupA_T, uplift_eg_groupB, uplift_eg_groupB_T = (calculate_uplift_EG(df, criterion, offer, eg) for df #in (groupA, groupA_T, groupB, groupB_T))

            try : 
                d   = compute_uplift_group_difference_pc()
                d_T = compute_uplift_group_difference_pc_T()
                if stability_uplift_pc() > 0 and stability_uplift_eg() > 0 and stability_uplift_cross_pc_eg() > 0 : # Minimal stability requirements
                    # Stability barrier : max distance accepted between samples of building and validation ex. default : 200% 
                    if abs(self.delta_pc(d, d_T)) < s :      
                        n_steps_executed.append(n)
                        n_cutoff_executed.append(cutoff)
                        n_uplift_diff_executed.append(d)
                        n_uplift_diff_executed_T.append(d_T)
                        # Custom stability kpi to minimize : product of inverse uplift diff and delta in test and train samples
                        n_stability_product.append(1/(10*d) * abs(self.delta_pc(d, d_T)))
            except :
                pass # in order to deal with possible NoneType in KPIs results

        if len(n_steps_executed) > 0:
            print("Solutions under constraints found : " + str(len(n_steps_executed)))

            booster_index  = [n_stability_product.index(i) for i in sorted(n_stability_product)]
            best_cutoffs   = [n_cutoff_executed[i] for i in booster_index ]
            print("Best cutoffs orderde by performance and stability : " + str(best_cutoffs))
            print("\n")
            print("Summary for cutoff : " + str(best_cutoffs[0]))
            o = self.regressor_split_summary(df_train, df_test, explanatory_var, best_cutoffs[0])
            print(o) 
            
            return best_cutoffs # return full list of cutoffs to iterate
        else: 
            print("No conversion found under stability constraints")
######
######################### =======================================================================

    def discretization_on_bounds_list(df, explanatory_var, bounds) :
        """ returns a new/modified dataframe and creates a new column with a discretized variable according to the given bounds list 
        bounds definition : for n bounds returns n modalities, with left closed and right open interval
        ex. [a, b] : group'a<=x<b', group'x>=b" """
        group_names = [str(bounds[i])+"-"+ str(bounds[i+1]) for i in range(len(bounds)-1)] + [str(bounds[-1])+"+"]
        
        def classify_in_bounds(x, group_names):
            for i in range(len(bounds)-1):
                if x < bounds[i+1]:
                    return group_names[i]
            return group_names[-1]
        
        # map function & add new column in the dataframe
        df[explanatory_var + "_DISCR"] = df[explanatory_var].map(lambda x : classify_in_bounds(x, group_names))
        group_repartition = [round(float(len(df[df[explanatory_var + "_DISCR"] == i]))/float(len(df)),2) for i in group_names]
        
        print(" New column added : " + str(explanatory_var) + "_DISCR")
        print(" With new modalities : " + str(group_names))
        print(" With modalities repartition : " + str(group_repartition))
        return df 


    def _classifier_split_summary(self,df_train, df_test, explanatory_var, split):
        # - SUMMARY - Training
        # ---------------------------------------------------------------------------------
        """ Base : df, GroupA : df[df[explanatory_var].map(lambda x : x in split[0])], GroupB : df[df[explanatory_var].map(lambda x : x in split[1])]
            T : Test df """
        
        S = [df_train, df_train[df_train[explanatory_var].map(lambda x : x in split[0])], df_train[df_train[explanatory_var].map(lambda x : x in split[1])]]
        
        summary = pd.DataFrame({'00_groups':['base', 'groupA_varIN' + str(split[0]), 'groupB_varIN' + str(split[1])], 
                                '01_groups_vol_ratio': [float(len(i))/float(len(df_train)) for i in S], 
                                '02_uplifts_pc': [self.calculate_uplift_test_canal(i) for i in S]
                                #'03_uplifts_eg': [calculate_uplift_EG(i, criterion, offer, eg) for i in S],
                                #'04_fin_rate' : [self,calculate_finance_rate(i)for i in S]
                                })
        
        
        # - SUMMARY - Cross-validation on test set
        # ---------------------------------------------------------------------------------   
        S_T = [df_test, df_test[df_test[explanatory_var].map(lambda x : x in split[0])], df_test[df_test[explanatory_var].map(lambda x : x in split[1])]]
        summary_T = pd.DataFrame({'00_groups':['T_base', 'T_groupA_varIN' + str(split[0]), 'T_groupB_varIN' + str(split[1])], 
                                '01_groups_vol_ratio': [float(len(i))/float(len(df_train)) for i in S_T], 
                                '02_uplifts_pc': [self.calculate_uplift_test_canal(i) for i in S_T]
                                #'03_uplifts_eg': [calculate_uplift_EG(i, criterion, offer, eg) for i in S_T],
                                #'04_fin_rate' : [self,calculate_finance_rate(i)for i in S_T]
                                 })        
        o = summary.append(summary_T) 
        return o    

    def Manual_classifier(self, df_train, df_test, criterion, offer, eg, explanatory_var, split) :
        """ Tests the split of two groups on manual modalities split - uplift summary"""
        o = self._classifier_split_summary(df_train, df_test, criterion, offer, eg, explanatory_var, split)
        return  o
    

    def SelfOptimize_classifier_simple(self, df, criterion, offer, explanatory_var, mini_segment = 0.35):
        """ Returns list of best splits ordered on uplift difference with linear trials"""
        
        modalities_list = df[explanatory_var].unique().tolist()
        modalities_uplift = []
        for i in modalities_list :
            uplift = self.calculate_uplift_test_canal(df[df[explanatory_var].map(lambda x : x == i)], criterion, offer)
            if uplift :
                modalities_uplift.append(uplift)

        modalities_list_sorted = [modalities_list[i] for i in [modalities_uplift.index(x) for x in sorted(modalities_uplift)]]

        modalities_split = [] # new splits created (consecutive)
        deltas_u_pc = [] # ordered on uplift
        mini_seg = [] # with mini segment constraint
        print('Seed list elements : ' + str(modalities_list))        
        
        for l in range(1, len(modalities_list_sorted)):
            modalities_groupA = [i for i in modalities_list_sorted if modalities_list_sorted.index(i)<l]
            modalities_groupB = [i for i in modalities_list_sorted if modalities_list_sorted.index(i)>=l]
            split = [modalities_groupA, modalities_groupB]
            uplift_groupA = self.calculate_uplift_test_canal(df[df[explanatory_var].map(lambda x : x in modalities_groupA)], criterion, offer)
            uplift_groupB = self.calculate_uplift_test_canal(df[df[explanatory_var].map(lambda x : x in modalities_groupB)], criterion, offer)
            if uplift_groupA and uplift_groupB :
                ABS_delta_AB = abs(uplift_groupA - uplift_groupB)
                deltas_u_pc.append(ABS_delta_AB)
                modalities_split.append(split)
                r = float(len(df[df[explanatory_var].map(lambda x : x in modalities_groupA)]))/float(len(df))
                mini_seg.append(min(r, 1-r))
        print('Number of modality splits combinations : ' + str(len(modalities_split)))
        
        ind = [deltas_u_pc.index(i) for i in sorted(deltas_u_pc, reverse = True)]
        res = pd.DataFrame({'ind' : ind, 
                            'best_splits' : [modalities_split[i] for i in ind],
                            'delta_uplifts_pc' : [deltas_u_pc[i] for i in ind] , 
                            'mini_seg' : [mini_seg[i] for i in ind]})
        res_constr = res[res.mini_seg > mini_segment]
        print('Number of significant trial splits for mini segment ' +str(mini_segment) + ' : ' + str(len(res_constr)) +'\n')
        print(res_constr)
        return res_constr.best_splits.tolist()











    def SelfOptimize_classifier_under_stability_constraints(self, df_train, df_test, explanatory_var, mini_segment, s, m):
        """Finds the optimal cluster split and tests the two groups Under stability constraints - uplift summary """

        def compute_uplift_group_difference_pc():
            """ The objective function to be maximize : difference in uplift in percentage between two groups split """
            ABS_delta_AB = abs(uplift_groupA - uplift_groupB)
            return ABS_delta_AB 

        def compute_uplift_group_difference_pc_T():
            """ The objective function to be maximize : difference in uplift in percentage between two groups split """
            ABS_delta_AB = abs(uplift_groupA_T - uplift_groupB_T)
            return ABS_delta_AB 

        def stability_uplift_pc():
            """ The constraint function makes sur a minimal stability exists between the train and test group :
                results of uplift in percentage must have positive product """ 
            delta_product = (uplift_groupA-uplift_groupB)*(uplift_groupA_T-uplift_groupB_T)
            return delta_product

        def create_trial_splits_on_unique_modality_combinations(df, explanatory_var, mini_segment, m):
            """ Trials to iterate and constraints on mini segment split """
            seed_list = df[explanatory_var].unique().tolist() 
            print('Seed list elements : ' + str(seed_list))
            # ------ Filter marginal modalities -------
            seed_toexclude = []
            for seed in seed_list :
                if float(len(df[df[explanatory_var] == seed]))/float(len(df)) < m:
                    seed_toexclude.append(seed)

            seed_list = [x for x in seed_list if x not in seed_toexclude]
            print('\n')
            print('Seed list elements retained under minimal modality volume ' + str(m) +' : ' + str(seed_list))

            def _create_all_unique_modality_split_combinations(seed_list):
                """ returns all possible splits of modalities grouping with group length bounds: [1, len(seed_list) -1] """
                import itertools
                # - collect all possible element combinations with length [1, len(seed_list) -1] 
                all_comb = [] 
                for length in range(1, len(seed_list)):
                    for subset in itertools.combinations(seed_list, length):
                        all_comb.append(subset)    
                # - collect all possible couple combinations
                all_couples = [] 
                for o in range(len(all_comb)):
                    o_a = sorted(list(all_comb[o]))
                    o_b = sorted(list((set(seed_list) - set(all_comb[o]))))
                    all_couples.append(set(tuple(i) for i in [o_a, o_b]))     
                # - keep unique couple combinations 
                db_couples = []  
                for c in all_couples:
                    if c not in db_couples :
                        db_couples.append(c)
                db_couples = [list(x) for x in db_couples] # drop dicts and keep list types       
                print('Number of modality splits combinations : ' + str(len(db_couples)))
                return db_couples 
            trial_splits = _create_all_unique_modality_split_combinations(seed_list)
            significant_trials = []
            split = []
            split_ratio = []
            for s in range(len(trial_splits)) :
                vol_ratio = float(len(df[df[explanatory_var].map(lambda x : x in trial_splits[s][0])]))/float(len(df))
                if vol_ratio >= mini_segment and vol_ratio <= 1-mini_segment:
                    significant_trials.append(s)
                    split.append(trial_splits[s])
                    split_ratio.append(str(round(vol_ratio,2)) +"-"+ str(round(1-vol_ratio,2)))
            print('Number of significant trial splits for mini segment ' +str(mini_segment) + ' : ' + str(len(significant_trials)) +'\n')
            print("TAMAÑO " + str(split))
            return split #list

        """ Custom iterator - split_trials """
        x_iterations             = create_trial_splits_on_unique_modality_combinations(df_train, explanatory_var, mini_segment, m)

        """ Compute uplift KPIs """
        
        n_steps                  = range(len(x_iterations))
        print("Number of iterations : " + str(len(n_steps)))

        """ Iterator outputs """
        n_steps_executed         = []
        n_splits_executed        = []
        n_uplift_diff_executed   = []
        n_uplift_diff_executed_T = []
        n_stability_product      = []
  
        
        for n in n_steps :
            t =  x_iterations[n]

            groupA, groupA_T = (grupo[grupo[explanatory_var].map(lambda x : x in t[0])] for grupo in (df_train, df_test))
 
            groupB, groupB_T = (grupo[grupo[explanatory_var].map(lambda x : x in t[1])] for grupo in (df_train, df_test))

            uplift_groupA, uplift_groupA_T, uplift_groupB, uplift_groupB_T             = (self.calculate_uplift_test_canal(grupo) for grupo in (groupA, groupA_T, groupB, groupB_T))

            #uplift_eg_groupA, uplift_eg_groupA_T, uplift_eg_groupB, uplift_eg_groupB_T = (calculate_uplift_EG(df, criterion, offer, eg) for df in (groupA, groupA_T, groupB, groupB_T))

            try : 
                
                d   = compute_uplift_group_difference_pc()
                d_T = compute_uplift_group_difference_pc_T()
                
                if stability_uplift_pc() > 0 : # Minimal stability requirements
                    # Stability barrier : max distance accepted between samples of building and validation ex. default : 200% 
                    
                    if abs(self.delta_pc(d, d_T)) < s :      
                        
                        n_steps_executed.append(n)
                            
                        n_splits_executed.append(t)
                        n_uplift_diff_executed.append(d)
                        n_uplift_diff_executed_T.append(d_T)
                        # Custom stability kpi to minimize : product of inverse uplift diff and delta in test and train samples
                        n_stability_product.append(1/(10*d) * abs(self.delta_pc(d, d_T)))
            except :
                pass # in order to deal with possible NoneType in KPIs results

        if len(n_steps_executed) > 0:
            print("Solutions under constraints found : " + str(len(n_steps_executed)))

            booster_index  = [n_stability_product.index(i) for i in sorted(n_stability_product)]
            best_splits   = [n_splits_executed[i] for i in booster_index ]
            print("Best splits orderde by performance and stability : " + str(n_splits_executed[:3]))
            print("\n")
            print("Summary for split : " + str(best_splits[0]))
            o = self._classifier_split_summary(df_train, df_test,  explanatory_var, best_splits[0])

            print(o) 
            return best_splits # return full list of cutoffs to iterate

        else: 
            print("No conversion found under stability constraints")
        

    
    def filter_column(self, df, column, list_of_values):
        """
        Funcion llamada en filter_column() para pasar como parametro un dataframe
        junto a la columna que se quiera filtrar dada una lista de valores o un valor unicamente
        """
        if type(list_of_values) == list:
            df2 = df[df[column].isin(list_of_values)]
        else:
            #Si sólo le pasamos un string, se irá por aquí
            df2 = df[df[column]==list_of_values]
        return df2

    def filter_train_test(self,df_total, train, test, column, list_of_values):
        """Funcion para filtrar train, test y el df total"""

        train2 = self.filter_column(train, column, list_of_values)
        test2 = self.filter_column(test, column, list_of_values)
        total2 = self.filter_column(df_total, column, list_of_values)
        return total2, train2, test2
    
    