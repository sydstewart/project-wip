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
  if dayofweek < 6:

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
  # print(dicts)
  dicts,dictspip, X_media,  pivotsyd_to_markdown= prepare_pandas(dicts, 0, None, None, None, None)
  X = pd.DataFrame.from_dict(dicts)
  #============================================================
  total_order_value = X['order_value'].sum()
  print( 'Total value Order', total_order_value )
  overall_percentage_completion =  X['percent_complete'].mean()
  print( 'Overall Percent Complete', overall_percentage_completion )
  print("========================================================")
  #=============================================================
  filtered_df = X[X['Stage Group'] == 'Projects on Hold']
  sum_of_onhold = filtered_df['order_value'].sum()
  count_of_onhold = filtered_df['order_value'].count() 
  on_hold_percentage_complete_on_hold  = filtered_df['percent_complete'].mean()
  work_completed_on_hold = sum_of_onhold * on_hold_percentage_complete_on_hold/100
  work_to_do_on_hold = sum_of_onhold - work_completed_on_hold 
  print('Total Projects on Hold', sum_of_onhold )
  print('on_hold_percentage_complete', on_hold_percentage_complete_on_hold)
  print('on_hold_work_to_do', work_to_do_on_hold )
  # print('Projects on Hold', filtered_df[['project_name','order_no']])
  print("========================================================")
  #==============================================================
  filtered_df = X[X['Stage Group'] == 'Project in Progress']
  sum_of_in_progress = filtered_df['order_value'].sum() 
  count_of_in_progress = filtered_df['order_value'].count() 
  percentage_complete_in_progress  = filtered_df['percent_complete'].mean()
  work_completed_in_progress= sum_of_in_progress * percentage_complete_in_progress/100
  work_to_do_in_progress = sum_of_in_progress  - work_completed_in_progress
  # print('Projects on Hold', filtered_df[['project_name','order_no']]) 
  # print('X',X)
  print( 'Total Projects in Progress', sum_of_in_progress  )
  print('in_progress_percentage_complete', percentage_complete_in_progress)
  print('in_progress_work_to_do', work_to_do_in_progress )
  print("========================================================")
  #==============================================================
  filtered_df = X[X['Stage Group'] == 'Project waiting to Start']
  sum_of_waiting_to_start = filtered_df['order_value'].sum() 
  count_of_waiting_to_start = filtered_df['order_value'].count() 
  percentage_complete_to_start  = filtered_df['percent_complete'].mean()
  work_completed_to_start= sum_of_waiting_to_start* percentage_complete_to_start/100
  work_to_do_to_start = sum_of_waiting_to_start  - work_completed_to_start
  print('Total Projects Waiting to Start', sum_of_waiting_to_start) 
  print('iwaiting_to_start_percentage_complete', percentage_complete_to_start )
  print('to_start_work_to_do',  work_to_do_to_start )
  # print('X',X)
  print("========================================================")
  #====================================================================
  total_value_of_projects = sum_of_waiting_to_start + sum_of_in_progress  + sum_of_onhold
  total_work_to_do = work_to_do_to_start + work_to_do_in_progress + work_to_do_on_hold
  print('total_value_of_projects adding three Stage Groups',total_value_of_projects )
  print('total_value_of_projects work to do',total_work_to_do )
  today = datetime.today()
 
  app_tables.stage_summary.add_row(Date_of_WIP = (today),  Sum_on_hold = round(float(sum_of_onhold),0), 
                                                           Sum_in_Progress = round(float(sum_of_in_progress ),0),
                                                           Sum_in_Waiting_to_Start = round(float(sum_of_waiting_to_start),0),
                                                           Total_Value_of_Projects = round(float(total_value_of_projects),0),
                                                           Percent_Completion_On_Hold = round(float(on_hold_percentage_complete_on_hold),1),
                                                           Percent_Completion_in_Progress = round(float(percentage_complete_in_progress),1),
                                                           Percent_Completion_to_start = round(float(percentage_complete_to_start),1),
                                                           Work_to_do_on_hold  = round(float(work_to_do_on_hold),0),
                                                           Work_to_do_in_Progress= round(float(work_to_do_in_progress),0),
                                                           Work_to_do_to_Start = round(float(work_to_do_to_start),0), 
                                                           Total_Work_To_Do =  round(float(total_work_to_do),0), 
                                                           Overall_Percent_Completion =  round(float(overall_percentage_completion),1),
                                                           Count_on_hold = count_of_onhold, 
                                                           Count_in_Progress = count_of_in_progress,
                                                           Count_of_waiting_to_start= count_of_waiting_to_start)
  