import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.secrets
import anvil.server

@anvil.server.callable
def last_import_date_stages():
  last_row_1 = app_tables.sales_orders_stage_changes.search(tables.order_by('order_date', ascending=False))[0]
  last_date = last_row_1['table_last_updated']
  return last_date
