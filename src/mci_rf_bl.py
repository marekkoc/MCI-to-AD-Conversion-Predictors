"""
Auxiliary Random Forests functions.

(C) MCI group.

Created: 2021.05.18 / Updated: 2021.06.23
"""

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from pathlib import Path


def confusion_matrix_coefficients_TPTNFPFN(X, y_true, y_pred):
    """
    Calculate usion matrix coefficients.
    
    Parameters:
    -------------
    X - test or validation (in e.g. CV10) set
    
    C: 2021.05.18./ U: 2021.05.18
    """

    X_extended = X.copy()
    X_extended['y_true_'] = np.where(y_true == 1, 'cAD', 'sMCI')
    X_extended['y_pred_'] = np.where(y_pred == 1, 'cAD', 'sMCI')
    
    # https://www.statology.org/compare-two-columns-in-pandas/
    conditions = [(X_extended['y_true_'] == 'cAD') &  (X_extended['y_pred_'] == 'cAD'),
                 (X_extended['y_true_'] == 'sMCI') &  (X_extended['y_pred_'] == 'sMCI'),
                 (X_extended['y_true_'] == 'sMCI') &  (X_extended['y_pred_'] == 'cAD'),
                 (X_extended['y_true_'] == 'cAD') &  (X_extended['y_pred_'] == 'sMCI')]
    choices = ['TP', 'TN', 'FP', 'FN']
    X_extended['CM_pred_'] = np.select(conditions, choices, default='Error')
    
    return X_extended
    
    
def link_prediction_results_with_other_subject_features(bl_table, predictions_df, cols2, filename='', save=True, results_dir=Path().cwd()):
    """
    Links prediction results with all other subject features.
    
    Parameters:
    ---------------
    bl_table - the bl table with all feature subjects to read from.
    predictions_df - a table with prediction results (i.e. X_extended with y_pred, y_true_, CM_pred_ )
    cols2 - an extra columns to select from `prediction_df` e.g. in CV process ([f'CV{FOLDS}F_',  f'CV{FOLDS}_Usage_'])
    
    C: 2021.05.18./ U: 2021.05.18
    """
    
    # get 'TRAIN' subset from the loaded df (train + test)
    bl_pred = bl_table.loc[predictions_df.index]
    # select some columns from misclassified subject df
    cols = ['y_true_', 'y_pred_', 'CM_pred_'] + cols2
    # merge both tables by index
    bl_pred = bl_pred.merge(predictions_df[cols], how='left', left_index=True, right_index=True, indicator=f'MERGE_predictions_')
    print(f'\nSubjects in the predictions table: {bl_pred.shape[0]}\n')
    
    if save:     
        bl_predictions_name = results_dir / filename
        bl_pred.sort_values(by=['RID'], inplace=True) 
        bl_pred.to_csv(bl_predictions_name, index=True)
        
        print(f'Predictions have been saved to a file:')
        print(f'\t\t{bl_predictions_name}')
        
    return bl_pred
 
    
def plot_mean_feature_importnce_cv(df, file_name_prefix, folds, figsize=(20,10), orientation='h', save=True, results_dir=Path().cwd()):
    """
    C: 2021.05.03 / U: 2021.05.03
    """
    # transfer 2D df to 1D df (melt)
    #https://stackoverflow.com/questions/40877135/plotting-two-columns-of-dataframe-in-seaborn
    # label text size
    #https://stackoverflow.com/questions/12444716/how-do-i-set-the-figure-title-and-axes-labels-font-size-in-matplotlib

    fig, ax = plt.subplots(figsize=figsize)
    fig.suptitle(f'Mean feature importance for k={folds} folds', fontsize=26,fontweight='bold')
    ax.set_xlabel('xlabel', fontsize=24)
    ax.set_ylabel('ylabel', fontsize=24) 
    ax.tick_params(labelsize=14)

    tidy = df.melt(id_vars='feature').rename(columns=str.title)
    tidy = tidy.sort_values(by=['Value'], ascending=False)
    if orientation == 'h':
        sns.barplot(x='Value', y='Feature', ci='sd', capsize=.2, data=tidy, ax=ax, orient=orientation)
    else:
        sns.barplot(x='Feature', y='Value', ci='sd', capsize=.2, data=tidy, ax=ax, orient=orientation)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    sns.despine(fig)

    if save:
        file_name_prefix_ext = f'{file_name_prefix}-CV{folds}-feat-importance-{orientation}.png'
        file_name_prefix_path = results_dir / file_name_prefix_ext
        plt.savefig(file_name_prefix_path)
        print(f'Mean featue importacne plot saved to:\n\t\t{file_name_prefix_path}\n')
        

    plt.grid()
    plt.show()
    

def plot_single_feature_importnce(df, file_name_prefix, figsize=(20,10), orientation='h', save=True, results_dir=Path().cwd()):
    """

    C: 2021.05.04 / U: 2021.05.04
    """

    fig, ax = plt.subplots(figsize=figsize)

    if orientation == 'h':
        sns.barplot(x=df, y=df.index, ci='sd', capsize=.2,  orient=orientation)
    else:
        sns.barplot(x=df.index, y=df, ci='sd', capsize=.2,  orient=orientation)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45) 


    #sns.barplot(x=df, y=df.index, ci='sd')
    # Add labels to your graph
    ax.set_xlabel('Feature Importance Score', fontsize=24)
    ax.set_ylabel('Features',fontsize=24)
    ax.set_title("RF Feature Importance", fontsize=24, fontweight='bold', pad=20)
    ax.tick_params(labelsize=14)

    if save:
        file_name_prefix_ext = f'{file_name_prefix}-TEST-feat-importance-{orientation}.png'
        file_name_prefix_path = results_dir / file_name_prefix_ext
        plt.savefig(file_name_prefix_path)
        print(f'Mean featue importacne plot saved to:\n\t\t{file_name_prefix_path}\n')
    
    plt.grid()
    plt.show()
    

def plot_confusion_matrix_CV(conf_mat_mean, conf_mat_mean_prc, folds, file_name_number, file_name_prefix, result_dir=Path().cwd(), save=True):
    """
    C: 2021.06.23 / U: 2021.06.23
    """
    
    title = f'Confusion matrix - CV{folds} ({file_name_number})'
    fig, ax = plt.subplots(figsize=(10,10))
    ax.set_aspect(aspect=1)
    lab = ['sMCI', 'cAD']
    res = sns.heatmap(conf_mat_mean, annot=True, xticklabels=lab, yticklabels=lab, ax=ax,annot_kws={"fontsize":20}, fmt='.1f')
    ax.tick_params(axis='both', which='major', labelsize=18)
    _ = ax.set_title(title, size=24, fontweight='bold')


    for t,p in zip(res.texts, conf_mat_mean_prc.flat):
        p = np.asarray(np.round(p,0), int)
        t.set_text(t.get_text() + f' ({p}%)')

    file_name_prefix_ext = f'{file_name_prefix}-conf-matrix-CV{folds}.png'
    file_name_prefix_path = result_dir / file_name_prefix_ext
    print(f'Confusion matrix saved to:\n\n\t\t{file_name_prefix_path}\n')
    
    if save:
        plt.savefig(file_name_prefix_path)
    plt.show()
    
    
def plot_confusion_matrix_TEST(conf_matrix_test, conf_matrix_test_prc, file_name_number, file_name_prefix, results_dir=Path().cwd(), save=True):
    """
    C: 2021.06.23 / U: 2021.06.23
    """
    title = f'Confusion matrix - TEST ({file_name_number})'
    fig, ax = plt.subplots(figsize=(10,10))
    ax.set_aspect(aspect=1)
    lab = ['sMCI', 'cAD']
    res = sns.heatmap(conf_matrix_test, annot=True, xticklabels=lab,
                      yticklabels=lab, ax=ax,annot_kws={"fontsize":20}, fmt='.1f')
    ax.tick_params(axis='both', which='major', labelsize=18)
    _ = ax.set_title(title, size=24, fontweight='bold')


    for t,p in zip(res.texts, conf_matrix_test_prc.flat):
        p = np.asarray(np.round(p,0), int)
        t.set_text(t.get_text() + f' ({p}%)')

    file_name_prefix_ext = f'{file_name_prefix}-conf-matrix-TEST.png'
    file_name_prefix_path = results_dir / file_name_prefix_ext
    
    if save:
        plt.savefig(file_name_prefix_path)
    plt.show()
    
    
def plot_confusion_matrix_TEST_IR(conf_matrix_test, conf_matrix_test_prc, file_name_number, file_name_prefix,title='bla bla', results_dir=Path().cwd(), save=True):
    """
    This is to create the Titles of the Confusion Matrix for Ingrid.
    
    C: 2021.06.23 / U: 2021.11.28
    """
    #title = f'Confusion matrix - TEST ({file_name_number})'
    fig, ax = plt.subplots(figsize=(10,10))
    ax.set_aspect(aspect=1)
    lab = ['sMCI', 'cAD']
    res = sns.heatmap(conf_matrix_test, annot=True, xticklabels=lab,
                      yticklabels=lab, ax=ax,annot_kws={"fontsize":20}, fmt='.1f')
    ax.tick_params(axis='both', which='major', labelsize=18)
    _ = ax.set_title(title, size=24, fontweight='bold')


    for t,p in zip(res.texts, conf_matrix_test_prc.flat):
        p = np.asarray(np.round(p,0), int)
        t.set_text(t.get_text() + f' ({p}%)')

    file_name_prefix_ext = f'{file_name_prefix}-conf-matrix-TEST.png'
    file_name_prefix_path = results_dir / file_name_prefix_ext
    
    if save:
        plt.savefig(file_name_prefix_path)
    plt.show()
    