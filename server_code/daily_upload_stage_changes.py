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
def daily_update_stage_changes():

  conn = connect()

  with conn.cursor() as curaudit:
    curaudit.execute(
      "Select sales_orders.date_entered as 'date_entered', \
            sales_orders.date_modified, sales_orders.billing_account_id, \
          sales_orders_audit.before_value_string as 'stage_before', sales_orders_audit.after_value_string as 'stage_after', \
          sales_orders_audit.field_name, sales_orders.so_number as 'Order_No', sales_orders.so_stage, \
          sales_orders.amount_usdollar as 'GBP_Excl_Vat', \
          sales_orders_audit.date_created As Update_date, \
          users.first_name  As Updated_by, \
          sales_orders_cstm.OrderCategory as order_category, \
          users.user_name AS user_name, \
          sales_orders.name  as 'name'\
          From sales_orders Inner Join \
                  sales_orders_audit On sales_orders.id = sales_orders_audit.parent_id \
                  Inner Join \
                  sales_orders_cstm On sales_orders_cstm.id_c = sales_orders.id Inner Join \
                  users On sales_orders_audit.created_by = users.id Inner Join \
                  users users1 On sales_orders.created_by = users1.id \
        Where sales_orders_audit.date_created > '2024-07-01' And \
                  sales_orders_audit.after_value_string In ('Closed', 'On Hold') And \
                  sales_orders_audit.field_name = 'so_stage' AND \
                  sales_orders_cstm.OrderCategory NOT IN ('Maintenance') "
                    
      
    )
  
    records = curaudit.fetchall()
    number_of_records =len(records)
  print('No of changes',number_of_records)


 
  if number_of_records:
    dicts = [{'order_no': r['Order_No'], 'project_name':r['name'] ,'order_date':r['date_entered'],  'order_value':r['GBP_Excl_Vat'] , 'Update_Date':r['Update_date'], \
              'order_category':r['order_category'], 'Updated_by':r['Updated_by'], 'Stage_Before':r['stage_before'],'Stage_After':r['stage_after']} for r in records]
  print('dicts',dicts)

  X = pd.DataFrame(dicts)
  X['order_value'] = X['order_value'].fillna(0)
  X['order_value_formated']= X['order_value'].map("£{:,.0f}".format)

  dicts  = X.to_dict(orient='records')
  print('dicts',dicts)
  #delete all rows in the order table
  app_tables.sales_orders_stage_changes.delete_all_rows()
  # results = app_tables.sales_orders_all.search()
  # for row in results:
  #   row.delete()
  print('table deleted')
  
  for row in dicts:
  
      updated =  datetime.now()
      app_tables.sales_orders_stage_changes.add_row(**{'order_no':row['order_no'],'project_name':row['project_name'], 'order_date':row['order_date'],'order_value':row['order_value'], 'order_value_formated':row['order_value_formated'],\
                                                        'Update_Date':row['Update_Date'], 'order_category':row['order_category'], 'Updated_by':row['Updated_by'],'Stage_Before':row['Stage_Before'],'Stage_After':row['Stage_After']})                                         
                                                      
      print('row loaded')
      for row in app_tables.sales_orders_stage_changes.search():
        row['table_last_updated'] = updated
      print('table loaded')