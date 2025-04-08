"""
Auxiliary PLOT functions for MCI tables.

(C) MCI group.

Created: 2020.10.15
Updated: 2021.03.04
"""
import numpy as np
import pandas as pd
import seaborn as sns
from pathlib import Path
import matplotlib.pyplot as plt

def plot_violin_box_feature_vs_subgroup(df, feature_name='AGE', **kw):
    """
    Plots violin and box plot figures of feature vs. Subgroup
    
    Changes: Additional parameter: title, by deafault figure title was assumed as feature name.
            There is possibility to set any title.
            
    
    Parameters:
    -------------
    df - data frame, a table to take features from (a pandas dataframe),
    feature_name - name of a feature to plot (a string, default: 'AGE')
    
    Optional:
    ----------
    title - a figure title (a string, dafault: feature_name vs. Subgroup)
    points - weather or not to plot jitter dots (a boolean value, default:True)
    figsize - figure size (a tuple with size, deafault: (16,8))
    
    
    x_label - x axis label (a string, default: 'Subgroup')
    x_label_size - x label font size (an inteager, default: 28)
    x_label_labelpad - x label distance from axis (an inteager, default:20)
    
    y_label - y axis label (a string, default: feature_name)
    y_label_size - y label font size (an inteager, default: 28)
    y_label_labelpad - y label distance from axis (an inteager, default:20)
    
    grid_on - turn on/off a grid (a boolean value, default: True)
    
    subplot_adj - adjust subplot spaces (a list with float numbers).
                Usage:  (left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.2,  hspace=0.35)
                Parameters:
                - sub_left
                - sub_bottom
                - sub_right
                - sub_top
                - sub_wspace
                - sub_hspace
                
    
    Created 2020.11.15 / Updated 2021.03.04
    """    
    title = kw.get('title', f'{feature_name} vs. Subgroup')
    points = kw.get('points', True)
    figsize = kw.get('figsize', (16,8))
    
    x_label = kw.get('x_label', 'Subgroup')
    x_label_size = kw.get('x_label_size', 28)
    x_label_labelpad = kw.get('x_label_labelpad', 10)
    
    y_label = kw.get('y_label', feature_name)
    y_label_size = kw.get('y_label_size', 28)
    y_label_labelpad = kw.get('y_label_labelpad', 10)
    
    # (left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.2,  hspace=0.35)
    sub_left = kw.get('sub_left', 0.05)
    sub_bottom = kw.get('sub_bottom', 0.05)
    sub_right = kw.get('sub_right', 0.95)
    sub_top = kw.get('sub_top', 0.9)
    sub_wspace = kw.get('sub_wspace', 0.05)
    sub_hspace = kw.get('sub_hspace', 0.05)
    
    figSaveName = kw.get('figSaveName', '')
    
    
    grid_on = kw.get('grid', True)
        
    
    #title = title if title else f'{feature_name} vs. Subgroup'
    violin, ax = plt.subplots(1,2, figsize=figsize, sharex=True, sharey=True)
    
    _ = plt.suptitle(title, fontsize=26, weight='bold')
    
    _ = sns.violinplot(x='Subgroup_', y=feature_name, hue='PTGENDER', data=df, split=True, ax=ax[0])
    if points:
        _ = sns.stripplot(x="Subgroup_", y=feature_name, hue='PTGENDER', data=df, dodge=True, palette='dark',ax=ax[0])
        
    _ = sns.boxplot(x='Subgroup_', y=feature_name, hue='PTGENDER', data=df,  ax=ax[1])
    

    for a in ax:
        a.set_xlabel(x_label, fontsize=x_label_size, weight='bold', labelpad=x_label_labelpad)
        a.set_ylabel(y_label, fontsize=y_label_size, weight='bold', labelpad=y_label_labelpad)
        
        a.tick_params(axis='both', which='major', labelsize=20)
        a.tick_params(axis='both', which='minor', labelsize=20)
        
        handles, labels = a.get_legend_handles_labels()
        a.legend(handles[0:2], labels[0:2],loc=8, prop={'size': 16})        
        a.grid(grid_on)    
        
    ax[1].set(ylabel=None)
    
    plt.subplots_adjust(sub_left, sub_bottom, sub_right, sub_top, sub_wspace, sub_hspace)
    if len(figSaveName):
        if not figSaveName.endswith('.png'): 
            figSaveName += '.png'
        
        p = Path('./figs')        
        if not p.exists():
            p.mkdir(parents=True, exist_ok=True)
            print(f'Created "figs" folder!!!!')
        
        pth = p / figSaveName
        if pth.exists():
            print(f'Overwrite the file: {pth}')
        plt.savefig(pth)
        print(f'Figure saved to:\t{pth}')
        
        

def plot_2_tables_box_feature_vs_subgroup(df1, df2, title=['first', 'last'],feature_name='AGE', figsize=(16,8), points=True):
    """
    Plots two box plot figures of feature vs. Subgroup of two tables.
    
    Created 2020.11.16 / Updated 2020.11.16
    """

    violin, ax = plt.subplots(1,2, figsize=figsize, sharex=True, sharey=True)
    _ = plt.suptitle(f'{feature_name} vs. Subgroup', fontsize=26, weight='bold')
    
    
    _ = sns.boxplot(x='Subgroup_', y=feature_name, hue='PTGENDER', data=df1,  ax=ax[0])
    _ = sns.boxplot(x='Subgroup_', y=feature_name, hue='PTGENDER', data=df2,  ax=ax[1])

    for k, a in enumerate(ax):
        a.set_xlabel('Subgroup_', fontsize=28, weight='bold', labelpad=20)
        a.set_ylabel(feature_name, fontsize=22, weight='bold', labelpad=20)
        a.set_title(title[k], fontsize=22, weight='bold')
        
        a.tick_params(axis='both', which='major', labelsize=20)
        a.tick_params(axis='both', which='minor', labelsize=20)
        
        handles, labels = a.get_legend_handles_labels()
        a.legend(handles[0:2], labels[0:2],loc=8, prop={'size': 16})
        
        a.grid(True)
    
       
def _plot_many_lines(ax, df, feature, color):
    """
    Plots a selected feature for each subject with specified color. Usually df is either sMCI or cAD df.
    Plots function in their real floating-point positions.
    
    Function set:1     
    C: 2020.11.19 / U:2020.11.19
    """
    for rid in df.RID.unique():
        # get a patient
        pat = df[df.RID==rid]
        # get a features
        y = pat[feature].values

        # age axis
        t = pat.AGE.values[0] + pat.Years_bl.values
        # mask of not NaN values        
        y_double = y.astype(np.double)
        y_mask = np.isfinite(y_double)

        p = ax.plot(t[y_mask], y[y_mask], 'o-', c=color, markersize=4)
        #color = p[0].get_color()
    
    #p[0].set_label(label)
    #plt.legend(fontsize=22)
    return p

    
def _plot_mean_over_time(ax, df1, feature, color):
    """
    Plots a selected feature mean over time.
    
    A mean plot is calculated in rounded time points pecified by round()
    function with a given precision. Thus most of ploted points are rounded
    in e.g int age values (e.g. 79) instead of their real floating-point positions.
    
    Returns mean value over all timepoints.
    
    Function set: 2
    C: 2020.11.23 / Updated 2020.11.23
    """
    
    df = df1.copy()
    
    df['AGE2'] = df['AGE'] + df['Years_bl']
    df['AGE2'] = df.AGE2.round(0)

    piv = df.pivot_table(index='RID', columns='AGE2', values=feature)

    val = piv.values
    val_d = val.astype(np.double)
#    val_mask = np.isfinite(val_d)
    t = piv.columns.values
        
    v_mean = np.nanmean(val_d, axis=0)
    v_mean_mask = np.isfinite(v_mean)
    ax.plot(t[v_mean_mask], v_mean[v_mean_mask], linewidth=10, c=color)
    return v_mean.mean()

        
        
def time_plot(df1, feature, **kw):
    """
    A framework to plot a feature for all subjects.
    
    Parameters:
    -------------
    df1 - data frame, a table to take features from (a pandas dataframe),
    feature - name of a feature to plot (a string, default: 'AGE')
    
    Optional:
    ----------
    mean - weather or not to plot mean value lines (a boolean valueg, dafault: False)
    regress - weather or not to regresion value lines (a boolean value, default:False)
    figsize - figure size (a tuple with size, deafault: (16,8))
    
    title - figure title (a string, default: feature_name with some info if needed)
    title_font_size - a figure title font size (an inteager, default: 28)
    title_font_weight - a figure title fone weight(a strind, default: 'bold')
    
    x_label - x axis label (a string, default: 'AGE')
    x_label_size - x label font size (an inteager, default: 28)
    x_label_labelpad - x label distance from axis (an inteager, default:20)
    
    y_label - y axis label (a string, default: feature_name)
    y_label_size - y label font size (an inteager, default: 28)4
    y_label_labelpad - y label distance from axis (an inteager, default:20)
    
    grid_on - turn on/off a grid (a boolean value, default: True) 
    
    Function set: 2
    C: 2020.11.20 / Updated 2020.12.01
    """
    
    feature_name = feature # left for previous version compati
    
    mean = kw.get('mean', False)
    regress = kw.get('regress', False)
    figsize = kw.get('figsize', (25,10))
    
    title = kw.get('title', feature_name)
    title_font_size = kw.get('title_font_size', 28)
    title_font_weight = kw.get('title_font_weight', 'bold')
    
    x_label = kw.get('x_label', 'AGE')
    x_label_size = kw.get('x_label_size', 28)
    x_label_labelpad = kw.get('x_label_labelpad', 20)
    
    y_label = kw.get('y_label', feature_name)
    y_label_size = kw.get('y_label_size', 28)
    y_label_labelpad = kw.get('y_label_labelpad', 20)
    
    grid_on = kw.get('grid_on', True)
    
    
    df = df1.copy()
    smci = df.loc[df.Subgroup_ == 'sMCI']
    cad = df.loc[df.Subgroup_ == 'cAD']
        
#     if regress:
#         #plt.figure(figsize=(25,10), dpi=100)
#         lm = sns.lmplot(x="AGE", y="RAVLT_immediate", hue="Subgroup_", data=df, scatter=False,
#                        markers=["o", "x"],line_kws={'linewidth':8}, height=7, aspect=2.3);
#         ax = lm.axes[0,0]
#     else:
#         f, ax = plt.subplots(figsize=(25,10), dpi=100)

    f, ax = plt.subplots(figsize=figsize, dpi=100)
    p1 = _plot_many_lines(ax, smci, feature_name, 'red')     
    if mean:
        mn1 =_plot_mean_over_time(ax, smci, feature_name, 'maroon' )
        p1[0].set_label(f'sMCI (mv={mn1:.1f})')
        title = f'{feature_name} and subgroup means over time'
    elif regress:
        sns.regplot(x="AGE", y=feature_name, data=smci, scatter=False,
                    line_kws={"color": 'maroon',"linewidth": 10}, ax=ax);
        p1[0].set_label(f'sMCI')
        title = f'{feature_name} and regression lines'
    else:
        p1[0].set_label(f'sMCI')
        #label = f'{feature_name}'
    
    p2 = _plot_many_lines(ax, cad, feature_name, 'blue')    
    if mean:
        mn2 = _plot_mean_over_time(ax, cad, feature_name, 'navy' )
        p2[0].set_label(f'cAD (mv={mn2:.1f})')
    elif regress:
        sns.regplot(x="AGE", y=feature_name, data=cad, scatter=False,
                    line_kws={"color": 'navy',"linewidth": 10}, ax=ax,);
        p2[0].set_label(f'cAD')
    else:
        p2[0].set_label(f'cAD')
        
    
    plt.legend(fontsize=22)     
    ax.set_xticklabels(ax.get_xticks().astype(int), fontsize=25)
    ax.set_yticklabels(ax.get_yticks().astype(int), fontsize=25)

    ax.grid(which='major')
    ax.grid(which='minor',linestyle='--', alpha=0.5)
    #ax.legend()

    ax.set_title(title, fontsize=title_font_size, fontweight=title_font_weight)
    
    ax.set_xlabel(x_label, fontsize=x_label_size, weight='bold', labelpad=x_label_labelpad)
    ax.set_ylabel(y_label, fontsize=y_label_size, weight='bold', labelpad=y_label_labelpad)

    ax.grid(grid_on)  
