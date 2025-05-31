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
from datetime import datetime, time, date, timedelta
import numpy as np
from anvil.pdf import PDFRenderer
# import anvil.pdf

from anvil.tables import app_tables
from prepare_dataframe import prepare_pandas




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
def get_orders_for_pivots(percent_complete,hi_percentage, assigned_to, category, not_completed):
    print(' starting sql')
    with conn.cursor() as cur:
                cur.execute(
                      "Select sales_orders.name As name, sales_orders.date_entered As date_entered, \
                        CONCAT(sales_orders.prefix,sales_orders.so_number) As so_number, sales_orders.so_stage As so_stage, \
                        sales_orders.subtotal_usd AS Order_Value, \
                      sales_orders_cstm.workinprogresspercentcomplete_c AS workinprogresspercentcomplete_c,\
                      sales_orders_cstm.OrderCategory AS OrderCategory,\
                      sales_orders_cstm.applicationarea_c AS AppArea, \
                      sales_orders_cstm.partialinvoicedtotal_c AS partially_invoiced_total, \
                      If(sales_orders_cstm.applicationarea_c = 'Anticoagulation', 'Anticoagulation', 'Safety Monitoring and Misc') As AppGroup ,\
                      sales_orders.so_number AS so_number,\
                      sales_orders.so_stage AS stage, \
                      users.user_name AS user_name, \
                      sales_orders_cstm.workinprogresspercentcomplete_c AS workinprogresspercentcomplete_c \
                      From sales_orders\
                      INNER JOIN `sales_orders_cstm` ON (`sales_orders`.`id` = `sales_orders_cstm`.`id_c`)\
                      LEFT JOIN `users` ON (`sales_orders`.`assigned_user_id` = `users`.`id`) \
                      Where sales_orders.date_entered > '2020-03-01' AND \
                      sales_orders_cstm.OrderCategory NOT IN ('Maintenance')     ")    #AND \
                          # sales_orders.so_stage  NOT IN ('Closed', 'On Hold','Cancelled', 'Complete')")  # ,'Complete'
    records = cur.fetchall()
    number_of_records =len(records)
    print('No of projects',number_of_records)

    if number_of_records:
              dicts = [{'order_no': r['so_number'], 'project_name':r['name'] ,'order_date':r['date_entered'], 'order_category':r['OrderCategory'],'assigned_to':r['user_name'] , \
                      'order_value':r['Order_Value'], 'percent_complete':r['workinprogresspercentcomplete_c'],'app_area':r['AppArea'] , 'stage':r['stage'], 'Appgroup':r['AppGroup'], \
                        'partially_invoiced_total':r['partially_invoiced_total']} \
                      for r in records]
    print(dicts)
    dicts,stage_group_dicts, X_media,  pivotsyd_to_markdown= prepare_pandas(dicts,percent_complete,hi_percentage,assigned_to, category, not_completed)
#     X = pd.DataFrame.from_dict(dicts)
    return dicts, stage_group_dicts, X_media,  pivotsyd_to_markdown

  
@anvil.server.callable  
def get_orders_for_project_list(percent_complete, hi_percentage, assigned_to, category, not_completed):
    print(' starting sql')
    with conn.cursor() as cur:
                cur.execute(
                      "Select sales_orders.name As name, sales_orders.date_entered As date_entered, \
                        CONCAT(sales_orders.prefix,sales_orders.so_number) As so_number, sales_orders.so_stage As so_stage, \
                        sales_orders.subtotal_usd AS Order_Value, \
                      sales_orders_cstm.workinprogresspercentcomplete_c AS workinprogresspercentcomplete_c,\
                      sales_orders_cstm.OrderCategory AS OrderCategory,\
                      sales_orders_cstm.applicationarea_c AS AppArea, \
                      sales_orders_cstm.partialinvoicedtotal_c AS partially_invoiced_total, \
                      If(sales_orders_cstm.applicationarea_c = 'Anticoagulation', 'Anticoagulation', 'Safety Monitoring and Misc') As AppGroup ,\
                      sales_orders.so_number AS so_number,\
                      sales_orders.so_stage AS stage, \
                      users.user_name AS user_name, \
                      sales_orders_cstm.workinprogresspercentcomplete_c AS workinprogresspercentcomplete_c \
                      From sales_orders\
                      INNER JOIN `sales_orders_cstm` ON (`sales_orders`.`id` = `sales_orders_cstm`.`id_c`)\
                      LEFT JOIN `users` ON (`sales_orders`.`assigned_user_id` = `users`.`id`) \
                      Where sales_orders.date_entered > '2020-03-01' AND \
                       sales_orders_cstm.OrderCategory NOT IN ('Maintenance') AND sales_orders.so_stage  NOT IN ('Closed', 'On Hold','Cancelled', 'Complete')")  # ,'Complete'
    records = cur.fetchall()
    number_of_records =len(records)
    print('No of projects',number_of_records)

    if number_of_records:
              dicts = [{'order_no': r['so_number'], 'project_name':r['name'] ,'order_date':r['date_entered'], 'order_category':r['OrderCategory'],'assigned_to':r['user_name'] , \
                      'order_value':r['Order_Value'], 'percent_complete':r['workinprogresspercentcomplete_c'],'app_area':r['AppArea'] , 'stage':r['stage'], 'Appgroup':r['AppGroup'], \
                        'partially_invoiced_total':r['partially_invoiced_total']} \
                      for r in records]
    print(dicts)
    dicts, X_media,  pivotsyd_to_markdown= prepare_pandas(dicts,percent_complete, hi_percentage, assigned_to, category, not_completed)
    return dicts, X_media,  pivotsyd_to_markdown
#     print('Made dicts and dataframe')
#     X['order_value']= X['order_value'].map(float)
#     # X['cumulative_orders'] =  X['order_value'].cusum()
#     print('Cusum =', X['order_value'])
#     X['percent_complete'] = X['percent_complete'].fillna(0)
#     # print('before',X['percent_complete'])
    
#     X['percent_complete']= X['percent_complete'].astype(int)
    
#     X['partially_invoiced_total'] = X['partially_invoiced_total'].fillna(0)
#     X['Work Completed'] =X['order_value'] * X['percent_complete']/100
#     X['Work To Do'] =X['order_value'] * (100 - X['percent_complete'])/100
#     X['Invoiced but NOT completed amount'] = X['partially_invoiced_total'] - X['Work Completed']
#     X['Invoiced but NOT completed amount']= X['Invoiced but NOT completed amount'].map(float)
#     if  not_completed =='Yes':
#            X =  X[X['Invoiced but NOT completed amount'] > 0]
#     elif not_completed =='No':
#            X =  X[X['Invoiced but NOT completed amount'] <= 0]
#     if assigned_to and not category:
#        filter = (X['assigned_to'] == assigned_to)
#        X =  X[X['percent_complete'] > int(percent_complete) ]
#        X =  X[filter]
#     elif category and not assigned_to:
#           X =  X[X['percent_complete'] > int(percent_complete)]
#           X =  X[X['order_category'] == category]
#     elif assigned_to and category:
#           X =  X[X['percent_complete'] > int(percent_complete) ]
#           filter = (X['assigned_to'] == assigned_to)
#           X =  X[filter]
#           X =  X[X['order_category'] == category]
#     elif percent_complete and not category and not assigned_to:
#           X =  X[X['percent_complete'] > int(percent_complete)]
#     # print('after filter',X['percent_complete'])
#     X['percent_complete'] = X['percent_complete'].map(int)
  
#     X['order_value_formated'] = X['order_value'].map("£{:,.0f}".format)
#     X['partially_invoiced_total_formated'] = X['partially_invoiced_total'].map("£{:,.0f}".format)
#     X['Invoiced but NOT completed amount_formated'] = X['Invoiced but NOT completed amount'].map("£{:,.0f}".format)
  
#     today = datetime.today()
#     X['days_elapsed'] = (today - X['order_date']).dt.days
#     # print(X['days_elapsed']) =  X['days_elapsed'])
#     X['Work Completed'] =X['order_value'] * X['percent_complete']/100
#     X['Work Completed_formated'] = X['Work Completed'].map("£{:,.0f}".format)
#     X['Work To Do'] =X['order_value'] * (100 - X['percent_complete'])/100
#     X['Order_Value_Value_Add _per Elapsed_day'] = X['order_value']//X['days_elapsed']
#     X['Work_completed_Value_Add _per Elapsed_day'] = X['Work Completed']//X['days_elapsed']
#    # X['Value Left to Do'] = (100 - X['percent_complete']) 
#     X['Year'] = X['order_date'].dt.year
#     X['Month']= X['order_date'].dt.month
#     X['Day']= X['order_date'].dt.day
#     X['Year'] = X['Year'].map(int)
#     X['Month'] = X['Month'].map(int)
#     X['Year Num'] =  X['Year'].map(int)
#     X['Month Num'] = X['Month'].map(int)
# #     def categorize_year( year, month):
# #       if month <= 2 :
# #           return year - 1
# #       elif month > 2:
# #           return year

# # # Apply the function to the Age column using the apply() function
# #     X['Fin Year'] = X['Year  Num'].apply(categorize_year)
#     # Define the conditions and corresponding categories
#     conditions = [
#     X['Month Num'] <= 2 ,
#     (X['Month Num'] > 2) & (X['Month Num'] <= 12),
  
# ]

#     categories = [X['Year Num'] -1, X['Year Num']]

# # Use np.select() to create the new column
#     X['Fin Year'] = np.select(conditions, categories, default='Unknown') 

#     conditions = [
#     X['Month Num'] <= 2 ,
#     (X['Month Num'] > 2) & (X['Month Num'] <= 12),
  
# ]

#     categories = [X['Month Num'] + 10 , X['Month Num'] - 2 ]

# # Use np.select() to create the new column
#     X['Fin Month'] = np.select(conditions, categories, default='Unknown')


  
#     pivotsyd = pd.pivot_table(X, values = "order_value", index=['order_category'], aggfunc=('sum'), margins=True, margins_name='Total')
#     pivotsyd  = pivotsyd.fillna(0)
#     pivotsyd = pivotsyd.sort_values(by=['order_value'], ascending=False)
#     print(pivotsyd)
#     # fig = px.bar(pivotsyd, x='order_category', y='order_value')
#     pivotsyd['order_value']=pivotsyd['order_value'].apply('{:,}'.format)
#     print("")
#     pivotsyd_to_markdown = pivotsyd.to_markdown()
#     print(pivotsyd_to_markdown)
#     pd.set_option('display.max_columns', None)
#     print('pivotsyd',pivotsyd)
  
    
 
#     dicts =X.to_dict(orient='records')
#     X.to_csv('/tmp/X.csv') 
#     X_media = anvil.media.from_file('/tmp/X.csv', 'text/csv', 'X')
#     # media_object = anvil.pdf.render_form('list_projects')
    
  
@anvil.server.callable  
def get_all_orders():
    print(' starting sql')
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
                          sales_orders.so_stage  NOT IN ('Closed', 'Complete')")
                    
    records = cur.fetchall()
    number_of_records =len(records)
    print('No of projects',number_of_records)

    if number_of_records:
              dicts = [{'order_no': r['so_number'], 'project_name':r['name'] ,'order_date':r['date_entered'], 'order_category':r['OrderCategory'],'assigned_to':r['user_name'] , \
                      'order_value':r['Order_Value'], 'percent_complete':r['workinprogresspercentcomplete_c'] } \
                      for r in records]
    print(dicts)
    X = pd.DataFrame.from_dict(dicts)

    
    print('Made dicts and dataframe')
    X['order_value']= X['order_value'].map(float)
    # X['cumulative_orders'] =  X['order_value'].cusum()
    print('Cusum =', X['order_value'])
    X['percent_complete'] = X['percent_complete'].fillna(0)
    # print('before',X['percent_complete'])
    
    X['percent_complete']= X['percent_complete'].astype(int)
    # X['order_date'] = pd.to_datetime(X.order_date).dt.strftime('%d/%m/%Y')
    
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
    elif percent_complete and not category and not assigned_to:
          X =  X[X['percent_complete'] > int(percent_complete)]
    # print('after filter',X['percent_complete'])
    X['percent_complete'] = X['percent_complete'].map(int)
    X['order_value_formated'] = X['order_value'].map("£{:,.0f}".format)
    today = datetime.today()
    X['days_elapsed'] = (today - X['order_date']).dt.days
    print(X['days_elapsed'])
    X['Year'] = X['order_date'].dt.year
    X['Month']= X['order_date'].dt.month
    X['Day']= X['order_date'].dt.day
    X['Work Completed'] =X['order_value'] * X['percent_complete']/100
    X['Work To Do'] =X['order_value'] * (100 - X['percent_complete'])/100
    pivotsyd = pd.pivot_table(X, values = "order_value", index=['order_category'], aggfunc=('sum'), margins=True, margins_name='Total')
    pivotsyd  = pivotsyd.fillna(0)
    pivotsyd = pivotsyd.sort_values(by=['order_value'], ascending=False)
    print(pivotsyd)
    # fig = px.bar(pivotsyd, x='order_category', y='order_value')
    pivotsyd['order_value']=pivotsyd['order_value'].apply('{:,}'.format)
    print("")
    pivotsyd_to_markdown = pivotsyd.to_markdown()
    print(pivotsyd_to_markdown)
    pd.set_option('display.max_columns', None)
    print('pivotsyd',pivotsyd)
  
    
 
    dicts =X.to_dict(orient='records')
    X.to_csv('/tmp/X.csv') 
    X_media = anvil.media.from_file('/tmp/X.csv', 'text/csv', 'X')
    # media_object = anvil.pdf.render_form('list_projects')
    return dicts, X_media,  pivotsyd_to_markdown
@anvil.server.callable
def create_pdf(dicts, field_parameters):
  pdf = anvil.pdf.render_form("listpdf", dicts, field_parameters, landscape= True, page_size = 'A4')
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
   X['order_value_formated'] = X['order_value'].map("£{:,.0f}".format) 
   dicts =X.to_dict(orient='records')
   print(dicts)
   media_object = anvil.pdf.render_form('list_projects_pdf',dicts)
   return media_object 


