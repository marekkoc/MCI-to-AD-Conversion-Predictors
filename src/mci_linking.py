"""
Auxiliary function to LINK tables with other SCORES.


In this module each SCORE table is linked in a separate function.

Based on:
 mci_link_long.py


(C) MCI group.

Created: 2021.03.02
Updated: 2021.10.04
"""

import numpy as np
import pandas as pd
from pathlib import Path
    

#######################################################################################################################################    


def link_neurobat(df_long, DATA_DIR):
    """
    df_long - a main table with longitudinal examinations for all (selected) subjects.
    DATA_DIR - a global variable, with path to folder with al lcsv files.
    
    C: 2021.03.02 / M: 2021.03.15
    """
    neuro = pd.read_csv(DATA_DIR / 'NEUROBAT.csv', low_memory=False, index_col=0)
    neuro.reset_index(level=0, inplace=True)
    
    cols_neuro = ['RID', 'Phase', 'VISCODE2', 'TRAASCOR', 'TRABSCOR', 'CLOCKSCOR', 'COPYSCOR', 'CATANIMSC',  'ANARTERR', 'EXAMDATE', 'AVTOT6', 'AVDEL30MIN', 'AVDELTOT', 'AVTOTB']
    neuro_red = neuro[cols_neuro]
    
#     # rename columns (old_name : new_name)
#     neuro_red = neuro_red.rename({'RID':'RID_neuro',
#                                  'VISCODE2':'VISCODE2_neuro',
#                                  'EXAMDATE':'EXAMDATE_neuro',
#                                  'Phase':'Phase_neuro',
#                                  'TRAASCOR' : 'TRAASCOR_neuro',
#                                  'TRABSCOR' : 'TRABSCOR_neuro',
#                                  'CLOCKSCOR' : 'CLOCKSCOR_neuro',
#                                  'COPYSCOR' : 'COPYSCOR_neuro',
#                                  'CATANIMSC' : 'CATANIMSC_neuro',
#                                  'ANARTERR' : 'ANARTERR_neuro',
#                                  }, axis='columns')    
    #### VERSION1
    # long = pd.merge(long, neuro_red, how='left', left_on=['RID','VISCODE3_', 'EXAMDATE'], right_on=['RID', 'VISCODE2_neuro', 'EXAMDATE_neuro'], suffixes=['_Long', '_Neuro'], indicator='MERGE_long_neuro')
    # long.shape    
    
    # update columns name
    neuro_red.columns = [c+'_neuro' for c in list(neuro_red.columns)]
    
    ### VERSION 2
    new_neuro = df_long.merge(neuro_red, how='left', left_on=['RID','VISCODE3_'], right_on=['RID_neuro', 'VISCODE2_neuro'],
                         suffixes=['_X_neuro', '_Y_neuro'], indicator='MERGE_long_neuro')
    new_neuro.drop(columns=['RID_neuro'], inplace=True)
    
    #######################################
    #### REMOVING DUPLICATED ROWS !!!! ####
    #######################################
    ### OPTION 1 - REMOVE ALL DUPLICATES (12 ROWS)    
    
    df1 = new_neuro.Idx_.value_counts().rename_axis('Idx_').reset_index(name='counts')
    idx = df1.loc[df1.counts==2, 'Idx_']
    shortlong = new_neuro[~new_neuro.Idx_.isin(idx)].copy()

    ### OPTION 2 - REMOVE ONE DUPLICATE OUT OF 2 (6 OUT OF 12)
#     idx2rem = new_neuro[new_neuro.duplicated(['Idx_'])].index
#     shortlong = new_neuro[~new_neuro.index.isin(idx2rem)]
    
    colsN = [c for c in shortlong.columns if c.endswith('_neuro')]    
    for c in ['Phase_neuro', 'EXAMDATE_neuro','MERGE_long_neuro', 'VISCODE2_neuro']:
        if c in colsN:
            colsN.remove(c)
            
    # Replace all negative values (-1) with np.NaN       
    for c in colsN:
        shortlong.loc[shortlong[c] < 0, c] = np.NaN    
    
    return shortlong
#######################################################################################################################################


def link_adas(df_long, DATA_DIR):
    """
    df_long - a main table with longitudinal examinations for all (selected) subjects.
    DATA_DIR - a global variable, with path to folder with al lcsv files.
    
    C: 2021.03.02 / M: 2021.03.10
    """
    
    adas1_full = pd.read_csv( DATA_DIR / 'ADASSCORES.csv', low_memory=False)
    adas1_cols = ['RID', 'VISCODE', 'TOTALMOD','Q1','Q2','Q3','Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10', 'Q11', 'Q12', 'Q14']
    adas1 = adas1_full[adas1_cols]
    
    adas1 = adas1.rename({'VISCODE':'VISCODE3',
                          'TOTALMOD': 'TOTAL13',
                          'Q14':'Q13'}, axis='columns')
    
    
    adas23go_full = pd.read_csv( DATA_DIR / 'ADAS_ADNIGO23.csv', low_memory=False)
    adas23go_cols = ['RID', 'VISCODE2', 'TOTAL13', 'Q1SCORE','Q2SCORE','Q3SCORE','Q4SCORE', 'Q5SCORE',
                     'Q6SCORE', 'Q7SCORE', 'Q8SCORE', 'Q9SCORE', 'Q10SCORE', 'Q11SCORE', 'Q12SCORE', 'Q13SCORE']
    adas23go = adas23go_full[adas23go_cols]
    
    adas23go = adas23go.rename({'Q1SCORE':'Q1','Q2SCORE':'Q2','Q3SCORE':'Q3','Q4SCORE':'Q4'}, axis='columns')
    adas23go = adas23go.rename({'Q5SCORE':'Q5','Q6SCORE':'Q6','Q7SCORE':'Q7','Q8SCORE':'Q8'}, axis='columns')
    adas23go = adas23go.rename({'Q9SCORE':'Q9','Q10SCORE':'Q10','Q11SCORE':'Q11','Q12SCORE':'Q12'}, axis='columns')
    adas23go = adas23go.rename({'Q13SCORE':'Q13', 'VISCODE2':'VISCODE3'}, axis='columns')
    
    adas = pd.concat([adas1, adas23go])
    
    adas.columns = [c+'_adas' for c in list(adas.columns)]
    
    new_adas = pd.merge(df_long, adas, how='left', left_on=['RID','VISCODE3_'], right_on=['RID_adas', 'VISCODE3_adas'],
                        suffixes=['_X_adas', '_Y_adas'], indicator='MERGE_long_adas')
    
    new_adas.drop(columns=['RID_adas'], inplace=True)
    
    
    colsN = [c for c in new_adas.columns if c.endswith('_adas')]
    
    for c in ['MERGE_long_adas', 'VISCODE3_adas']:
        if c in colsN:
            colsN.remove(c)
            
    for c in colsN:
        new_adas.loc[new_adas[c] < 0, c] = np.NaN 
    
    return new_adas
#######################################################################################################################################

def link_gdscale(df_long, DATA_DIR):
    """
    df_long - a main table with longitudinal examinations for all (selected) subjects.
    DATA_DIR - a global variable, with path to folder with al lcsv files.
    
    C: 2021.03.15 / M: 2021.03.15
    """
    
    gdscale = pd.read_csv(DATA_DIR / 'GDSCALE.csv', low_memory=False, index_col=0)
    gdscale.reset_index(level=0, inplace=True)
    
    cols_gdscale = ['RID', 'Phase', 'VISCODE2', 'EXAMDATE', 'GDTOTAL']
    gdscale_red = gdscale[cols_gdscale]
    
    gdscale_red = gdscale_red.replace('sc', 'bl')
    
    # update columns name
    gdscale_red.columns = [c+'_gds' for c in list(gdscale_red.columns)]
    
    new_gdscale = df_long.merge(gdscale_red, how='left', left_on=['RID','VISCODE3_'], right_on=['RID_gds', 'VISCODE2_gds'],
                         suffixes=['_X_gds', '_Y_gds'], indicator='MERGE_long_gds')
    new_gdscale.drop(columns=['RID_gds'], inplace=True)
    
    new_gdscale.loc[new_gdscale.GDTOTAL_gds < 0, 'GDTOTAL_gds'] = np.NaN
    
    return new_gdscale
#######################################################################################################################################

def link_faq(df_long, DATA_DIR):
    """
    
    C: 2021.09.23 by AV
    U: 2021.10.04
    """
    
    faq = pd.read_csv(DATA_DIR / 'FAQ.csv', low_memory=False, index_col=0)
    faq.reset_index(level=0, inplace=True)
    
    cols_faq = ['RID', 'Phase', 'VISCODE2', 'EXAMDATE', 'FAQSOURCE', 'FAQFINAN', 'FAQFORM', 'FAQSHOP',
                'FAQGAME', 'FAQBEVG', 'FAQMEAL', 'FAQEVENT', 'FAQTV', 'FAQREM', 'FAQTRAVL', 'FAQTOTAL']
    faq_red = faq[cols_faq]
    
    faq_red = faq_red.replace('sc', 'bl')
    
    # update columns name
    faq_red.columns = [c+'_faq' for c in list(faq_red.columns)]
    
    new_faq = df_long.merge(faq_red, how='left', left_on=['RID','VISCODE3_'], right_on=['RID_faq', 'VISCODE2_faq'],
                         suffixes=['_X_faq', '_Y_faq'], indicator='MERGE_long_faq')
    
    return new_faq
#######################################################################################################################################

def link_freesurfer(df_long, DATA_DIR_FS, current_FS_result_file_name):
    """
    df_long - a main table with longitudinal examinations for all (selected) subjects.
    DATA_DIR_FS - a global variable, with path to folder with al csv FreeSurfer files.
    
    C: 2021.03.29 / M: 2021.04.16
    """

    fs_name = DATA_DIR_FS / current_FS_result_file_name
    fs = pd.read_csv(fs_name)

    # Renamse some column names
    fs = fs.rename({'subject': 'PTID', 'tp_imageuid': 'Imageuid_', 'cross_complete':'complete_cross', 'long_complete':'complete_long'}, axis='columns')

    # Select columns from a FreeSurfer table
    cols_fs = ['Imageuid_', 'PTID',
               'Left-Lateral-Ventricle_cross', 'Right-Lateral-Ventricle_cross',
               'Left-Lateral-Ventricle_long', 'Right-Lateral-Ventricle_long', 
               'Left-Hippocampus_cross', 'Right-Hippocampus_cross',
                'Left-Hippocampus_long', 'Right-Hippocampus_long',
               'eTIV_x_cross', 'eTIV_y_cross',
               'eTIV_x_long',  'eTIV_y_long',
               'complete_long', 'complete_cross']
    fs_red = fs[cols_fs]


    df =  pd.merge(df_long, fs_red, how='left', on=['Imageuid_', 'PTID'],indicator='MERGE_FS_' )
    return df
#######################################################################################################################################
