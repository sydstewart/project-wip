import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.secrets
import anvil.server

@anvil.server.callable
def sydtest():
  # orders = app_tables.sales_orders.search()
  # schema = datatable_schema("sales_orders")
  # dicts = schema.dump(orders, many=True)
  output = 'This is a Test'
  return output