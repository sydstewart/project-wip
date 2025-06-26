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
def daily_by_stats():
  # ++++++++++++++++++++++++++++++++++++++
  dayofweek = datetime.today().weekday()
  print('Day of Week', datetime.today().weekday())
  # dayofweek = 5
  if dayofweek < 5:

     conn = connect()
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
                      Where sales_orders.date_entered > '2020-01-01' AND \
                      sales_orders_cstm.OrderCategory NOT IN ('Maintenance')         AND \
                      sales_orders.so_stage  NOT IN ('Closed', 'Cancelled', 'Complete')")  # ,'Complete' 2020-01-01
  records = cur.fetchall()
  number_of_records =len(records)
  print('No of projects',number_of_records)

  if number_of_records:
    dicts = [{'order_no': r['so_number'], 'project_name':r['name'] ,'order_date':r['date_entered'], 'order_category':r['OrderCategory'],'assigned_to':r['user_name'] , \
              'order_value':r['Order_Value'], 'percent_complete':r['workinprogresspercentcomplete_c'],'app_area':r['AppArea'] , 'stage':r['stage'], 'Appgroup':r['AppGroup'], \
              'partially_invoiced_total':r['partially_invoiced_total']} \
             for r in records]
  print(dicts)
  dicts,dictspip, X_media,  pivotsyd_to_markdown= prepare_pandas(dicts, 0, 100, None, None, None)
  X = pd.DataFrame.from_dict(dicts)
  #=============================================================
  filtered_df = X[X['Stage Group'] == 'Projects on Hold']
  sum_of_onhold = filtered_df['order_value'].sum()
  count_of_onhold = filtered_df['order_value'].count() 

  print('Projects on Hold', filtered_df[['project_name','order_no']])
  #==============================================================
  filtered_df = X[X['Stage Group'] == 'Project in Progress']
  sum_of_in_progress = filtered_df['order_value'].sum() 
  count_of_in_progress = filtered_df['order_value'].count() 
  print('Projects on Hold', filtered_df[['project_name','order_no']]) 
  print('X',X)

  #==============================================================
  filtered_df = X[X['Stage Group'] == 'Project waiting to Start']
  sum_of_waiting_to_start = filtered_df['order_value'].sum() 
  count_of_waiting_to_start = filtered_df['order_value'].count() 
  print('Projects Waiting to Start', filtered_df[['project_name','order_no']]) 
  print('X',X)
  #====================================================================
  total_value_of_projects = sum_of_waiting_to_start + sum_of_in_progress  + sum_of_onhold
  today = datetime.today()

  app_tables.stage_summary.add_row(Date_of_WIP = (today),  Sum_on_hold = round(float(sum_of_onhold),0), Sum_in_Progress = round(float(sum_of_in_progress ),0), Sum_in_Waiting_to_Start = round(float(sum_of_waiting_to_start),0),
                                  Total_Value_of_Projects = round(float(total_value_of_projects),0),
                                  Count_on_hold = count_of_onhold, Count_in_Progress = count_of_in_progress,
                                  Count_of_waiting_to_start= count_of_waiting_to_start)
  