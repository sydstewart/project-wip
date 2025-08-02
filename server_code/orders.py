import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.secrets
import anvil.server


@anvil.server.callable
def orders():
  orders = app_tables.sales_orders_all.search(q.fetch_only("order_no","project_name"))
  return orders
