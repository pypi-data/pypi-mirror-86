
#from views import COL_PLACEHOLDER,pd_read
import pandas as pd, numpy as np

from collections import defaultdict
import os
import pickle
import argparse
import sys
import click
import json
import boto3
import io
import s3fs
from smart_open import open as s_open

import xlsxwriter
from itertools import product
import featuretools as ft
from ftools import ft_agg
from helper import *



ref_map = defaultdict(list)




def create_bin(df,col):
    bins = []

    for val in df[col]:
        if "<=" in val:
            val = int(val.strip("<="))
        elif ">=" in val:
            continue
            #val = int(val.strip(">="))
        else:
            val = int(val.split("-")[-1])
        bins.append(val)
    return bins

def my_cut(col,x, bins,
            lower_infinite=True, upper_infinite=True,
            **kwargs):
    r"""Wrapper around pandas cut() to create infinite lower/upper bounds with proper labeling.

    Takes all the same arguments as pandas cut(), plus two more.

    Args :
        lower_infinite (bool, optional) : set whether the lower bound is infinite
            Default is True. If true, and your first bin element is something like 20, the
            first bin label will be '<= 20' (depending on other cut() parameters)
        upper_infinite (bool, optional) : set whether the upper bound is infinite
            Default is True. If true, and your last bin element is something like 20, the
            first bin label will be '> 20' (depending on other cut() parameters)
        **kwargs : any standard pandas cut() labeled parameters

    Returns :
        out : same as pandas cut() return value
        bins : same as pandas cut() return value
    """

    # Quick passthru if no infinite bounds
    if not lower_infinite and not upper_infinite:
        return pd.cut(x, bins, **kwargs)

    # Setup
    num_labels      = len(bins) - 1
    include_lowest  = kwargs.get("include_lowest", False)
    right           = kwargs.get("right", True)

    # Prepend/Append infinities where indiciated
    bins_final = bins.copy()
    if upper_infinite:
        bins_final.insert(len(bins),float("inf"))
        num_labels += 1
    if lower_infinite:
        bins_final.insert(0,float("-inf"))
        num_labels += 1

    # Decide all boundary symbols based on traditional cut() parameters
    symbol_lower  = "<=" if include_lowest and right else "<"
    left_bracket  = "(" if right else "["
    right_bracket = "]" if right else ")"
    symbol_upper  = ">" if right else ">="

    # Inner function reused in multiple clauses for labeling
    def make_label(i, lb=left_bracket, rb=right_bracket):
        return "{0}{1}, {2}{3}".format(lb, bins_final[i], bins_final[i+1], rb)

    # Create custom labels
    labels=[]
    for i in range(0,num_labels):
        new_label = None

        if i == 0:
            if lower_infinite:
                new_label = "{0} {1}".format(symbol_lower, bins_final[i+1])
            elif include_lowest:
                new_label = make_label(i, lb="[")
            else:
                new_label = make_label(i)
        elif upper_infinite and i == (num_labels - 1):
            new_label = "{0} {1}".format(symbol_upper, bins_final[i])
        else:
            new_label = make_label(i)

        labels.append(new_label)
    ref_map[col]=labels
    # Pass thru to pandas cut()
    return pd.cut(x, bins_final, labels=labels, **kwargs)


def single_itr(fts:list,df):
    # fts like ['age','sp']
    itr_cols=[]
    itr_vals=[]
    for ft in fts:
        itr_cols.append(ft)
        if ft in ref_map:
            itr_vals.append(ref_map[ft])
        else:
            itr_vals.append(df[ft].unique().tolist())

    return itr_cols,itr_vals

def prod_itr(fts:list,df):
    # fts is like ['age|covergage','age|SP']
    # df should be the data in config['entities']
    # ref_map below is like {'SP':['Y','N']}
    itr_cols=[]
    itr_vals=[]
    for ft in fts:
        ft_used = ft.split('|')
        new_ft = '_'.join(ft_used)
        #itr_cols.append(new_ft)
        if new_ft not in df:
            df[new_ft]=df[ft_used[0]].astype(str)+"_"+df[ft_used[1]].astype(str) # generate new column concat with two others
        #unique_vals=[ref_map[f] if f in ref_map else df[f].unique().tolist() for f in ft_used] #get unique column values, check if in the reference table list
        #print(unique_vals)
        #itr_val = [x[0]+'_'+x[1] for x in list(product(unique_vals[0],unique_vals[1]))] #get the product values for new feature values
        #itr_vals.append(itr_val)
    #return itr_cols,itr_vals
    return df

def prepare_config(config):#path,config_name):
    #with s_open(os.path.join(path,'{}.pickle'.format(config_name)), 'rb') as handle:
    #    config = pickle.load(handle)


    #get data
    for i,entity in enumerate(config['entities']):
        print('name in confg:',entity['entity'])
        data = pd_read(entity['entity'],src='s3',sample=1000)
        config[entity['entity']]=data


    #map reference if have and interesting values


    # deal with reference first
    for pvt in config['pivotings']:
        if pvt['reference']!=COL_PLACEHOLDER[0]: #only accept for reference for one column; which means we only have 1 single or 1 prod feature for this time, i.e. len(fts)==0
            # get data from entities
            df_name = pvt['entity']
            df = config[df_name]
            # get features
            if 'column2' in pvt:
                print('has prod')
                fts = pvt['column1']+'|'+pvt['column2'] #get column name like 'age|coverage'
                df[fts]=df[pvt['column1']].astype(str)+"_"+df[pvt['column2']].astype(str) #get new column
            else:
                fts = pvt['column1']
            print('fts',fts)
            grp = pd_read(pvt['reference'])
            ref_type = pvt['ref_type']
            if ref_type=='range':
                #df_used = config['datas'][data_id]
                fe = grp.columns[0]
                bins = create_bin(grp,fe)
                print(bins)
                df[fts]=my_cut(fe,df[fts],bins,right=True,include_lowest=True)
                #reference.append(pvt
            else:
                maps = pd.Series(grp.iloc[:,1].values,index=grp.iloc[:,0]).rename(fts).to_dict()
                df.map(maps)
            '''
            # get interesting values
            if pvt['kind']=='two':
                itr_cols,itr_vals =prod_itr([fts],df)
                pvt['columns']=itr_cols
                pvt['values']=itr_vals
            else:
                itr_cols,itr_vals =single_itr([fts],df)
                pvt['columns']=itr_cols
                pvt['values']=itr_vals
            '''
    # get intereting values for others with no reference
    #reference={}
    for pvt in config['pivotings']:
        if pvt['reference']==COL_PLACEHOLDER[0]: #only accept for reference for one column; which means we only have 1 single or 1 prod feature for this time, i.e. len(fts)==0
            df_name = pvt['entity']
            #get data
            df = config[df_name]
            #get pivot feature list and get interesting values
            if pvt['kind']=='two':
                fts = [x[0]+'|'+x[1] for x in list(product(pvt['column1'].split('|'),pvt['column2'].split('|')))] #fts is like ['age|covergage','age|SP']
                #itr_cols,itr_vals =prod_itr(fts,df)
                df = prod_itr(fts,df)
                #pvt['columns']=itr_cols
                #pvt['values']=itr_vals
            '''
            else:

                fts = pvt['column1'].split('|') #like ['age','sp']
                print('iam in single',fts)
                itr_cols,itr_vals =single_itr(fts,df)
                pvt['columns']=itr_cols
                pvt['values']=itr_vals
                print('in single',(itr_cols,itr_vals))
            '''
    print('after itr, config is',config['pivotings'])

    return config

def get_features(config,schema_name,output_name):
    #config = prepare_config(path,config_name)
    config_prod = prepare_config(config)
    ent = ft_agg(config_prod)
    en_set,cutoff = ent.get_entityset()
    features_sv = ft.load_features(os.path.join(path,schema_name))

    df_out = ent.calculate_matrix(en_set,features_sv,cutoff)
    df_reset_idx = ent.recover_col(df_out,ent.target_idx_columns,ent.target_key)

    df_reset_idx.to_csv(os.path.join(path,output_name))
