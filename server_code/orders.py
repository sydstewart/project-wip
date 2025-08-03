import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.secrets
import anvil.server
import pandas as pd

@anvil.server.callable
def orders(kwargs):

  if kwargs:
    orders = app_tables.sales_orders_all.search( **kwargs)
  else:
    orders = app_tables.sales_orders_all.search()
  # q.fetch_only("order_no","project_name","stage"
  # convert to datframe to calc new columns
  # X = pd.DataFrame.from_dict(orders)
  # X['work_to_do'] = (X['order_value'] * ((100 - (X['percent_complete']))/100))
  # # X['work_to_do'] = '£'+ str('{:,.2f}'.format(X['work_to_do'] ) )
  # orders  = X.to_dict(orient='records')
      
  # print('orders', orders)
  return orders
  # if partname:
  #       orders = app_tables.sales_orders_all.search(q.fetch_only("order_no","project_name","stage"), project_name= q.ilike('%' + partname +'%'))
  # elif partname and stagegroup :
  #     orders = app_tables.sales_orders_all.search(q.fetch_only("order_no","project_name","stage"), q.all_of(stage=q.any_of(*stages), project_name= q.ilike('%' + partname +'%')))
  # elif stagegroup :
  #    orders = app_tables.sales_orders_all.search(q.fetch_only("order_no","project_name","stage"), stage=q.any_of(*stages))
  # elif not partname and not stagegroup:
  #    orders = app_tables.sales_orders_all.search(q.fetch_only("order_no","project_name","stage"))
  # return orders
