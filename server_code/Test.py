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
  
@anvil.server.background_task
def testprojects():
  
  conn = connect()
#=============================================================================  
  # Load Orders 
  with conn.cursor() as cur:
        cur.execute(
              "Select sales_orders.name As name, sales_orders.date_entered As date_entered, \
                CONCAT(sales_orders.prefix,sales_orders.so_number) As so_number, sales_orders.so_stage As so_stage, \
                sales_orders.subtotal_usd AS Order_Value, \
               sales_orders_cstm.workinprogresspercentcomplete_c AS workinprogresspercentcomplete_c,\
               sales_orders_cstm.OrderCategory AS OrderCategory,\
               sales_orders.so_number AS so_number\
              From sales_orders\
               INNER JOIN `sales_orders_cstm` ON (`sales_orders`.`id` = `sales_orders_cstm`.`id_c`)\
              Where sales_orders.date_entered > '2015-09-30' AND \
                  sales_orders_cstm.OrderCategory NOT IN ('Maintenance') AND \
                  sales_orders.so_stage  NOT IN ('Closed', 'On Hold','Cancelled','Work In Progress - 4S')"
                    )  
  records = cur.fetchall()
  number_of_records =len(records)

# calculate WIP
  with conn.cursor() as cur1:
        cur1.execute(
          "Select Sum(sales_orders.subtotal_usd) As Total_Order_Value,\
            Avg(sales_orders_cstm.workinprogresspercentcomplete_c) As Average_WIP,\
            Sum((sales_orders.subtotal_usd *  sales_orders_cstm.workinprogresspercentcomplete_c) / 100) As Total_WIP_VaLUE \
          From sales_orders \
              INNER JOIN `sales_orders_cstm` ON (`sales_orders`.`id` = `sales_orders_cstm`.`id_c`)\
              Where sales_orders.date_entered > '2015-09-30' AND \
                  sales_orders_cstm.OrderCategory NOT IN ('Maintenance') AND \
                  sales_orders.so_stage NOT IN ('Closed', 'On Hold', 'Cancelled','Work In Progress - 4S')"
        )
  for r in cur1.fetchall():
        Total_Order_Value =r['Total_Order_Value']
        Total_Order_Value = f"{Total_Order_Value  :.2f}"
        print('Total_Order_Value=',r['Total_Order_Value'])
        Average_WIP = (r['Average_WIP'])
        Average_WIP  = f"{Average_WIP :.2f}"
        print('Average_WIP=',Average_WIP )
        print('Total_WIP_VaLUE',r['Total_WIP_VaLUE'])
        Total_WIP_VaLUE = r['Total_WIP_VaLUE']
        Total_WIP_VaLUE = f"{Total_WIP_VaLUE :.2f}"
        Total_WIP_VaLUE = float(Total_WIP_VaLUE)
  totals = cur1.fetchall()
  today = datetime.today()
  last_row = app_tables.completed_work.search(tables.order_by('Date_entered', ascending=False))[0]
  last_reading = last_row['Order_Value_Completed']
  print('last_reading=', last_reading)
  delta = Total_WIP_VaLUE - float(last_reading)
  app_tables.completed_work.add_row(Order_Value_Completed=Total_WIP_VaLUE,Date_entered = today,delta_work= delta)
  totals = cur.fetchall()
  return records,Total_Order_Value , Total_WIP_VaLUE , Average_WIP, number_of_records


@anvil.server.callable
def get_run_chart():
   chart_data = app_tables.completed_work.search()
   return chart_data