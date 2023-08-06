# to do list: 1.add infer schema function (df.infer_object().dtype)
#             2. make one datasets have more than one frn keys (need to consider DB's update_entities)
#             3. can't edit when the cell is empty (primitives)
#             4. add time_unit option
#             5. add groupby primitive (for transformatin like time_since_previous)
#             6. primitive_cp might be removed
#             7. time_unit ; cutoff
#             8. data type how to convert pandas datatype into featuretools.
#             9. sample (then need to make all the unique values selected in the intr values; then within ft_agg, do the samping, not from read data!)
# notes: cols not drop after concat can simply use set(frn)+set(idx)-set(time_index) (leave time index)
# notes: all the check, for "columns2" check, use if column2 in xxx; for 'reference'or'time_idx', use 'reference'==COL_PLACEHOLDER[0]
from flask import Flask,render_template,request,redirect,url_for,jsonify,make_response,jsonify,session
from flask_wtf import FlaskForm
from wtforms import SelectField,TextField,SubmitField,SelectMultipleField,widgets
from wtforms.validators import URL, DataRequired
import pandas as pd
import os
from itertools import product
import pyarrow as pa
import pyarrow.parquet as pq
import json
import datetime
import numpy as np
import sys
import boto3
import botocore
import pickle
from smart_open import open as s_open

import s3fs
import io
import xlsxwriter
from get_ft_features import get_features
from helper import *
#from grouping import app


import urllib.request
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
app.config['DEBUG']=True
app.config['SECRET_KEY']='secret'

url = "http://randomfactgenerator.net"
#bucket_name = ""
#config_name = ""
#folder_name = ""
#path = ""
#files =[]
#cols_lst = {}



data_files = files_no_data = get_file_names(bucket_name,folder_name)

files_no_data = get_file_names(bucket_name,folder_name,data=False)



# define form class
class Select2MultipleField(SelectMultipleField):
    def pre_validate(self, form):
        # Prevent "not a valid choice" error
        pass
    def process_formdata(self, valuelist):
        if valuelist:
            self.data = ",".join(valuelist)
        else:
            self.data = ""


class file_form(FlaskForm):
    configuration=  SelectField('Configuration',choices= [file for file in files_no_data])
    schema_name=  SelectField('Schema_name', choices=[file for file in files_no_data])
    output_name = TextField('Bucket', [DataRequired(),])
class data_form(FlaskForm):
    entity_dev = SelectField('In Dev',choices=[])
    entity_prod = SelectField('In Prod',choices=[])
    submit = SubmitField("Submit")



@app.route('/')
def home():
    if not session.get('logged_in'):
        f_form = file_form()
        return render_template('directory.html',f_form=f_form)
    return render_template('home.html', path=path,config_name=session['config_name'],\
                                        schema_name = session['schema_name'],output_name=session['output_name'])

@app.route('/directory', methods=['GET','POST'])
def directory():
    f_form=file_form()
    #session['files'] = get_file_names(bucket_name,folder_name,data=False)
    #print('FILES are',files_no_data)

    if request.method=="POST":
        session['config_name'] = f_form.configuration.data
        session['schema_name'] = f_form.schema_name.data
        out= f_form.output_name.data
        session['output_name']=out if out.endswith('.csv') or out.endswith('.xlsx') or out.endswith('.parquet') else out+'.csv'

        #print('b and pre',(bucket_name,pre))
        session['logged_in'] = True
    return home()#redirect(url_for('/',p_form=p_form))#home()

@app.route('/directory/<bucket>')
def get_directory(bucket):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)
    result = bucket.meta.client.list_objects(Bucket=bucket.name,Delimiter='/')
    folders = [o.get('Prefix') for o in result.get("CommonPrefixes")]
    return jsonify({"folders":folders})

@app.route('/re_directory')
def re_directory():
    session['logged_in']=False
    return render_template('re_directory.html')


@app.route('/data_selection',methods=["GET","POST"])
def data_selection():
    df_form = data_form()
    #print('session files',session['files'])
    # defaul cols values
    with s_open(os.path.join(path,session['config_name']), 'rb') as handle:
        config = pickle.load(handle)
    df_form.entity_dev.choices = [DEFAULT_SELECT]+[file for file in config['all_data']]
    df_form.entity_prod.choices = [DEFAULT_SELECT]+[file for file in data_files]

    # get user submit
    if request.method=="POST":
        entity_dev = df_form.entity_dev.data
        entity_prod = df_form.entity_prod.data

        DB.add_mapping(entity_dev,entity_prod)

    tables = DB.get_table('mappings')
    return render_template('data_selection.html', df_form=df_form, tables=tables)


@app.route('/col/<entity>')
def col(entity):
    if session.get(entity+'col'):
        cols = session[entity+'col']
    else:
        cols = get_col(entity,src='s3',bucket_name=session['bucket_name'],pre=session['folder_name'])
        session[entity+'col']=cols #as cache, since get_col takes time.
    return jsonify({"cols":cols})

@app.route("/mappings/deletetable")
def mappings_deletetable():
    tableid = request.args.get("tableid")
    DB.delete_mappings(tableid)
    return redirect(url_for('data_selection'))


@app.route('/success',methods=['GET','POST'])
def success():
    print('i am run wiht config name',session['config_name'])
    with s_open(os.path.join(path,session['config_name']), 'rb') as handle:
        config = pickle.load(handle)
    for entity in config['entities']:
        prod = list(DB.db['mappings'].find({'data_dev':entity['entity']},{"_id":0,"data_prod":1}))[0]['data_prod']
        entity['entity']=prod
    schema_name = session['schema_name']
    output_name = session['output_name']
    get_features(config,schema_name,output_name)
    s3 = boto3.resource('s3')
    try:
        s3.Object(bucket_name, os.path.join(folder_name,session['output_name'])).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            ex="Not Successfully"
    else:
        # The object does exist.
        ex="Successfully"
    return render_template('success.html',path=path,output_name=session['output_name'],ex=ex)





@app.route("/remove/<string:collection>")
def remove_collection(collection):


    DB.drop_table(collection)
    return '{} is removed from database'.format(collection)


@app.route("/remove/all")
def remove_all():
    #remove primitives
    DB.client.drop_database('auto_ft')
    return 'the database is removed'

@app.route('/run_wait')
def run_wait():
    content = urllib.request.urlopen(url).read()
    parsedHTML = BeautifulSoup(content,features="html.parser")
    tag = parsedHTML.find_all('div',{'id':'z'})[0]
    fact = re.search('<div id="z">(.+?)<br/>',str(tag))
    fact = fact.group(1)
    return render_template('run_wait.html',fact=fact)



def get_file_names(bucket_name,pre,data=True):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    #print('bucket and pre in s3 in get_file_name',(bucket_name,pre))

    s3_file_names = []
    for obj in bucket.objects.filter(Delimiter='/',Prefix=pre):
        f = obj.key.split('/')[-1]
        if f:
            s3_file_names.append(f)
    files = [file for file in s3_file_names if file.endswith(".csv") or file.endswith(".parquet")\
                                                or file.endswith(".xlsx")]
    if not data:
        files = [file for file in s3_file_names if not(file.endswith(".csv") or file.endswith(".parquet")\
                                                    or file.endswith(".xlsx"))]
    #print('fiels not data:',files)
    return files

def do_update(data):
    #data = json.loads(data)
    idx,edit_val,col_name,df_name = data['row_id'],data['edit'],data['col'],data['df_name']
    edit_cur_val_backup=DB.update_primitive(df_name,idx,col_name,edit_val)
    edit_cur_val_backup = json.dumps(edit_cur_val_backup)
    return edit_cur_val_backup

def get_col(file,src='s3',bucket_name=None,pre=None):

    if file==DEFAULT_SELECT:
        return [DEFAULT_SELECT]
    if src=='test':
        file_path = os.path.join(csvfolderpath, file)
    else:
        file_path = os.path.join(os.path.join(bucket_name,pre),file)
    #csvFile = os.path.join(csvfolderpath, file)
    if file.endswith('.csv'):
        table = pd.read_csv(file_path, nrows=10)
    if file.endswith('.xlsx'):
        s3_c = boto3.client('s3')
        file_path = os.path.join(pre,file)
        obj = s3_c.get_object(Bucket=bucket_name, Key=file_path)
        data = obj['Body'].read()
        table = pd.read_excel(io.BytesIO(data),nrows=10)
    if file.endswith('.parquet'):
        table = pd.read_parquet(file_path,  engine='pyarrow')
        table = table.head(10)
    cols = COL_PLACEHOLDER+table.columns.tolist()
    return cols

def post_value_with_fallback(key):
    if request.form.get(key):
        return request.form.get(key)
    return DEFAULT_SELECT

def post_values_with_fallback(key):
    if request.form.getlist(key):
        return request.form.getlist(key)
    return DEFAULT_SELECT

def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULT_SELECT

def get_values_with_fallback(key):
    if request.args.getlist(key):
        return request.args.getlist(key)
    if request.cookies.getlist(key):
        return request.cookies.getlist(key)
    return DEFAULT_SELECT


'''
@app.route('/', methods=['POST'])
def upload_files():
    for uploaded_file in request.files.getlist('file'):
        filename = uploaded_file.filename
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
                abort(400)
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        #uploaded_file.save(uploaded_file.filename)
    return redirect(url_for('index'))
@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)
@app.route('/Login')
def Login():
    return render_template('login.html')
'''
def get_table(user_input):
    dict={user_input:'hi'}
    return dict    #returns list of dictionaries, for example...
                   #dict = [{'name':'Joe','age':'25'},
                  #        {'name':'Mike','age':'20'},
                  #        {'name':'Chris','age':'29'}]


if __name__ == '__main__':
    app.run(port=8000,host='0.0.0.0')
