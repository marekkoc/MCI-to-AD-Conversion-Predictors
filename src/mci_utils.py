"""
Auxiliary UTiLS functions to MCI tables.

(C) MCI group.

Created: 2021.03.30
Updated: 2021.10.06
"""

def package_versions(installedOnly=False, theMostImportant=[]):
    """
    Created on Wed Nov  1 13:00:07 2017
    @author: Marek

    based on: mk_package_info.py

    USAGE:
        installedOnly = True / False - if True ommits not installed package
        mostImportant = ['numpy', 'scipy', 'seaborn'] - list of interested packages only


    C: 2017.11.01
    M: 2021.03.30
    """
    import sys
    import importlib
    import platform as pl

    print("\n")
    print("Computer name: {}".format(pl.node()))
    print("Operating system: {}, {}".format(pl.system(), pl.architecture()[0]))

    print(f"\nPython path: {sys.executable}")
    print ("Python version: {}\n".format(sys.version))    


    not_installed_info = ''
    pkgs_lst = []
    vers_lst = []
    mk_packages = ['numpy', 'scipy', 'pandas', 'seaborn', 'matplotlib', 'sklearn', 'skimage', 'OpenGL', 'nibabel', 'dicom', 
                  'PyInstaller', 'PIL', 'imageio', 'cython', 'csv', 'json', 'statsmodels', 'ipywidgets', 'eli5', 'pdpbox', 'joblib', 'networkx']

    for p in mk_packages:
        try:
            module = importlib.import_module(p, package=None)
            #print(f'{p}: {module.__version__}')
            ver = module.__version__
        except:
            #print(f'{p} {not_installed_info}')
            ver = not_installed_info
        pkgs_lst.append(p)
        vers_lst.append(ver)        
    #############################      
    try:
        import tkinter
        ver = tkinter.TkVersion
    except ImportError:
        ver = not_installed_info
    pkgs_lst.append('tkinter')
    vers_lst.append(ver)
    #############################
    try:
        import PyQt5
        from PyQt5 import QtCore
        ver = QtCore.QT_VERSION_STR
    except ImportError:
        ver = not_installed_info
    pkgs_lst.append('PyQt5')
    vers_lst.append(ver)
    #############################
    try:
        import vtk
        ver = vtk.vtkVersion.GetVTKSourceVersion()
    except ImportError:
        ver = not_installed_info
    pkgs_lst.append('vtk')
    vers_lst.append(ver)
    #############################
    try:
        import itk
        ver = itk.Version.GetITKSourceVersion()
    except ImportError:
        ver = not_installed_info
    pkgs_lst.append('itk')
    vers_lst.append(ver)
    #############################
    
    
    try:
        import pandas as pd
        df = pd.DataFrame.from_dict({'module':pkgs_lst, 'version':vers_lst})
        df['module2'] = df['module'].str.lower()
        df.sort_values(by=['module2'], inplace=True)
        df.index=range(1, len(df)+1)
        df = df[['module', 'version']]

        if installedOnly:
            df = df.loc[df.version != not_installed_info]

        if len(theMostImportant):
            df = df.loc[df.module.isin(theMostImportant)]
        return df
    except ImportError:
        return print(zip(pkgs_lst, vers_lst))
    
    
def textWrap(text):
    """
    C: 2019.06.18
    M: 2021.04.04
    """
    print()
    p = len(text) + 8
    print(p * '#')
    print("### %s ###" % text)
    print(p * '#')

    
def rename_columns(df, dc_names, verbose=True):
    """
    Rename column names in a df. Function returns a COPY of original df with a new column names.
    
    Parameters:
    --------------------------
    df - a df to change column names,
    dc_names - dictionary with old names (as keys) and new names (as values),
    verbose - prints out old and new column names.
    
    
    Usage:
    --------------------------
    dct_names = {'AGE': 'age', 'FAQ': 'faq'}
    bl = rename_columns(bl, dc_names=dct_names)
        
    C: 2021.07.30 / U: 2021.07.30
    """
    
    keys_new = dc_names.keys()
    keys_old = df.columns
    
    for k in keys_new:        
        if k not in keys_old:
            print(f'Wrong column name: {k}')
    print()
            
            
    if verbose: print(f'OLD names:\n{df.columns}\n')
    df_new = df.rename(columns=dc_names)    
    if verbose: print(f'NEW names:\n{df_new.columns}\n')
    
    return df_new

def load_train_val_cv_splits_from_file(kfolds_file, CV):
    """
    Gets test/split indices from saved csv file for different fold number (k={10,20,50,...}). This is to have the same subject split
    betwenn `bl` and `long` experiments.
    
    
    Parameters:
    -----------------------------
    kfold.csv - path to file with splits (defaut is: results/20201110/kfolds.csv)
    CV: split number, part of column name, eg: CV=10 (or 20,50,...)
    
    Returns:
    ----------------------------
    SPLITS: a list of tuples with train and val indices ( (train0, val0), (train1, val1), (train2, val2), ....)
    
    
    C: 2021.10.06 / U:2021.10.06
    """
    import numpy as np
    import pandas as pd
    
    df = pd.read_csv(kfolds_file, index_col=0)

    # get columns with specified folds number e.g. K=10
    col_names = [c for c in df.columns if f'_CV{CV}_' in c]

    # REF. TO SCRIPT 3.01
    SPLITS = []

    for col in df[col_names]:
        # to sa odczyatane indeksy
        #train_index = df.loc[df[col] == 'train'].index
        #validation_index = df.loc[df[col] == 'val'].index

        # to sa indeksy/numery wierszy (0,1,..) indeksow pacjentow (13, 26,...) w df X_train
        # https://stackoverflow.com/questions/28837633/pandas-get-position-of-a-given-index-in-dataframe
        validation_index_index = df.index.get_indexer_for((df[df[col] == 'val'].index))
        train_index_index = df.index.get_indexer_for((df[df[col] == 'train'].index))

        SPLITS.append([np.array(train_index_index), np.array(validation_index_index)])        
    #print(df.loc[validation_index, col])    
    return SPLITS
