"""
Auxiliary feature permutation functions.

(C) MCI group.

Created: 2021.06.23 / Updated: 2021.09.14
"""
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from pathlib import Path

from sklearn import metrics
from sklearn.base import clone


def _get_group_names(features_dct):
    """
    Get groups and their names from dict with name (a key) and group (a value, a list of feature names). Elements in the features_dct that are not a list, are skipped.
    
    Usage:
    ----------------------
    Input:
    feature_dct - a dct with group name as a key, and list o features as a value.
    
    Output:
    a list of strings in a format: {key}:{value}
    
    
    C: 2021.06.23 / U: 2021.09.14
    """
    return [f'{k}:{v}' for k,v in features_dct.items() if isinstance(v, list)]

def _print_group_names(features_dct):
    """
    Print groups and their names from dict with name (a key) and group (a value, a list of feature names). Elements in the features_dct that are not a list, are not printed out.
    
    Usage:
    ----------------------
    Input:
    feature_dct - a dct with group name as a key, and list o features as a value.
    
    Output:
    a list of strings in a format: {key}:{value}
    
    C: 2021.06.23 / U:2021.06.23
    """
    [print(f'{k}:{v}') for k,v in features_dct.items() if isinstance(v, list)]


def _get_4_scores(y_true, y_pred):
    """
    Calculate and return 4 scores: f1, ass, recall and precision.
    
    C: 2021.05.20 / U: 2021.05.20
    """    
    f1 = metrics.f1_score(y_true, y_pred)
    acc = metrics.accuracy_score(y_true, y_pred)
    recall = metrics.recall_score(y_true, y_pred)
    prec = metrics.precision_score(y_true, y_pred)
    return f1, acc, recall, prec


def _get_feature_group_info(column_list, groups, verbose):
    """
    
    Returns:
    ------------------------------------------
    # feture names linked as a groups and single - [list]
    all_features = [['AGE', 'FAQ'],
                     ['LRHHC_n_long', 'LRLV_n_long'],
                     'AVDEL30MIN_neuro',
                     'AVDELTOT_neuro']
                     
    # feture and group names - [dictionary]
    all_feature_names = {'Group_0': ['AGE', 'FAQ'],
                         'Group_1': ['LRHHC_n_long', 'LRLV_n_long'],
                         'AVDEL30MIN_neuro': 'AVDEL30MIN_neuro',
                         'AVDELTOT_neuro': 'AVDELTOT_neuro'}
                         
    
    DODAC:
     - group_names - liste z nazwami grup zamiast automatycznego generowania nazw (Group_0, Group_1,...)
    
    C: 2021.06.23 / U:2021.06.23
    """
    feat_list = []
    for g in groups:
        feat_list.extend(g)
        
    # check feature names (spelling mistakes)
    no  = [n for n in feat_list if n not in column_list]
    if no:
        print(f'\nWrong names ({len(no)}/{len(feat_list)}):\n\t{no} ')
        print('\n*** Fix it NOW!!!\n\t\tha ha ha ;D\n\n')
        print(f'Valid feature names:\n{column_list.to_list()}')
        return

    # divide by groupS and 'single' features
    # subtract groups from all features to get onlu singles
    singles = set(column_list)    
    for g in groups:
        singles = singles.difference(set(g))        
    # list wiht all features (groups and singles)
    all_features = groups + list(sorted(singles))   
    
    # an extra dict to replace list of features (a group) with an name Group_0, Group_1, ...
    all_feature_names = {}
    for k, f in enumerate(all_features):
        if isinstance(f,list):
            all_feature_names[f'Group_{k}']=f
        else:
            all_feature_names[f]=f       
    # info (optonal)
    if  verbose:    
        # print info
        print(f'All features:\n\t{column_list.to_list()}')    
        print('\nFeature groups:')
        for g in groups:
            print(f'\t{g}')
        print(f'\nSingle features:\n\t{sorted(list(singles))}')
        print('\n\n')
    
    return all_features, all_feature_names



def shuffle_features_with_groups(rf, X, y, groups=[], precission=2, verbose=True, random_state=None,
                                 repetitions=100, sortBy=None, ascending=True):
    """
    Feature permutation. Function permutes featureas from a X set, some of them can be joined and permuted in groups.
    
    Parameters:
    --------------------
    groups - a nested list. Contains grouped feature namse in separate lists e.g.
                                                    gropus= [['a1','a2','a3'], ['b1','b2','b3','b4'], ['c1','c2']]
    random_state - int number or None. If None, randomly selected random seed value (each run gives different result).
    repetions - nr of repetitions to average the restult. If repetitions > 0 then random state is automatically set to None. This will print random feature permutation (random values).
    sortBy - a feature name to sort values by : 'f1'/'acc'/'recall'/'prec'
    ascending - wheter sortBy in ascending or descending order (True/False).
    
    
    C: 2021.05.01 / U: 2021.06.24
    """
    column_list = X.columns
    X = X.copy()
    y = y.copy()
    
    if repetitions > 0:
        rep = repetitions # shorter name
        random_state = None # random seed (each run different)
        print(f'Repetition(s) = {rep+1}\nAveraging mode!\nrandom_state = {random_state}\n')
    else:
        rep = 1
        print(f'Repetition(s) = {rep+1}\nSingle permutation mode\nrandom_state = {random_state}\n')
    
    ### INFO PART ##############################################
    all_features, all_feature_names = _get_feature_group_info(column_list, groups, verbose)
    #print(all_features)
    #print(all_feature_names)
    ### END OF INFO PART ##############################################    
    
    # prediction
    y_pred = rf.predict(X)  
    
    # baseline scores
    f1_baseline, acc_baseline, recall_baseline, prec_baseline = _get_4_scores(y, y_pred)
    
    # list for score drops
    f1_list, acc_list, recall_list, prec_list = [],[],[],[]        
    
    # feature(s) loop
    for k, cols in enumerate(all_features):        
        # permutation of the selected column(s)
        save = X[cols].copy()
        #X[cols] = np.random.permutation(X[cols])
        
        f1_a, acc_a, recall_a, prec_a = np.zeros(rep), np.zeros(rep), np.zeros(rep), np.zeros(rep)
        # repetition loop
        for r in range(rep):
            X[cols] = np.random.RandomState(random_state).permutation(X[cols])

            y_pred_f = rf.predict(X)               
            # arrays for selectd feature permutation scores
            f1_f, acc_f, recall_f, prec_f = _get_4_scores(y, y_pred_f)        
            # difference between baseline and feature scores        
            f1_a[r] = f1_baseline - f1_f
            acc_a[r] = acc_baseline - acc_f
            recall_a[r] = recall_baseline - recall_f
            prec_a[r] = prec_baseline - prec_f
        
        f1_list.append(f1_a.mean())
        acc_list.append(acc_a.mean())
        recall_list.append(recall_a.mean())
        prec_list.append(prec_a.mean())
        # restore the initial column value
        X[cols] = save 
        
        
    df = pd.DataFrame.from_dict({'f1':f1_list, 'acc':acc_list, 'recall':recall_list, 'prec':prec_list})
    df.index = all_feature_names.keys()       
    
    if sortBy:
        df = df.sort_values(sortBy, ascending=ascending)        
    return df.round(precission), all_feature_names



def plot_permuted_features(df, file_name_prefix, type, save=True, results_dir=Path().cwd(), figsize=(22,12), title_suffix='' ):
    """
    type = string, one of these values: empty/-drop/-random
    title_suffix - some additional text to display in the main title
    
    TO DO:
    - zmienic nazwe na plot features
    - dodac mozliwosc wyboru ktore i ile wspolczynniki rysujemy (f1,acc,..)
    - dodac mozlowsc zmiany nazwy pliku podczas zapisu...aby rozroznic nazyw grup cech...
    - 
    
    C:2021.06.23 / U:2021.06.24
    """

    fig, ax = plt.subplots(2,2, sharex=True, sharey=True, figsize=figsize)
    axs = ax.flat[:]

    for ax, f in zip(axs, df.columns.to_list()):
        sns.barplot(x=df[f], y=df.index, ax=ax)

        # Add labels to your graph
        ax.set_xlabel(ax.get_xlabel(), fontsize=18, fontweight='bold')
        ax.xaxis.set_label_position('top')

        #ax.set_ylabel('Feature(s)', fontsize=18)
        #ax.set_title(f, fontsize=20, pad=20, fontweight='bold')
        ax.tick_params(labelsize=18)
        ax.grid(True)

    plt.subplots_adjust(hspace=0.15)
    plt.suptitle(f'Feature importance. {title_suffix}', fontsize=26, fontweight='bold')
    
    if save:
        file_name_prefix_ext = f'{file_name_prefix}-{type}-features.png'
        file_name_prefix_path = results_dir / file_name_prefix_ext
        plt.savefig(file_name_prefix_path)
        print(f'Shuffle [group] feature(s) saved to:\n\t\t{file_name_prefix_path}\n')

    plt.show()
    
    
def dropcol_importances(rf, X_train, y_train, X_test, y_test, random_state=42, groups=[], verbose=True, precission=2):
    """
    C: 2021.06.23 / U: 2021.06.23
    """
    column_list = X_train.columns
    X_train = X_train.copy()
    y_train = y_train.copy()
    X_test = X_test.copy()
    y_test = y_test.copy()
    
    ### INFO PART ##############################################
    all_features, all_feature_names = _get_feature_group_info(column_list, groups, verbose)  
#     print('ALL_FEATURES\n')
#     print(all_features)
#     print('ALL_FEATURE_NAMES\n')
#     print(all_feature_names)
#     print('NR OF FEATURES:\n')
#     print(len(X_train.columns))
    ### END OF INFO PART ##############################################    
   
    
    rf_ = clone(rf)
    rf_.random_state = random_state
    rf_.fit(X_train, y_train)
    y_test_pred = rf_.predict(X_test)
    # baseline scores
    f1_baseline, acc_baseline, recall_baseline, prec_baseline = _get_4_scores(y_test, y_test_pred)
    # list for score drops
    f1_list, acc_list, recall_list, prec_list = [], [], [] ,[]  
    
    
    for k, cols in enumerate(all_features):
        X_train_drop = X_train.drop(cols, axis=1)
        X_test_drop = X_test.drop(cols, axis=1)
        
        #################################
#         print(30*'x')
#         print('Columns dropped:\n')
#         print(str(cols))
#         print('Columns in df:\n')
#         print(X_train_drop.columns.to_list())
        ####################################
        
        rf_ = clone(rf)
        rf_.random_state = random_state
        rf_.fit(X_train_drop, y_train)
        
        y_test_drop_pred = rf_.predict(X_test_drop)
        
        # selectd feature permutation scores
        f1_f, acc_f, recall_f, prec_f = _get_4_scores(y_test, y_test_drop_pred)  
        
        # difference between baseline and feature scores        
        f1_list.append(f1_baseline - f1_f)
        acc_list.append(acc_baseline - acc_f)
        recall_list.append(recall_baseline - recall_f)
        prec_list.append(prec_baseline - prec_f)        
        
    
    df = pd.DataFrame.from_dict({'f1':f1_list, 'acc':acc_list, 'recall':recall_list, 'prec':prec_list})
    df.index = all_feature_names.keys()    
    
    return df.round(precission), all_feature_names
