"""
Auxiliary PREPROCESSING functions on MCI tables.

(C) MCI group.

Created: 2020.11.13
Updated: 2021.03.08
"""
import numpy as np
import mci_get as mget


def count_score_nr_for_patient(df, score_name, score_nr_name,  df_name='A TABLE', sh=True):
    """
    Counts number of avaliable score for each patient, and assaign this value to a new df column .
    
    
    ### Jupyter cell usage example:
    k = 8
    display(mci_all_columns.loc[mci_all_columns.RID == k, 'IMAGEUID'])
    print(mci_all_columns.loc[mci_all_columns.RID == k, 'IMAGEUID'].count())
    
    Created: 2021.03.08 / Updated: 2021.03.08
    """        
    for r in df.RID.unique(): 
        #pat_df = mget.get_value_from_column(df, 'RID', r)
        pat_df = df.loc[df.RID == r]
        df.loc[df.RID == r, score_nr_name] = pat_df[score_name].count()    
    # convertion from float to integer
    df[score_nr_name] = df[score_nr_name].astype(int)
    if sh:
        print(f'A new column "{score_nr_name}" is added to "{df_name}" table.')
    return df



def count_MR_images_for_patient(df, name='A TABLE', sh=True):
    """
    Counts number of avaliable MR images for each patient, and assaign this value to a new df column 'MRIs'.
    
    
    ### Jupyter cell usage example:
    k = 8
    display(mci_all_columns.loc[mci_all_columns.RID == k, 'IMAGEUID'])
    print(mci_all_columns.loc[mci_all_columns.RID == k, 'IMAGEUID'].count())
    
    Created: 2020.11.13 / Updated: 2021.03.08
    """        
    for r in df.RID.unique(): 
        pat_df = mget.get_value_from_column(df, 'RID', r)
        df.loc[df.RID == r, 'MRIs_Nr_'] = pat_df.IMAGEUID.count()
    # convertion from float to integer
    df['MRIs_Nr_'] = df.MRIs_Nr_.astype(int)
    if sh:
        print(f'A new column "MRIs_Nr_" is added to "{name}" table.')
    return df


def count_visits_for_patient(df, name='A TABLE', sh=True):
    """
    Counts number of visitst for each patient, assigns this value to a new df column 'Visits'
    
    Created: 2020.11.13 / Upadated: 2021.03.08
    """

    for r in df.RID.unique():
        pat_df = mget.get_value_from_column(df, 'RID', r)
        df.loc[df.RID == r, 'Visits_Nr_'] = pat_df.shape[0]
    # convertion from float to integer
    df['Visits_Nr_'] = df.Visits_Nr_.astype(int)
    if sh:
        print(f'A new column "Visits_Nr_" is added to "{name}" table.')
    return df


def count_sMCI_cAD(df):
    """
    Retrurnd a new table that contains ONLY sMCI and cAD patients. 
    
    Created 2020.11.14 / Updated 2020.11.14
    """
    df = df.sort_values(by=['RID', 'EXAMDATE'])

    df_nan = df.dropna(subset = ["DX"])
    for r in df_nan.RID.unique():
        pat = df_nan.loc[df_nan.RID == r]
        #pat1 = df.loc[df.RID == r]        

        # get sMCI (all MCI)
        mci = np.all(pat.DX == 'MCI')
        if mci:
            df.loc[df.RID == r, 'Subgroup_'] = 'sMCI'

        # cAD - get first MCI and have at least one hit of Dementia
        v = pat.DX.values
        first = v[0]
        mci = pat.DX == 'MCI'   

        if first == 'MCI' and not np.all(mci):
            ad = pat.DX == 'Dementia'
            if np.all(mci | ad):
                df.loc[df.RID == r, 'Subgroup_'] = 'cAD'

    return df.loc[df['Subgroup_'].isin(['sMCI', 'cAD'])]


def reorder_columns(df_long, verbose=False):
    """
    Reoreder columnn; group columns from the same type (table).
    
    C: 2021.03.30 / U: 2021.03.30
    """
    cols1 = df_long.columns.to_list()
    cols11 = cols1.copy()
    len1 = len(cols1)
    
    adas_lst = sorted([c for c in df_long.columns if c.endswith('_adas')])
    neuro_lst = sorted([c for c in df_long.columns if c.endswith('_neuro')])
    gds_lst = sorted([c for c in df_long.columns if c.endswith('_gds')])     
    long_lst = sorted([c for c in df_long.columns if c.endswith('_long')]) 
    cross_lst = sorted([c for c in df_long.columns if c.endswith('_cross')]) 
    ours_lst = sorted([c for c in df_long.columns if c.endswith('_')])

    adni_lst = sorted(list(set(list(df_long.columns)).difference(set(adas_lst), set(neuro_lst), set(gds_lst), 
                                                            set(long_lst), set(cross_lst), set(ours_lst))))
    # ADNI columns
    # select some columns to the beginning of a new list
    adni_lst_new = []
    for f in ['RID', 'PTID','PTGENDER', 'PTEDUCAT', 'EXAMDATE', 'AGE', 'Years_bl', 'Month', 'Month_bl', 'DX', 'DX_bl',
             'ORIGPROT', 'Phase', 'IMAGEUID']:
        adni_lst_new.append(adni_lst.pop(adni_lst.index(f)))
    # add not selected columns after sorting them
    adni_lst_new = adni_lst_new + sorted(adni_lst)

    # new column order list
    new_column_order = adni_lst_new + adas_lst + neuro_lst + gds_lst + long_lst + cross_lst + ours_lst
    df_new = df_long.reindex(columns=new_column_order)
    
    
    if verbose:
        cols2 = new_column_order.copy()
        len2 = len(cols2)

        for c in cols1:
            if c in cols2:
                cols2.remove(c)
                cols11.remove(c)
        if len(cols2) == len(cols11):
            print(f'Columns in and out are the same!')                
        print(f'Columns in {len1}, out {len2}')
        
    return df_new


def coding_(x):
    if x <= 1: x=0
    elif x <= 3: x = 1
    elif x == 4: x = 2
    elif x >= 5: x = 3
    return x


def faq_pos_neg_classification(df_long):
    """
    Classification of FAQ values to POSITIVE or NEGATIVE states. 
    
    C: 2021.09.26 / U:2021.10.21
    """
    faq_cols = [c for c in df_long.columns if '_faq' in c]
    faq_cols.remove('EXAMDATE_faq')
    faq_cols.remove('FAQSOURCE_faq')
    faq_cols.remove('FAQTOTAL_faq')
    faq_cols.remove('MERGE_long_faq')
    faq_cols.remove('Phase_faq')
    faq_cols.remove('RID_faq')
    faq_cols.remove('VISCODE2_faq')
    
    # the table with selected '_faq' columns
    faq1 = df_long[faq_cols].copy()    
    
    # fill in the main table (df_long) with coded FAQ values 
    for col in faq_cols:
        new_col = col + '_cod_'
        
        df_long[new_col] = faq1[col].apply(coding_)
        df_long[new_col] = df_long[new_col].fillna(-1).astype(int)
        print(f'A new column "{new_col}" is added to "long" table.')
        
    # select columns with newly coded features '_faq_cod_'
    cod_cols = [c for c in df_long.columns if '_faq_cod_' in c]
    
    # the table with selected and coded '_faq_cod_' columns
    faq2 = df_long[cod_cols].copy() 

    cnt = faq2[faq2 >= 3].count(axis=1)
        
    #faq2['Faq_cnts_'] = cnt
    # positive -> 'P', negatiove -> 'N'
    #faq2['Faq_dsc_'] = np.where(cnt >=3 , 'P', 'N')
    
    df_long['Faq_cnts_'] = cnt
    print('A new column "Faq_cnts_" is added to "long" table.')    
    # positive -> 'P', negatiove -> 'N'
    df_long['Faq_dsc_'] = np.where(cnt >=3 , 'P', 'N')
    print('A new column "Faq_dsc_" is added to "long" table.')
    
    return df_long