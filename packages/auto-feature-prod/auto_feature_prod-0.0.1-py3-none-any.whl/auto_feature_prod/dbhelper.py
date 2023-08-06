import pymongo
from bson.objectid import ObjectId
import numpy as np
import pandas as pd
import sys
import os
DATABASE = "auto_ft_prod"

class DBHelper:

    def __init__(self):
        if "DB_PORT_27017_TCP_ADDR" in os.environ:
            HOSTIP = os.environ["DB_PORT_27017_TCP_ADDR"]
        else:
            HOSTIP = "localhost"
        self.client = pymongo.MongoClient(HOSTIP, 27017)
        #client = pymongo.MongoClient(os.environ["DB_PORT_27017_TCP_ADDR"], 27017)
        self.db = self.client[DATABASE]


    def add_mapping(self,entity_dev,entity_prod):
        return self.db.mappings.insert_one({'data_dev':entity_dev,"data_prod":entity_prod})

    def update_entities(self,df,frn_key):
        target = list(self.db.entities.find({'entity':df}))[-1]
        return self.db.entities.update_one(target, {"$set": {"frn_key":frn_key}})
    def delete_entities(self,table_id):
        self.db.entities.remove({"_id": ObjectId(table_id)})
    def delete_mappings(self,table_id):
        self.db.mappings.remove({"_id": ObjectId(table_id)})


    def add_pivotings(self,entity,column1,column2=[],reference=[],ref_type=[]):
        if not column2:
            return self.db.pivotings.insert_one({'entity':entity,'kind':'one','column1':column1,'reference':reference,'ref_type':ref_type})
        return self.db.pivotings.insert_one({'entity':entity,'kind':'two','column1':column1,'column2':column2,'reference':reference,'ref_type':ref_type})
    def delete_pivotings(self,table_id):
        self.db.pivotings.remove({"_id": ObjectId(table_id)})


    def add_features(self,features_init):
        for ft in features_init:
            self.db.features.insert_one({'features':ft})

    def delete_features(self,table_id):
        self.db.features.remove({"_id": ObjectId(table_id)})

    def delete_with_id(self,table_id,collection_name):
        self.db[collection_name].remove({"_id": ObjectId(table_id)})

    def add_ft_restore(self,table_id,collection_from,collection_to):
        ft=list(self.db[collection_from].find({"_id": ObjectId(table_id)},{"_id":0}))[0]['features']
        self.db[collection_to].insert_one({'_id': ObjectId(table_id),'features':ft})

    def delete_ft_restore(self,table_id):
        self.db.ft_restore.remove({"_id": ObjectId(table_id)})

    def get_params(self):
        return list(self.db.params.find().sort('_id',-1))[0]

    def add_updates(self,id_val,gr_val):
        return self.db.updates.insert_one({'id_val':id_val,'gr_val':gr_val})

    def get_updates(self):
        return list(self.db.updates.find())

    def get_col_map(self,file_name,col1,col2):
        col_used = list(self.db[file_name].find({},{'_id':0,col1: 1,col2:1 }))
        col_map = pd.DataFrame(col_used).set_index(col1).T.to_dict('records')
        return col_map[0]

    def add_table(self,file_name,df):
        #if file_name in self.db.list_collection_names():
        #    print('has already')
        #    return
        if file_name in self.db.list_collection_names():
            self.drop_table(file_name)
        db_table = self.db[file_name]
        #db_table_res = self.db[file_name+"_res"]
        params = self.get_params()
        # get the data with smaller size then save into DB to decrease further I/O time
        df = self.helper_agg(df,list([params['ft']]+[params['gr_ft']]),params['cnt_ft'],params['avg_ft'])
        #df_res = self.helper_agg(df,params['gr_ft'],params['cnt_ft']+['cnt'],params['avg_ft'],True)
        #print('df before insert',df)

        db_table.insert_many(df.to_dict('records'))

        # do a backup in order to reset
        if not file_name+'_record_ori' in self.db.list_collection_names():
            db_ori = self.db[file_name+'_record_ori']
            #db_cal = self.db[file_name+'_record_cal']
            #db_col = self.db[file_name+'_cols']
            db_ori.insert_many(df.to_dict('records'))
            #db_cal.insert_many(df_cal.to_dict('records'))
            #db_col.insert_one({'all_used_cols':all_used_cols,'res_used_cols':res_used_cols})
        #db_table_res.insert_many(df_res.to_dict('records'))

    def update_table(self,file_name,ft_val,gr_ft_val):
        db_table = self.db[file_name]
        #db_res = self.db[file_name+"_res"]
        params = self.get_params()

        '''
        #extract old values
        myquery = {params["ft"]:ft_val}
        find_doc = list(db_table.find(myquery))[0]
        ori_grp, ori_cnt_val, ori_avg_val = find_doc[params['gr_ft']],\
                                                [find_doc[f] for f in params['cnt_ft']],\
                                                [find_doc[f] for f in params['avg_ft']]
        '''
        #update new values
        db_table.update_one({params["ft"]: ft_val}, {"$set": {params["gr_ft"]:gr_ft_val}})

    def get_table_one(self,file_name):
        return list(self.db[file_name].find_one())

    def get_final(self,file_name):
        df_ori,df_res,_,_=self.get_table(file_name)
        return df_res,df_ori

    def get_table(self,file_name,withid=True):
        if withid:
            return list(self.db[file_name].find().sort("_id"))
        else:
            return list(self.db[file_name].find({},{'_id':0}))




    def drop_table(self,file_name):
        if file_name in self.db.list_collection_names():
            self.db[file_name].drop()
