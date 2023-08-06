import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

from bcselector.filter_methods.cost_based_filter_methods import difference_find_best_feature, fraction_find_best_feature
from bcselector.filter_methods.no_cost_based_filter_methods import no_cost_find_best_feature
from bcselector.information_theory.j_criterion_approximations import mim, mifs, mrmr, jmi, cife

__all__ = [
    '_MockVariableSelector',
    'DiffVariableSelector',
    'FractionVariableSelector'
]

class _MockVariableSelector():
    def __init__(self):
        self.data = None
        self.target_variable = None
        self.costs = None
        self.normalized_costs = None
        self.budget = None
        self.criterion_values = []
        self.filter_values = []
        self.colnames = None
        self.stop_budget = False

        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

        self.variables_selected_order = []
        self.cost_variables_selected_order = []
        self.j_criterion_func = None

        self.total_scores = None
        self.total_costs = None
        self.no_cost_total_scores = None
        self.no_cost_total_costs = None

        self.model = None
        self.scoring_function = None
        self.beta = None
        self.number_of_features = None

        self.fig = None
        self.ax = None


    def fit(self, data, target_variable, costs, j_criterion_func = 'cife', seed = 42, budget = None, test_size = 0.2, **kwargs):
        self.variables_selected_order = []
        self.cost_variables_selected_order = []

        if 'beta' in kwargs.keys():
            self.beta = kwargs['beta']

        # data & costs
        assert isinstance(data, np.ndarray) or isinstance(data, pd.DataFrame), "Argument `data` must be numpy.ndarray or pandas.DataFrame"
        if isinstance(data,np.ndarray):
            assert isinstance(costs,list), "When using `data` as np.array, provide `costs` as list of floats or integers"
        else:
            assert isinstance(costs,(list, dict)), "When using `data` as pd.DataFrame, provide `costs` as list of floats or integers or dict {'col_1':cost_1,...}"

        if isinstance(data, pd.DataFrame):
            self.data = data.values
            self.colnames = data.columns
            if isinstance(costs,dict):
                self.costs = [costs[x] for x in data.columns]
            else:
                self.costs = costs
        else:
            self.data = data
            self.colnames = ['var_' + str(i) for i in np.arange(1,self.data.shape[1]+1)]
            self.costs = costs

        # normalized costs
        if (min(self.costs) >= 0) and (max(self.costs) <= 1):
                self.normalized_costs = self.costs
        else:
            # I add 0.0001 to avoid 0 cost feature
            self.normalized_costs = list((np.array(self.costs) - min(self.costs) + 0.0001)/(max(self.costs)-min(self.costs)+0.0001))

        assert len(self.data.shape) == 2, "For `data` argument use numpy array of shape (n,p) or pandas DataFrame" 
        assert data.shape[1] == len(costs), "Length od cost must equal number of columns in `data`"

        # target_variable
        assert isinstance(target_variable,np.ndarray) or isinstance(target_variable,pd.core.series.Series), "Use np.array or pd.Series for argument `target_variable`"

        if isinstance(target_variable,pd.core.series.Series):
            self.target_variable = target_variable.values
        else:
            self.target_variable = target_variable
        
        assert self.data.shape[0] == len(self.target_variable), "Number of rows in 'data' must equal target_variable length"

        # j_criterion_func
        j_criterion_dict = {'mim':mim,'mifs':mifs,'mrmr':mrmr,'jmi':jmi,'cife':cife}
        assert j_criterion_func in ['mim','mifs','mrmr','jmi','cife'], "Argument `j_criterion_func` must be one of ['mim','mifs','mrmr','jmi','cife']"
        self.j_criterion_func = j_criterion_dict[j_criterion_func]

        if budget is not None:
            assert isinstance(budget,(int,float)), "Argument `budget` must be float or int."
            assert budget >= 0, "Budget must be greater or equal 0."
            self.budget = budget

        # Train test split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.data, self.target_variable, test_size=test_size, random_state=seed)

    def get_ranked_variables(self):
        return self.variables_selected_order
    
    def get_ranked_costs(self):
        return self.cost_variables_selected_order

    def score(self, model, scoring_function, **kwargs):
        self.total_scores = []
        self.total_costs = []
        self.model = model
        self.scoring_function = scoring_function

        assert len(self.variables_selected_order) > 0, "Run fit method first."
        current_cost = 0

        for i,var_id in enumerate(tqdm(self.variables_selected_order, desc='Scoring')):
            cur_vars = self.variables_selected_order[0:i+1]
            self.model = self.model.fit(X=self.X_train[:,cur_vars], y=self.y_train)
            y_hat = self.model.predict_proba(self.X_test[:,cur_vars])[:,1]
            score = self.scoring_function(self.y_test, y_hat)
            current_cost += self.costs[var_id]
            self.total_scores.append(score)
            self.total_costs.append(current_cost)
    def score_no_cost(self):
        self._no_cost_score(stop_budget=self.stop_budget)
        
    def plot_scores(self, budget = None, compare_no_cost_method = False, savefig=False, annotate=False, annotate_box=False, figsize=(12,8), bbox_pos = (0.72, 0.60), **kwargs):
        assert self.total_scores, "Run `score` method first."
        
        self.fig, self.ax = plt.subplots(figsize=figsize)
        if budget is not None:
            assert isinstance(budget,(int,float)), "Argument `budget` must be float or int."
            self.ax.axvline(x=budget, linewidth=3, label = f'budget={budget:.2f}')
        elif self.budget is not None:
            self.ax.axvline(x=self.budget, linewidth=3, label = f'budget={self.budget:.2f}')
        else:
            pass

        move_horizontal = max(self.total_costs)/100
        move_vertical = max(self.total_scores)/100
        if compare_no_cost_method is True:
            self._no_cost_score(stop_budget=self.stop_budget)
            self.ax.plot(self.no_cost_total_costs, self.no_cost_total_scores, linestyle='--', marker='o', color='r', label = 'no regard to cost')
            self.ax.plot(self.total_costs, self.total_scores, linestyle='--', marker='o', color='b', label = 'with regard to costs')
            self.ax.legend(prop={"size":16})

            if annotate == True:
                move_horizontal = max(self.no_cost_total_costs + self.total_costs)/100
                move_vertical = max(self.no_cost_total_scores + self.total_scores)/100
                costs_normalized_to_alpha = list((
                    np.array(self.no_cost_cost_variables_selected_order)\
                     - min(self.costs) + 0.7)\
                     /(max(self.costs)\
                     -min(self.costs)+0.7))
                for i, txt in enumerate(self.no_cost_variables_selected_order):
                    self.ax.annotate(
                        txt, 
                        (self.no_cost_total_costs[i], self.no_cost_total_scores[i]),
                        bbox=dict(boxstyle="round", alpha=costs_normalized_to_alpha[i], color='red'), 
                        xytext=(self.no_cost_total_costs[i]+move_horizontal, self.no_cost_total_scores[i]+move_vertical*0.5), 
                        size=10,
                        color = 'white')
        else:
            self.ax.plot(self.total_costs, self.total_scores, linestyle='--', marker='o', color='b')
        
        if annotate == True:
            costs_normalized_to_alpha = self.normalized_costs = list((
                    np.array(self.cost_variables_selected_order)\
                     - min(self.costs) + 0.7)\
                     /(max(self.costs)\
                     -min(self.costs)+0.7))
            for i, txt in enumerate(self.variables_selected_order):
                self.ax.annotate(
                    txt, 
                    (self.total_costs[i], self.total_scores[i]),
                    bbox=dict(boxstyle="round", alpha=costs_normalized_to_alpha[i], color='blue'), 
                    xytext=(self.total_costs[i]+move_horizontal, self.total_scores[i]-move_vertical),
                    size=10,
                    color = 'white')


        self.ax.set_title('Model ' + self.scoring_function.__name__ + ' vs cost' , fontsize = 18)
        self.ax.tick_params(axis='both', which='major', labelsize=16)
        self.ax.set_xlabel('Cost', fontsize = 16)
        self.ax.set_ylabel(self.scoring_function.__name__, fontsize = 16)

        # BBox with feature names
        if annotate_box == True:
            variables_idx = set(self.variables_selected_order).union(set(self.no_cost_variables_selected_order))
            variables_names = [self.colnames[i] for i in variables_idx]
            variables_costs = [self.costs[i] for i in variables_idx]
            textstr = '\n'.join([str(idx) + ': ' + name + f' C={cost:.2f}' for idx,name,cost in zip(variables_idx, variables_names, variables_costs)])
            props = dict(boxstyle='round', facecolor='gray', alpha=0.1)
            self.ax.text(bbox_pos[0], bbox_pos[1], textstr, transform=self.ax.transAxes, fontsize=14,verticalalignment='top', bbox=props, size=12, color = 'gray')

        if savefig == True:
            assert kwargs.get('fig_name'), "Must specify `fig_name` as key word argument"
            name = kwargs.pop('fig_name')
            plt.savefig(name, **kwargs)
        plt.tight_layout()
        plt.show()

    def _no_cost_score(self, stop_budget=False, **kwargs):
        # Rank variables with NoCostVariableSelector
        S = set()
        U = set([i for i in range(self.data.shape[1])])

        self.no_cost_variables_selected_order = []
        self.no_cost_cost_variables_selected_order = []

        for i in tqdm(range(self.number_of_features), desc='Selecting No-cost Features'):
            k, _, cost = no_cost_find_best_feature(j_criterion_func = self.j_criterion_func, 
                                data = self.data, 
                                target_variable = self.target_variable, 
                                prev_variables_index = list(S),
                                possible_variables_index = list(U),
                                costs = self.costs,
                                beta = self.beta)
            S.add(k)
            if stop_budget is True and (sum(self.no_cost_cost_variables_selected_order) + cost) >= (self.budget or np.inf):
                break
            self.no_cost_variables_selected_order.append(k)
            self.no_cost_cost_variables_selected_order.append(cost)
            U = U.difference(set([k]))
            if len(S) == self.number_of_features:
                break

        current_cost = 0
        self.no_cost_total_scores = []
        self.no_cost_total_costs = []

        for i,var_id in enumerate(self.no_cost_variables_selected_order):
            cur_vars = self.no_cost_variables_selected_order[0:i+1]
            self.model = self.model.fit(X=self.X_train[:,cur_vars], y=self.y_train)
            y_hat = self.model.predict_proba(self.X_test[:,cur_vars])[:,1]
            score = roc_auc_score(self.y_test, y_hat)
            current_cost += self.costs[var_id]
            self.no_cost_total_scores.append(score)
            self.no_cost_total_costs.append(current_cost)

class DiffVariableSelector(_MockVariableSelector):
    """Ranks all features in dataset with difference cost filter method.

    Parameters
    ----------

    Attributes
    ----------

    Examples
    --------

    """
    def fit(self, data, target_variable, costs, lamb,j_criterion_func = 'cife', number_of_features = None, budget = None, stop_budget = False, **kwargs):
        # lamb
        assert isinstance(lamb, int) or isinstance(lamb, float), "Argument `lamb` must be integer or float"
        self.lamb = lamb
        self.stop_budget = stop_budget
        super().fit(data=data, target_variable=target_variable, costs=costs, j_criterion_func=j_criterion_func, budget=budget, **kwargs)

        if number_of_features is None:
            self.number_of_features = self.data.shape[1]
        else:
            self.number_of_features = number_of_features
        if self.budget is None and stop_budget == True:
            warnings.warn("Unused argument `stop_budget`. Works only with `budget` argument.")
        
        S = set()
        U = set([i for i in range(self.data.shape[1])])

        self.variables_selected_order = []
        self.cost_variables_selected_order = []

        for i in range(self.number_of_features):
        # for i in tqdm(range(self.number_of_features), desc=f'Selecting Features for r = {self.lamb:0.3f}'):
        # while len(U) > 0:
            k, filter_value, criterion_value, cost = difference_find_best_feature(j_criterion_func = self.j_criterion_func, 
                                                                                    data = self.X_train, 
                                                                                    target_variable = self.y_train, 
                                                                                    prev_variables_index = list(S),
                                                                                    possible_variables_index = list(U),
                                                                                    costs = self.costs,
                                                                                    normalized_costs=self.normalized_costs,
                                                                                    lamb = self.lamb,
                                                                                    **kwargs)
            S.add(k)

            if stop_budget is True and (sum(self.cost_variables_selected_order) + cost) >= (self.budget or np.inf):
                break

            self.variables_selected_order.append(k)
            self.cost_variables_selected_order.append(cost)
            self.criterion_values.append(criterion_value)
            self.filter_values.append(filter_value)
            U = U.difference(set([k]))

            if len(S) == self.number_of_features:
                break

class FractionVariableSelector(_MockVariableSelector):
    """Ranks all features in dataset with difference cost filter method.

    Parameters
    ----------

    Attributes
    ----------

    Examples
    --------

    """
    def fit(self, data, target_variable, costs, r, j_criterion_func = 'cife', number_of_features = None, budget = None, stop_budget = False, **kwargs):
        # r
        assert isinstance(r, int) or isinstance(r, float), "Argument `r` must be integer or float"
        self.r = r
        self.stop_budget = stop_budget

        super().fit(data=data, target_variable=target_variable, costs=costs, j_criterion_func=j_criterion_func, budget=budget, **kwargs)
        
        if number_of_features is None:
            self.number_of_features = self.data.shape[1]
        else:
            self.number_of_features = number_of_features
        if self.budget is None and stop_budget == True:
            warnings.warn("Unused argument `stop_budget`. Works only with `budget` argument.")

        S = set()
        U = set([i for i in range(self.data.shape[1])])

        self.variables_selected_order = []
        self.cost_variables_selected_order = []

        for i in range(self.number_of_features):
        # for i in tqdm(range(self.number_of_features), desc=f'Selecting Features for r = {self.r:0.3f}'):
        # while len(U) > 0:
            k, filter_value, criterion_value, cost = fraction_find_best_feature(j_criterion_func = self.j_criterion_func, 
                                data = self.data, 
                                target_variable = self.target_variable, 
                                prev_variables_index = list(S),
                                possible_variables_index = list(U),
                                costs = self.costs,
                                normalized_costs=self.normalized_costs,
                                r = self.r,
                                **kwargs)
            S.add(k)

            if stop_budget is True and (sum(self.cost_variables_selected_order) + cost) >= (self.budget or np.inf):
                break

            self.variables_selected_order.append(k)
            self.cost_variables_selected_order.append(cost)
            self.criterion_values.append(criterion_value)
            self.filter_values.append(filter_value)
            U = U.difference(set([k]))
            if len(S) == self.number_of_features:
                break


class NoCostVariableSelector(_MockVariableSelector):
    """Ranks all features in dataset with difference cost filter method.

    Parameters
    ----------

    Attributes
    ----------

    Examples
    --------

    """
    def fit(self, data, target_variable, costs, j_criterion_func = 'cife', **kwargs):

        super().fit(data, target_variable, costs, j_criterion_func, **kwargs)
        
        S = set()
        U = set([i for i in range(self.data.shape[1])])

        self.variables_selected_order = []
        self.cost_variables_selected_order = []

        for i in tqdm(range(len(U)), desc='Scoring No-cost Features'):
            k, _, cost = no_cost_find_best_feature(j_criterion_func = self.j_criterion_func, 
                                data = self.data, 
                                target_variable = self.target_variable, 
                                prev_variables_index = list(S),
                                possible_variables_index = list(U),
                                costs = self.costs)
            S.add(k)
            self.variables_selected_order.append(k)
            self.cost_variables_selected_order.append(cost)
            U = U.difference(set([k]))
            if len(S) == self.number_of_features:
                break

    def plot_scores(self, model):
        super().plot_scores(model)
        plt.show()

        