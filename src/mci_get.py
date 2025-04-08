"""
Auxiliary GET functions from MCI tables.

(C) MCI group.

Created: 2020.10.13
Updated: 2021.04.12
"""

import pandas as pd
   
def get_patient_lists_with_images(df):
    """
    Gets two patient lists with at leats one image, and without any image.
    
    C: 2020.10.16
    M: 2020.10.16
    """
    
    zeros = []
    notzeros = []

    # count patients with and without MR images
    if 'MRIs_Nr_' in df:
        for r in df.RID.unique():
            pat = get_value_from_column(df, 'RID', r)
            ims = pat.MRIs_Nr_.unique()
            if ims:
                notzeros.append(ims)
            else:
                zeros.append(ims)
    return zeros, notzeros
    
    
def get_value_from_column(df, column, value):
    """
    An universal function to get selected values from a column.
    
    Parameters:
    -----------
    df (pandas df): A table (data frame), e.g. adnimerge or merge.
    column (string): Name of column (e.g. 'PTID') to select a value (e.g. "011_S_00029")
        
    Returns:
    ---------
    df : All rows with velues in a column.
    
    Usage:
    ------
    df_patient = get_value_from_column(merge, column='PTID', value='941_S_1203') -> gets all rows with PTID='941_S_1203' from PTID column
    df_age = get_value_from_column(merge, column='AGE', value='83.3') -> gets all rows with AGE=83.3 from AGE column
    df_dx = get_value_from_column(merge, column='DX', value='CN') -> gets all rows with DX='CN' from DX column
    
    C: 2020.09.24
    U: 2020.09.25    
    """ 
    #return df[df.PTID.str.contains(ptid)]
    return df.loc[df[column] == value]


def get_paiteint_diagnosis(df, rid):
    """
    Get BL and all current diagnoses for RID
    
    Paremeters:
    -----------
    df - table,
    rid - Participant roster ID
    
    Returns
    -------
    diags (list) : list of tuples (Baseline diagnosis, Diagnosis, Original study protocol) for a given rid
    
    C: 2020
    M: 2020.09.25
    """
    diags = list(zip(df.loc[df.RID == rid].DX_bl.values, df.loc[df.RID == rid].DX.values, df.loc[df.RID == rid].PTID))
    return diags


def get_patient_diagonosis_sorted_by_date(df, rid):
    """
    Get BL and all current diagnoses for RID
    
    C: 2020
    M: 2020.09.25
    """
    #diags = list(zip(df.loc[df.RID == rid].DX_bl.values, df.loc[df.RID == rid].DX, df.loc[df.RID == rid].PTID, df.loc[df.RID == rid].EXAMDATE))
    dfn = df[df.RID == rid]
    dfn = dfn.sort_values(by=['EXAMDATE'])
    return dfn


def get_patient_list(df, name='A TABLE', sh=True):
    """
    Returns list of patients in a df based on unique values in a RID column.
    
    C: 2020.10.13
    M: 2020.10.13
    """
    rid_list = df.RID.unique()
    if sh:
        print(f'Number of patients in a {name.upper()} table: {len(rid_list)}\n')        
    return rid_list


def get_patient_with_more_equalled_k_visits(df, k=3):
    """
    Returns a df that contains patients with visit number equalled to or more than k (#visits>=k).
    
    Created: 2020.11.13 / Updated: 2020.11.13
    """
    return df.loc[df.Visits_Nr_ >= k]


def get_patient_with_more_equalled_n_months(df, n=12):
    """
    Get the df with patients those treatment lasts n months or longer.
    
    Created: 2020.11.13 / Upadted: 2020.11.13
    """    
    c = df.groupby('RID', as_index=False).nth(-1)
    d = c.loc[c.Month>=n]
    
    ### VERSION 1
#     vis12 = pd.DataFrame()
#     for r in d.RID.values:
#         pat = df.loc[df.RID == r]
#         vis12 = pd.concat([vis12, pat])
        
    ### VERSION 2 
    pts = d.RID.values.tolist()
    vis12 = df[df['RID'].isin(pts)]
    return vis12

def get_patient_nth_examination(df, nth=0):
    """
    Get the nth examination for each patient, where:
        - the first examination: nth = 0
        - the second examination: nth = 1
        - N examinatino: nth-1
        - the last examination: nth = -1
    
    
    Created: 2020.11.14 / Updated: 2020.11.14
    """
    table = df.groupby('RID', as_index=False).nth(nth)
    return table


def get_patient_bl(df):
    """
    Created: 2021.03.08 / Updated: 2021.03.08
    """    
    return df.loc[df.VISCODE3_ == 'bl']


def get_phase_info(df, feature='EXAMDATE', name='A table'):
    """
    Get phase and indices for each phase and the total indices in the df.
    
    
    USAGE:
    ---------------
    idx_dct = mget.get_phase_info(merge, 'EXAMDATE')
    for k,v in idx_dct.items():
    print(k,len(v), v[:4])
    merge.loc[idx_dct['ADNI2']]
    
    C: 2021.02.25 / U:2021.02.25
    """
    #check the column name with a ADNI phase
    if 'Phase' in df.columns:
        feat = 'Phase'
    elif 'COLPROT' in df.columns:
        feat = 'COLPROT'
    else:
        print("Can't get Phase from a dataframe")
        
    # Get all phases
    phases = df[feat].unique()
    print(f'{name} (rows:{df.shape[0]});\tSCORE: {feature} \n')
    
    idx_dct = {'all':df.index.values} 
    for ph in phases:
        # df with every phase
        cur_df = df[df[feat] == ph]
        tot = cur_df.shape[0]
        
        # count fearue numer in a phase
        if feature in cur_df.columns:            
            vals = cur_df[feature].notna().sum()
            s = f'; valid {vals}, ({vals*100/tot:.1f}%)'
        else:
            s=f",\tno '{feature}' in the df!"        
        print(f'\t{ph} ({tot}){s}')
        idx_dct[ph] = cur_df.index.values
    return idx_dct
    
    