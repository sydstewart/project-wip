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

@anvil.server.callable
def extract_orders():
  """Launch a single stats background task."""
  task = anvil.server.launch_background_task('load_orders')
  return task

anvil.server.background_task
def load_orders():
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
                          sales_orders.prefix as prefix,\
                        sales_orders.so_number as so_no,\
                        CONCAT(sales_orders.prefix,sales_orders.so_number) As so_number, sales_orders.so_stage As so_stage, \
                        sales_orders.subtotal_usd AS Order_Value, \
                      sales_orders_cstm.workinprogresspercentcomplete_c AS workinprogresspercentcomplete_c,\
                      sales_orders_cstm.OrderCategory AS OrderCategory,\
                      sales_orders_cstm.applicationarea_c AS AppArea, \
                      sales_orders_cstm.partialinvoicedtotal_c AS partially_invoiced_total, \
                      sales_orders_cstm.Waiing_On AS waiting_on ,\
                      sales_orders_cstm.waitingNote AS waiting_note , \
                      If(sales_orders_cstm.applicationarea_c = 'Anticoagulation', 'Anticoagulation', 'Safety Monitoring and Misc') As AppGroup ,\
                      sales_orders.so_number AS so_number,\
                      sales_orders.so_stage AS stage, \
                      users.user_name AS assigned, \
                      sales_orders_cstm.workinprogresspercentcomplete_c AS workinprogresspercentcomplete_c \
                      From sales_orders\
                      INNER JOIN `sales_orders_cstm` ON (`sales_orders`.`id` = `sales_orders_cstm`.`id_c`)\
                      LEFT JOIN `users` ON (`sales_orders`.`assigned_user_id` = `users`.`id`) \
                      WHERE sales_orders.so_number > 0 AND \
                      sales_orders_cstm.OrderCategory NOT IN ('Maintenance')   ")
    # AND \
    # sales_orders.so_stage  NOT IN ('Closed', 'Cancelled', 'Complete')")  # ,'Complete' 2020-01-01 # Where sales_orders.date_entered > '2020-01-01' AND \
  records = cur.fetchall()
  number_of_records =len(records)
  print('No of projects',number_of_records)

  if number_of_records:
    dicts = [{'order_no': r['so_number'],'prefix':r['prefix'], 'so_no':r['so_no'],'project_name':r['name'] ,'order_date':r['date_entered'], 'order_category':r['OrderCategory'],'assigned_to':r['assigned'] , \
              'order_value':r['Order_Value'], 'percent_complete':r['workinprogresspercentcomplete_c'],'app_area':r['AppArea'] , 'stage':r['stage'], 'Appgroup':r['AppGroup'], \
              'partially_invoiced_total':r['partially_invoiced_total'],'waiting_on':r['waiting_on']} \
             for r in records]
    for row in dicts:
      app_tables.sales_orders_all.add_row(**row)
      print('adding row')
    # orders = app_tables.sales_orders .search()
