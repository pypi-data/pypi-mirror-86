import re
from featuretools.primitives import make_agg_primitive,make_trans_primitive
from featuretools.variable_types import DateOfBirth,Text,Numeric,Categorical,Boolean,Index,DatetimeTimeIndex,Datetime,TimeIndex,Discrete,Ordinal
from scipy.stats import mode
from featuretools.primitives import TimeSinceLast,TimeSinceFirst,AvgTimeBetween,TimeSince,TimeSincePrevious
import numpy as np
from v_ft.custom_primitives import *
from v_ft import time_unit as tu
import time
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
from functools import reduce
import featuretools as ft
from helper import COL_PLACEHOLDER


# # featuretools class

import re
from featuretools.primitives import make_agg_primitive,make_trans_primitive
from featuretools.variable_types import DateOfBirth,Text,Numeric,Categorical,Boolean,Index,DatetimeTimeIndex,Datetime,TimeIndex,Discrete,Ordinal
from scipy.stats import mode
from featuretools.primitives import TimeSinceLast,TimeSinceFirst,AvgTimeBetween,TimeSince,TimeSincePrevious
import numpy as np
from v_ft.custom_primitives import *
from v_ft import time_unit as tu
import time
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
from functools import reduce
import featuretools as ft


# # featuretools class


class ft_agg(object):
    def __init__(self,config):
        self.config = config
        self.entities = config['entities']
        self.relations = config['relations']
        self.pivotings = config['pivotings']

        #self.agg_kpt = config['pmt_agg_kpt']
        #self.tfm_kpt = config['pmt_tfm_kpt']

        self.time_unit = 'year'#config['t_unit'] #year,month,day, with year as default


        # cutoff config
        self.if_cut = False #config['has_cutoff']

        self.cutoff = None # config['cutoff_date']


    def get_info(self,df_name,info_name):
            for entity in self.entities:
                if entity['entity']==df_name:
                    return entity[info_name]

    def add_r(self,es,one_df,one_col,many_df,many_col):
        es = es.add_relationship(ft.Relationship(es[one_df][one_col],es[many_df][many_col]))
        return es

    def gen_idx(self,df,cols_k=None,name_key=None,keep_cols=[]): #no need to drop since index only has count method (and for those concat keys, since the single column is not index, so count won't be used)
        # concat keys and drop related cols but keep those also used to do calculation (like c_loss_typ in IP)
        print('col are',df.columns)
        print('key is',cols_k)
        print('name key is',name_key)
        #col_drp = []
        if not name_key in df.columns and name_key and cols_k:
            print('generate key')
            df[name_key]=df[cols_k].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)
            #col_drp+=cols_k
        #print(col_drp)
        #col_drp = list(set(col_drp)-set(keep_cols))
       # print('col to drop',col_drp)
        #print('cols have',df.columns)
        #df = df.drop(columns=list(set(col_drp)))
        #print('after drop',df)
        return df

    def dup_chk(self,datasets):
        # use the key subset
        for data in datasets:
            data[2].drop_duplicates(subset=data[1], keep='first', inplace=True)

    def get_entityset(self):
        # get product features
        ###############################################
        #### self.datasets [[name,data,key],....]######
        ###############################################

        ###############################################
        #### generate keys and frn keysfor each table #
        ###############################################

        for entity in self.entities:
            # deal with time_idx
            if entity['time_idx']==COL_PLACEHOLDER[0]:
                entity['time_idx']=None
            # get target alias
            if entity['if_target']=='yes':
                self.target=entity['alias']
                self.target_idx_columns=entity['idx'].split('|') #used to recover concat index features (since index column will be in the output features' index)
                self.target_key = entity['alias']+'_key'
            if not '|' in entity['idx']:
                entity['key']=entity['idx']
                continue
            cols_key = entity['idx'].split('|') #key columns
            #self.ig_vars[entity['alias']]=cols_key #add the col that consitute the index and will be ignore during dfs
            data_cur = self.config[entity['entity']] #data
            idx_key = entity['alias']+'_key' #new key name
            entity['key']=idx_key #change name
            data_cur = self.gen_idx(data_cur,cols_key,idx_key) # no need to save back since it is mutable varaible


        for relation in self.relations:
            # get one and many alias
            one_alias = self.get_info(relation['one'],'alias')
            many_alias = self.get_info(relation['many'],'alias')
            # get key name
            frn_idx_key = many_alias+'_frn_'+one_alias
            #get many side data
            frn_data_cur = self.config[relation['many']]
            #get frn key columns
            frn_cols_key = relation['foreign_key'].split('|')
            #change parameters in reation
            relation['foreign_key'] = frn_idx_key
            relation['one']=one_alias
            relation['many']=many_alias
            relation['one_key']=relation['one']+'_key'
            frn_data_cur = self.gen_idx(frn_data_cur,frn_cols_key,frn_idx_key) # no need to save back since it is mutable varaible



        es = ft.EntitySet() #id='itli'
        # add entity
        ## check duplicate keys (should be avoided in the future)
        #self.dup_chk(new_datasets)


        ##################################
        # get cutoff date for processing#
        ##################################
        if self.if_cut:
            df_4_cutoff = new_datasets[-1][2]
            if not self.cutoff:
                self.cutoff = 'cutoff'
                df_4_cutoff[self.cutoff] =  pd.to_datetime('today')

            if self.config['use_cutoff_df']:
                print('i am in use cutoff dataset')
                cut_off_df=self.gen_idx(self.cutoff,self.cutoff_idx,new_datasets[-1][1])
                #cols_k=None,name_key=None,c
                # if use_cutoff_df, then set up cut_df and cut_df index keys
                #config['cut_df'] = None
                #config['cut_df_idx']=None
                #self.cutoff.rename(columns={self.cutoff_idx:'CaseNo'},inplace=True)
                #cut_off_df = self.cutoff[['CaseNo',self.cutoff]]
            else:
                if is_numeric_dtype(df_4_cutoff[self.cutoff]) or is_string_dtype(df_4_cutoff[self.cutoff]):
                    df_4_cutoff[self.cutoff]=pd.to_datetime(df_4_cutoff[self.cutoff],errors='coerce')
                cut_off_df = df_4_cutoff[[new_datasets[-1][1],self.cutoff]].drop_duplicates()

               #make cotoff time at target entity level and no duplicates
        else:
            cut_off_df=None


        for entity in self.entities:
            idx_used = entity['key']
            if idx_used:
                mk_idx=False
            else:
                idx_used=entity['alias']+'_key'
                mk_idx=True

            es.entity_from_dataframe(entity_id = entity['alias'],
                                     dataframe=self.config[entity['entity']],
                                     make_index=mk_idx,
                                     index=idx_used,
                                     time_index=entity['time_idx'])

        # add relations (one to many: one_df, one_key, many_df,many_frn)
        for relation in self.relations:
            es = self.add_r(es,relation['one'],relation['one_key'],relation['many'],relation['foreign_key'])

        return es,cut_off_df



    def calculate_matrix(self,es,features,cutoff):
        mtrx = ft.calculate_feature_matrix(features=features, entityset=es,cutoff_time=cutoff)
        return mtrx

    def recover_col(self,df,cols,key):
        df = df.reset_index()
        df[cols] = df[key].str.split("_",n=len(cols)-1,expand=True)
        df.drop(columns=key,inplace=True)
        return df

    def deal_colName(self,df):
        rep_names=[]
        for i in df.columns:
            rep_names.append(i.replace('(','<').replace(')','>').replace('=','@').replace('.','/').replace(',','/').replace(' ',''))
        df.columns=rep_names
        return df
