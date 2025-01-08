import anvil.email
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.secrets
import anvil.server
import pymysql
import anvil.tables.query as q
import anvil.media
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
# import anvil.pdf

from anvil.tables import app_tables

from datetime import datetime, time , date , timedelta



def connect():
  connection = pymysql.connect(host='51.141.236.29',
                               port=3306,
                               user='CRMReadOnly',
                               password=anvil.secrets.get_secret('Teamwork Pass'),
                               database = 'infoathand',
                               cursorclass=pymysql.cursors.DictCursor)
  if not connection:
     alert(' Connection down')
  return connection

conn = connect()
    #=============================================================================  
      # Load Orders 
@anvil.server.callable  
def get_orders(kwargs):
    with conn.cursor() as cur:
                cur.execute(
                      "Select sales_orders.name As name, sales_orders.date_entered As date_entered, \
                        CONCAT(sales_orders.prefix,sales_orders.so_number) As so_number, sales_orders.so_stage As so_stage, \
                        sales_orders.subtotal_usd AS Order_Value, \
                      sales_orders_cstm.workinprogresspercentcomplete_c AS workinprogresspercentcomplete_c,\
                      sales_orders_cstm.OrderCategory AS OrderCategory,\
                      sales_orders.so_number AS so_number,\
                      users.user_name AS user_name, \
                      sales_orders_cstm.workinprogresspercentcomplete_c AS workinprogresspercentcomplete_c \
                      From sales_orders\
                      INNER JOIN `sales_orders_cstm` ON (`sales_orders`.`id` = `sales_orders_cstm`.`id_c`)\
                      LEFT JOIN `users` ON (`sales_orders`.`assigned_user_id` = `users`.`id`) \
                      Where sales_orders.date_entered > '2020-01-01' AND \
                          sales_orders_cstm.OrderCategory NOT IN ('Maintenance') AND \
                          sales_orders.so_stage  NOT IN ('Closed', 'On Hold','Cancelled','Complete')"
                            )  
    records = cur.fetchall()
    number_of_records =len(records)
    print('No of projects',number_of_records)

    if number_of_records:
              dicts = [{'order_no': r['so_number'], 'project_name':r['name'] ,'order_date':r['date_entered'], 'order_category':r['OrderCategory'],'assigned_to':r['user_name'] , \
                      'order_value':r['Order_Value'], 'percent_complete':r['workinprogresspercentcomplete_c'] } \
                      for r in records]
    print(dicts)
    X = pd.DataFrame.from_dict(dicts)
    
    X['percent_complete'] = X['percent_complete'].fillna(0)
    filter = (kwargs)
    X =  X[filter]
        
  
  # print('before',X['percent_complete'])
    
    # X['percent_complete']= X['percent_complete'].astype(int)
   
    # if assigned_to and not category:
    #    filter = (X['assigned_to'] == assigned_to)
    #    X =  X[X['percent_complete'] > int(percent_complete) ]
    #    X =  X[filter]
    # elif category and not assigned_to:
    #       X =  X[X['percent_complete'] > int(percent_complete)]
    #       X =  X[X['order_category'] == category]
    # elif assigned_to and category:
    #       X =  X[X['percent_complete'] > int(percent_complete) ]
    #       filter = (X['assigned_to'] == assigned_to)
    #       X =  X[filter]
    #       X =  X[X['order_category'] == category]

    # print('after filter',X['percent_complete'])
    X['percent_complete'] = X['percent_complete'].map(str)
    dicts =X.to_dict(orient='records')
    X.to_csv('/tmp/X.csv') 
    X_media = anvil.media.from_file('/tmp/X.csv', 'text/csv', 'X')
    # media_object = anvil.pdf.render_form('list_projects')
    return dicts, X_media 

@anvil.server.callable
def create_pdf(dicts):
  pdf = anvil.pdf.render_form("list_projects_pdf", dicts, landscape =True)
  return pdf



@anvil.server.callable
def generate_pdf(pdf_info):
  # media_object = anvil.pdf.render_form('list_projects')
   print('pdf_info =', pdf_info)
   assigned_to =pdf_info['assigned to']
   percent_complete = pdf_info['percent_complete']
   category = pdf_info['category']
   with conn.cursor() as cur:
                cur.execute(
                      "Select sales_orders.name As name, sales_orders.date_entered As date_entered, \
                        CONCAT(sales_orders.prefix,sales_orders.so_number) As so_number, sales_orders.so_stage As so_stage, \
                        sales_orders.subtotal_usd AS Order_Value, \
                      sales_orders_cstm.workinprogresspercentcomplete_c AS workinprogresspercentcomplete_c,\
                      sales_orders_cstm.OrderCategory AS OrderCategory,\
                      sales_orders.so_number AS so_number,\
                      users.user_name AS user_name, \
                      sales_orders_cstm.workinprogresspercentcomplete_c AS workinprogresspercentcomplete_c \
                      From sales_orders\
                      INNER JOIN `sales_orders_cstm` ON (`sales_orders`.`id` = `sales_orders_cstm`.`id_c`)\
                      LEFT JOIN `users` ON (`sales_orders`.`assigned_user_id` = `users`.`id`) \
                      Where sales_orders.date_entered > '2020-01-01' AND \
                          sales_orders_cstm.OrderCategory NOT IN ('Maintenance') AND \
                          sales_orders.so_stage  NOT IN ('Closed', 'On Hold','Cancelled','Complete')"
                            )  
   records = cur.fetchall()
   number_of_records =len(records)
   print('No of projects',number_of_records)
  
   if number_of_records:
              dicts = [{'order_no': r['so_number'], 'project_name':r['name'] ,'order_date':r['date_entered'], 'order_category':r['OrderCategory'],'assigned_to':r['user_name'] , \
                      'order_value':r['Order_Value'], 'percent_complete':r['workinprogresspercentcomplete_c'] } \
                      for r in records]
   print(dicts)
   X = pd.DataFrame.from_dict(dicts)
    
   X['percent_complete'] = X['percent_complete'].fillna(0)
    # print('before',X['percent_complete'])
    
   X['percent_complete']= X['percent_complete'].astype(int)
    
   if assigned_to and not category:
        filter = (X['assigned_to'] == assigned_to)
        X =  X[X['percent_complete'] > int(percent_complete) ]
        X =  X[filter]
   elif category and not assigned_to:
          X =  X[X['percent_complete'] > int(percent_complete)]
          X =  X[X['order_category'] == category]
   elif assigned_to and category:
          X =  X[X['percent_complete'] > int(percent_complete) ]
          filter = (X['assigned_to'] == assigned_to)
          X =  X[filter]
          X =  X[X['order_category'] == category]
  
    # print('after filter',X['percent_complete'])
   X['percent_complete'] = X['percent_complete'].map(str)
   dicts =X.to_dict(orient='records')
   media_object = anvil.pdf.render_form('list_projects_pdf',dicts)
   return media_object 