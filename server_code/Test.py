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
  
@anvil.server.callable
def testprojects():
  
  conn = connect()
#=============================================================================  
  # Load Orders 
  with conn.cursor() as cur:
        cur.execute(
              "Select sales_orders.name As name, sales_orders.date_entered As date_entered, \
                sales_orders.so_number As so_number, sales_orders.so_stage As so_stage, \
                sales_orders.subtotal_usd AS Order_Value \
              From sales_orders\
              Where sales_orders.date_entered > '2024-01-01'"
                    )  
  records = cur.fetchall()
  return records
  # number_of_records = len(cur.fetchall())
  # # result = cur.fetchone()
  # # print(result) 
  # for r in cur.fetchall():
  #      dicts = [{'Sales_Order_No':r['so_number'],'Date_entered' : r['date_entered']}]
  # for d in dicts:
  #     app_tables.tableau.add_row(**d)
