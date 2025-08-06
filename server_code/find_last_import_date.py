import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.secrets
import anvil.server

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
@anvil.server.callable
def last_import_date():
  last_row_1 = app_tables.sales_orders_all.search(tables.order_by('order_date', ascending=False))[0]
  last_date = last_row_1['updated']
  return last_date
#
