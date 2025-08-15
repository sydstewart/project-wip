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
import statistics
from prepare_dataframe import prepare_pandas
from anvil.tables import app_tables
import numpy as np
from datetime import datetime, time , date , timedelta
from anvil_extras.serialisation import datatable_schema
 

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
  
@anvil.server.background_task
@anvil.tables.in_transaction
def daily_by_stats_trial():

  conn = connect()
  print(' starting sql')
  with conn.cursor() as cur:
    cur.execute(
      "Select sales_orders.name As name, sales_orders.date_entered As date_entered, \
                          sales_orders.prefix as prefix,\
                        sales_orders.so_number as so_no,\
                        CONCAT(sales_orders.prefix,sales_orders.so_number) As so_number, \
                        sales_orders.so_stage As so_stage, \
                        sales_orders.subtotal_usd AS Order_Value, \
                       sales_orders_cstm.workinprogresspercentcomplete_c AS workinprogresspercentcomplete_c,\
                      sales_orders_cstm.OrderCategory AS OrderCategory,\
                      sales_orders_cstm.applicationarea_c AS AppArea, \
                      sales_orders_cstm.partialinvoicedtotal_c AS partially_invoiced_total, \
                      sales_orders_cstm.Waiing_On AS waiting_on ,\
                      sales_orders_cstm.waitingNote AS waiting_note , \
                      sales_orders.so_number AS so_number,\
                      sales_orders.so_stage AS stage, \
                      users.user_name AS user_name, \
                      sales_orders_cstm.workinprogresspercentcomplete_c AS workinprogresspercentcomplete_c \
                      From sales_orders\
                      INNER JOIN `sales_orders_cstm` ON (`sales_orders`.`id` = `sales_orders_cstm`.`id_c`)\
                      LEFT JOIN `users` ON (`sales_orders`.`assigned_user_id` = `users`.`id`) \
                      WHERE sales_orders.so_number > 2823 AND \
                      sales_orders_cstm.OrderCategory NOT IN ('Maintenance')   ")
  #   # AND \
  #   # sales_orders.so_stage  NOT IN ('Closed', 'Cancelled', 'Complete')")  # ,'Complete' 2020-01-01 # Where sales_orders.date_entered > '2020-01-01' AND \
  records = cur.fetchall()
  number_of_records =len(records)
  print('No of projects',number_of_records)
  
  if number_of_records:
    dicts = [{'order_no': r['so_number'],'prefix':r['prefix'], 'so_no':r['so_no'],'project_name':r['name'] ,'order_date':r['date_entered'], 'order_category':r['OrderCategory'],'assigned_to':r['user_name'] , \
              'order_value':r['Order_Value'], 'percent_complete':r['workinprogresspercentcomplete_c'],'app_area':r['AppArea'] , 'stage':r['stage'],  \
              'partially_invoiced_total':r['partially_invoiced_total'],'waiting_on':r['waiting_on'],'waiting_note':r['waiting_note'],'so_number':r['so_number']} \
            for r in records]
    
  # To calculate new columns and None values to zero
  
  X = pd.DataFrame(dicts)
  X['percent_complete'] = X['percent_complete'].fillna(0)
  X['order_value'] = X['order_value'].fillna(0)
  X['work_to_do'] = (X['order_value'] * ((100 - (X['percent_complete']))/100))
  X['work_to_do']= X['work_to_do'].fillna(0)
  X['work_completed'] =(X['order_value'] * ((X['percent_complete'])/100))
  X['work_completed']= X['work_completed'].fillna(0)
  X['partially_invoiced_total'] = X['partially_invoiced_total'].fillna(0)
  X['invoiced_but_work_not_done'] = X['partially_invoiced_total'] - X['work_completed']
  X['invoiced_but_work_not_done'] = X['invoiced_but_work_not_done'].fillna(0)
  X['invoiced_but_work_not_done']= X['invoiced_but_work_not_done'].map("£{:,.0f}".format)

  X['work_to_do_formated']= X['work_to_do'].map("£{:,.0f}".format)
  X['work_completed_formated']= X['work_completed'].map("£{:,.0f}".format)
  X['order_value_formated']= X['order_value'].map("£{:,.0f}".format)
  X['partially_invoiced_total_formated']= X['partially_invoiced_total'].map("£{:,.0f}".format)

  # work ourt eklapsed days
  today = datetime.today() #.strftime('%Y-%m-%d')
  print('today', today)
  X['today']= today
  X['today']= pd.to_datetime(X.today,utc =True)
  # print(X['today'])
  X['order_date'] = pd.to_datetime(X.order_date,utc =True)
  # print('order date',X['order_date'] )
  X['days_elapsed'] = (X['today'] - X['order_date']).dt.days
  # print('elapsed',X['days_elapsed']  )

  # # Group the stages into categories
  workinprogress_stages =['Awaiting Sign-Off','Work In Progress - 4S', 'Pre-requisites in progress' ,'Ready for GoLive', 'Ready for UAT','Ready to Start','UAT WIP','Invoiced, still work to be completed']
  hold_stages = ['On Hold']
  waitingtostart_stage =  [ 'Order Approved', 'Order Submitted for Approval','Ordered']
  closed_stage =['Closed']
  complete_stage =['Complete']
  cancelled_stage = ['Cancelled']
  conditions = [
    X['stage'].isin(workinprogress_stages),
    X['stage'].isin(hold_stages),
    X['stage'].isin(waitingtostart_stage),
    X['stage'].isin(complete_stage),
    X['stage'].isin(closed_stage),
    X['stage'].isin(cancelled_stage) ]

  categories = ['Work in Progress','On Hold' ,'Waiting to Start', 'Closed','Cancelled']

# Use np.select() to create the new column
  X['Stage Group'] = np.select(conditions, categories, default='Unknown')


 

  dicts  = X.to_dict(orient='records')

  # delete all rows in the order table
  app_tables.sales_orders_all.delete_all_rows()
  # results = app_tables.sales_orders_all.search()
  # for row in results:
  #   row.delete()
  print('table deleted')
  # Receate the Order table
   
  for row in dicts:
    # print (row['A'], row['B'], row['C'])
    updated =  datetime.now()
    app_tables.sales_orders_all.add_row(**{'order_no':row['so_number'],'prefix':row['prefix'], 'so_no':row['so_no'],'project_name':row['project_name'], 'order_date':row['order_date'], \
                                           'order_category':row['order_category'],'assigned_to':row['assigned_to'] , \
                                           'order_value':row['order_value'], 'percent_complete':row['percent_complete'],'app_area':row['app_area'], \
                                           'stage':row['stage'], \
                                           'partially_invoiced_total':row['partially_invoiced_total'],'waiting_on':row['waiting_on'],\
                                           'waiting_note':row['waiting_note'],'so_number':row['so_number'], 'work_to_do':row['work_to_do'], 'invoiced_but_work_not_done':row['invoiced_but_work_not_done'], \
                                           'work_completed':row['work_completed'] ,'stage_group':row['Stage Group'], 'days_elapsed':row['days_elapsed'], \
                                            'work_to_do_formated': row['work_to_do_formated'],'work_completed_formated': row['work_completed_formated'], \
                                            'order_value_formated':row['order_value_formated'], 'partially_invoiced_total_formated':row['partially_invoiced_total_formated'], \
                                            'invoiced_but_work_not_done_formated':row['invoiced_but_work_not_done_formated'], })
  
  for row in app_tables.sales_orders_all.search():
        row['updated'] = updated
  print('table loaded')


    # print(dicts)
    