"""
Auxiliary INFO functions about MCI tables.

(C) MCI group.

Created: 2020.11.13
Updated: 2021.10.04
"""

import ipywidgets as widgets
from IPython.display import display

import random
import numpy as np
import pandas as pd
import mci_get as mget


def listdir(path, howmany='all'):
    if howmany == 'all':
        return sorted(list(path.iterdir()))
    else:
        return sorted(list(path.iterdir())[:howmany])
    

def df_info(df, k=3, name='data frame'):
    """
    Print table inforamtion and display k first rows.
    
    If k<0 dispaly a full table.
    If k==0 print only table information.
    If k>0 print k first rows (similar to head(k) function)
    
    Parameters
    -----------
    df - a data frame with MCI columns,
    k - number of column to print,
    name - data frame name to print in a description.
    
    
    Returns
    -------
    print info
    
    C: 2020.10.10
    U: 2020.11.12
    """
    zeros,  notzeros = mget.get_patient_lists_with_images(df)
            
    s = ''
    s += (f'{name.upper()}:')
    s += (f'\n\tRows(exams): {df.shape[0]},')
    s += (f'\n\tColumns (features): {df.shape[1]},')
    s += (f'\n\tPatients number (unique RID): {len(df.RID.unique())},')
    if 'IMAGEUID' in df.columns:
        s += (f'\n\t\tPatients with at least one MRI image (MRIs): {len(notzeros)},')
        s += (f'\n\t\tPatients without any MRI image (MRIs): {len(zeros)},')
        s += (f'\n\tMRI images (IMAGEUID): {df.IMAGEUID.count()}.\n')
        
    print(s)
    print()
    if k<0:
        return df.iloc[:]
    elif k==0:
        return None
    else:
        return df.head(k)
    
def df_info2(df_lst, df_names, sh=True):
    """
    Prints difference info about two tables.
    C: 2020.10.16
    M: 2021.02.26
    """
    
    df_lst = df_lst if isinstance(df_lst, list) else [df_lst]
    df_names = df_names if isinstance(df_names, list) else [df_names]
    
    data = {}
    for k, df in enumerate(df_lst):
        lst = []
        lst.append(df.shape[0]) # rows
        lst.append(df.shape[1]) # cols
        lst.append(len(df.RID.unique())) # patients        
        zeros, notzeros = mget.get_patient_lists_with_images(df)
        
        notzeros_count = len(notzeros) if len(notzeros)  else 0
        zeros_count = len(zeros) if len(zeros) else 0
        lst.append(notzeros_count)
        lst.append(zeros_count)   
        if 'IMAGEUID' in df.columns:
            lst.append(df.IMAGEUID.count()) # nr of images
        else:
            lst.append(0)
            
        key = df_names[k]
        data[key] = lst
        if sh:
            print(f'{key}... done')
    
    print('\n')
    index1 = ['Rows (exams)', 'Cols. (features)', 'All patientes (unique RID)']
    index2 = ['Patients with at least one MR img (MRIs)','Patients without MR imags (MRIs)', 'MRI images (IMAGEUID)']
    index = index1 + index2
    
    df = pd.DataFrame.from_dict(data)     
    df.columns = df_names
    df.index = index
    
#     # https://stackoverflow.com/questions/61359214/how-to-center-align-headers-and-values-in-a-dataframe-and-how-to-drop-the-index
#     df1 = df.style.set_table_styles([dict(selector='th', props=[('text-align', 'center')])])
#     df1.set_properties(**{'text-align': 'center'}).hide_index()
#     print(f'\n')
    display(df)
    

def compare_dfs(df1, df2, df1_name='df1', df2_name='df2'):
    """
    Prints difference info about two tables.
    
    C: 2020.10.15
    M: 2020.10.15
    """
    r1, c1 = df1.shape
    r2, c2 = df2.shape
    p1, p2 = len(df1.RID.unique()), len(df2.RID.unique())
    i1, i2 = df1.IMAGEUID.count(), df2.IMAGEUID.count()
     
    data = {'df1':[r1, c1, p1, i1], 'df2':[r2, c2, p2, i2], 'diff':[r1-r2, c1-c2, p1-p2, i1-i2]} 
    index=['Rows (exams)', 'Cols. (features)', 'Patientes (unique RID)', 'MRI images (IMAGEUID)']
    df = pd.DataFrame.from_dict(data) 
    
    df.columns = [df1_name, df2_name, 'difference']
    df.index = index
    
    print(f'Difference between two tables: {df1_name.upper()} and {df2_name.upper()}\n')
    display(df)
    
    
def iterate_patient_GUI(df, column='RID', name='data frame', rid=None, sh=False):
    """
    
    Iterate over patients.
    
    parameters
    ========================
    df - a dataframe to iterate by
    column - a column to iterate on,
    
    
    C: 2020.10.11
    M: 2021.03.23
    """     
    global k, df1    
    subjects = df[column].unique()
    
    if rid in subjects:
        k = np.where(subjects==rid)[0][0]  
    else:
        k = 0
    df11 = df.loc[df[column] == subjects[k]]   
#     # https://stackoverflow.com/questions/61359214/how-to-center-align-headers-and-values-in-a-dataframe-and-how-to-drop-the-index
    df1 = df11.style.set_table_styles([dict(selector='th', props=[('text-align', 'center')])])
    df1.set_properties(**{'text-align': 'center'}).hide_index()

    
    right = widgets.Button(description='Next',button_style='', tooltip='Click me', icon='hand-o-right')
    rand =  widgets.Button(description='Random',disabled=False,button_style='',tooltip='Random subject',icon='random')
    left =  widgets.Button(description='Prev.',disabled=False,button_style='',tooltip='Click me',icon='hand-o-left')
    reset = widgets.Button(description='Reset',disabled=False,button_style='',tooltip='Reset subject',icon='eraser')
    hide = widgets.Button(description='Hide',disabled=False,button_style='',tooltip='Reset subject',icon='eye-slash')
    output = widgets.Output(overflow_x='auto')
    with output:
        display(df1) 

    
    def on_button_clicked(but):
        global k
        output.clear_output()            
            
        if but.description == 'Next':
            k += 1            
        if but.description == 'Prev.':
            k -= 1            
        if but.description == 'Random':
            k = random.choice(range(len(subjects)))
            print(k)
        if but.description == 'Reset':
            k = 0
        if but.description == 'Hide':
            output.hide()
            
        k %= len(subjects)
        df11 = df.loc[df[column] == subjects[k]] 
        df1 = df11.style.set_table_styles([dict(selector='th', props=[('text-align', 'center')])])
        df1.set_properties(**{'text-align': 'center'}).hide_index()
        with output:
            display(df1)
    
    buttons = [right, left, rand, reset, hide]
    [b.on_click(on_button_clicked) for b in buttons]
   
    if sh:
        df_info(df, -1, name)
    
#     hbox = widgets.HBox([widgets.HBox([left, rand, right, reset, hide])])
    hbox = widgets.HBox([left, rand, right, reset, hide])    
    display(widgets.VBox([hbox, output]))
    
    
def included_feature_info(df, pattern='adni-adas-neuro-gds-faq-long-cross-_'):
    """
    Create a df with names types (e.g. _adas, _neuro, _) present in df's columns. It serves to check the curret content of tables in terms of included features.
    
    pattern: feature names with dash among them.
    
    
    Included patterns:
    - adni,
    - adas,
    - neuro,
    - gds,
    - faq,
    - long,
    - cross,
    - ours.
    
    
    The last update: Listing of 'faq' features.    
    C: 2021.03.10 / U: 2021.10.04
    """
    
    adas_lst = sorted([c for c in df.columns if c.endswith('_adas')])
    neuro_lst = sorted([c for c in df.columns if c.endswith('_neuro')])
    gds_lst = sorted([c for c in df.columns if c.endswith('_gds')])         
    faq_lst = sorted([c for c in df.columns if c.endswith('_faq')])     
    long_lst = sorted([c for c in df.columns if c.endswith('_long')]) 
    cross_lst = sorted([c for c in df.columns if c.endswith('_cross')]) 
    ours_lst = sorted([c for c in df.columns if c.endswith('_')])
    
    adni_lst = sorted(list(set(list(df.columns)).difference(set(adas_lst), set(neuro_lst), set(gds_lst), set(faq_lst), 
                                                            set(long_lst), set(cross_lst), set(ours_lst))))

    
    dct = {}
    if 'adni' in pattern:
        dct[f'adni (#{len(adni_lst)})'] = adni_lst  
    if 'adas' in pattern:
        dct[f'adas (#{len(adas_lst)})'] = adas_lst       
    if 'neuro' in pattern:
        dct[f'neuro (#{len(neuro_lst)})'] = neuro_lst
    if 'gds' in pattern:
        dct[f'gds (#{len(gds_lst)})'] = gds_lst            
    if 'faq' in pattern:
        dct[f'faq (#{len(faq_lst)})'] = faq_lst         
    if 'long' in pattern:
        dct[f'long (#{len(long_lst)})'] = long_lst
    if 'cross' in pattern:
        dct[f'cross (#{len(cross_lst)})'] = cross_lst
    if '_' in pattern:
        dct[f'ours (#{len(ours_lst)})'] = ours_lst
        
    df1 = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in dct.items() ]))
    df1.replace(np.NaN, '', inplace=True)
    print(f'Total number of columns: {len(df.columns)}\n')
    return df1


def df_stats_info(df, precision=3):
    """
    Basic df statistics for float and int column values.
    
    val_range = 
    
    C: 2021.03.11 / U: 2021.03.12
    """
    df = df.select_dtypes(include=['float', 'int'])
    #df.drop(columns=['RID'], inplace=True)

    index_names = []
    dct = {}

    col_names = ['max.', 'mean', 'min.', 'std', 'val_range', 'NaN_Nr']
    for c in df.columns:
        index_names.append(c)
        a  = df[c].values
        ptp = a[~np.isnan(a)].ptp()
        dct[c] = [df[c].max(), df[c].mean(), df[c].min(), df[c].std(), ptp, df[c].isna().sum()]


    res = pd.DataFrame(dct, index=col_names).T.round(precision)
    res['NaN_Nr'] = res['NaN_Nr'].astype(int)

    if 'RID' in res.columns: 
        res['RID'] = res['RID'].astype(int)
    return res

def df_stats_info2(df, precision=3):
    """    
    
    C: 2021.03.22 / U: 2021.03.22
    """
    return pd.DataFrame.from_dict({'min':df.min(), 'mean':df.mean(), 'max':df.max()}).round(precision)


def feature_split_info(df, feature_name='Subgroup_', display_type='#%', col_name='COL'):
    """
    Function counts absolute and/or percentage values (by value_counts() function) in each feature category (determined by feature_name). 
    
    display_type = '#' / '%' / '#%'
    
    C: 2021.03.15 / M: 2021.03.17
    """
    df1 = df[feature_name].value_counts().rename_axis(feature_name).reset_index(name=f'# {col_name}')
    df2 = df[feature_name].value_counts(normalize=True).rename_axis(feature_name).reset_index(name=f'% {col_name}')
    
    if display_type == '#':
        return df1
    elif display_type == '%':
        return df2
    elif '#' in display_type and '%' in display_type:
        df = pd.merge(df1, df2, how='left', on=feature_name)
        return df.sort_values(by=feature_name)
    else:
        print('Wrong type!')
        return pd.DataFrame()