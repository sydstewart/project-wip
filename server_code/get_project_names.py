import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.secrets
import anvil.server


@anvil.server.callable
def get_project_names():

  projectlist =   list({(r['project_name']) for r in app_tables.sales_orders_stage_changes.search()})
  
  return projectlist