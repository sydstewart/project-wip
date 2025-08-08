import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.secrets
import anvil.server
import pandas as pd
from datetime import datetime, time , date , timedelta

@anvil.server.callable
def orders(kwargs):

  if kwargs:
    orders = app_tables.sales_orders_all.search( **kwargs)
  else:
    orders = app_tables.sales_orders_all.search(stage = q.not_('Closed'))
  # q.fetch_only("order_no","project_name","stage"
  print('orders', orders)
  # convert to datframe to calc new columns  if orderss are found
  if len(orders) > 0:
      X = pd.DataFrame.from_dict(orders)
      X['work_to_do'] = (X['order_value'] * ((100 - (X['percent_complete']))/100))
      X['work_to_do_formated']= X['work_to_do'].map("£{:,.0f}".format)
      X['order_value_formated']= X['order_value'].map("£{:,.0f}".format)
      X['partially_invoiced_total'] = X['partially_invoiced_total'].fillna(0)
      X['partially_invoiced_total_formated']= X['partially_invoiced_total'].map("£{:,.0f}".format)
      X['Invoiced_but_work_not_done'] = X['partially_invoiced_total'] - X['work_to_do']
      today = datetime.today() #.strftime('%Y-%m-%d')
    
      print('today', today)
      X['today']= today
      X['today']= pd.to_datetime(X.today,utc =True)
      # print(X['today'])
      X['order_date'] = pd.to_datetime(X.order_date,utc =True)
      # print('order date',X['order_date'] )
      X['days_elapsed'] = (X['today'] - X['order_date']).dt.days
      # print('elapsed',X['days_elapsed']  )
      
      orders  = X.to_dict(orient='records')
      
  # print('orders', orders)
  return orders

