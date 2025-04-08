"""
Auxiliary DATA BALANCING functions on MCI tables.

(C) MCI group.

Update:
Renamed features:
    - AGE_bin_ --> Age_bin_
    - AGE_rounded_ ---> Age_rounded_

Created: 2021.03.17 / Updated: 2021.03.22
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import StratifiedShuffleSplit

import mci_info as minfo



def train_test_split_baseline(bl_df, age_bins=[50,60,70,80,95], split_categories=['Age_bin_', 'Subgroup_', 'PTGENDER'],
                              random_state=42, test_size=0.2, df_name='bl', sh=True):
    """
    Splits base line table to train / test sets with stratification based on:
        - 'Age_bin_',
        - 'Subgroup_',
        - 'PTGENDER'
        
     Parameters:
     -----------------------
    bl_df - dataframe, MUST BE baseline (bl) with a sigle row for each subject,
    age_bins - threshold Age_rounded to bins
    split_categories - a list of categories to split
    
    
    C: 2021.03.17 / M: 2021.03.31
    """

    age_bin_labels = [f'({age_bins[i]}-{age_bins[i+1]}]' for i in range(len(age_bins[:-1]))]
    bl_df['Age_bin_'] = pd.cut(bl_df.Age_rounded_, bins=age_bins, labels=age_bin_labels)
    if sh:
        print(f'A new column "Age_bin_" is added to the "{df_name}" table')

    # splitting 
    split = StratifiedShuffleSplit(n_splits=1, test_size=test_size, random_state=random_state)

    for train_i, test_i in split.split(bl_df, bl_df[split_categories]):
        train_set = bl_df.iloc[train_i]
        test_set = bl_df.iloc[test_i]

    train_set = train_set.assign(Usage_='train')
    test_set = test_set.assign(Usage_='test')
    if sh:
        print(f'A new column "Usage_" is added to the "{df_name}" table')

    bl_new = pd.concat([train_set, test_set])
    return bl_new


def check_train_test_bl_balance(bl, feature_name='Age_bin_', display_type='%'):
    """
    Compares train, test ant the whole set regarding some categorical feauture. It uses mci_info.feature_split_info() function to count number of instances in each subcategory (by values_count()). display type is by percentage "%", counts "#" or both "%#".    
    
    C: 2021.03.17 / M: 2021.03.17
    """
    
    train_set = bl.loc[bl.Usage_ == 'train']
    test_set = bl.loc[bl.Usage_ == 'test']    

    train_age_group = minfo.feature_split_info(train_set, feature_name, display_type, col_name='train_set')
    test_age_group = minfo.feature_split_info(test_set, feature_name, display_type, col_name='test_set')
    train_test_age_group = pd.merge(train_age_group, test_age_group, how='left', on=feature_name, suffixes=['LEFT', 'RIGHT'])

    bl_age_group = minfo.feature_split_info(bl, feature_name, display_type, col_name='bl (all)')
    all_age_group = pd.merge(train_test_age_group, bl_age_group, how='left', on=feature_name, suffixes=['LEFT', 'RIGHT'])

    return all_age_group.sort_values(by=feature_name)


def plot_subgroup_distributions(df, split_feature='PTGENDER',p0_hue='Subgroup_', suptitle='A Title'):
    """
    
    C: 2021.03.17 / M:2021.03.17
    """
    sns.set_context("paper", rc={"font.size":16, "axes.titlesize":16,"axes.labelsize":16,'xtick.labelsize':'small', 'ytick.labelsize':'small'})
    sns.set_style("ticks", {"xtick.major.size": 12, "ytick.major.size": 12})

    #sns.set_style("dark")
    f,ax = plt.subplots(1,6, figsize=(25,8))
    ax0, ax1, ax2, ax3, ax4, ax5 = ax

    sns.set_style("darkgrid")
    p0 = sns.histplot(data=df, x=split_feature, hue=p0_hue, ax=ax0, multiple='stack').set_title('#Count')
    p1 = sns.histplot(data=df, x=split_feature, hue='Age_bin_', ax=ax1, multiple='stack').set_title('#Age bins')
    p2 = sns.boxplot(y='Age_rounded_', x=split_feature, data=df, width=0.5, ax=ax2).set_title('AGE')
    p3 = sns.boxplot(y='Participation_length_yr_', x=split_feature, data=df, width=0.5, ax=ax3).set_title('Treatment lenght')
    p4 = sns.boxplot(y='ADAS13_adni_Nr_', x=split_feature, data=df, width=0.5, ax=ax4).set_title('#ADAS 13')
    p5 = sns.boxplot(y='Visits_Nr_', x=split_feature, data=df, width=0.5, ax=ax5).set_title('#Visits')
    
    for a in ax:
        a.grid(True)

    plt.subplots_adjust(wspace=0.4)
    _ = plt.suptitle(suptitle, fontweight='bold', fontsize=24)
    
    
def plot_subgroup_distributions_to_paper(df, split_feature='PTGENDER',p0_hue='Subgroup_', suptitle='', save_name='A name' ):
    """
    
    C: 2021.03.17 / M:2022.04.07
    """
    sns.set_context("paper", rc={"font.size":16, "axes.titlesize":16,"axes.labelsize":16,'xtick.labelsize':'small', 'ytick.labelsize':'small'})
    sns.set_style("ticks", {"xtick.major.size": 12, "ytick.major.size": 12})

    #sns.set_style("dark")
    f,ax = plt.subplots(1,4, figsize=(25,8))
    #ax0, ax1, ax2, ax3, ax4, ax5 = ax
    ax0, ax1, ax2, ax3 = ax

    sns.set_style("darkgrid")
    p0 = sns.histplot(data=df, x=split_feature, hue=p0_hue, ax=ax0, multiple='stack')
    p0.set(xlabel='#Subjects')
    
    p1 = sns.histplot(data=df, x=split_feature, hue='Age_bin_', ax=ax1, multiple='stack')
    p1.set(xlabel='#Subjects')
    
    p2 = sns.boxplot(y='Age_rounded_', x=split_feature, data=df, width=0.5, ax=ax2)
    p2.set(ylabel='Age')
    
    p3 = sns.boxplot(y='Participation_length_yr_', x=split_feature, data=df, width=0.5, ax=ax3)
    p3.set(ylabel='Participation length in years')
    
    #p4 = sns.boxplot(y='ADAS13_adni_Nr_', x=split_feature, data=df, width=0.5, ax=ax4).set_title('#ADAS 13')
    #p5 = sns.boxplot(y='Visits_Nr_', x=split_feature, data=df, width=0.5, ax=ax5).set_title('#Visits')
    
    for a in ax:
        a.grid(True)
    for p in [p0,p1,p2,p3]:
        p.set(xlabel=None)

    plt.subplots_adjust(wspace=0.4)
    _ = plt.suptitle(suptitle, fontweight='bold', fontsize=24)
    
    plt.savefig(save_name + '.pdf')
    
    
    