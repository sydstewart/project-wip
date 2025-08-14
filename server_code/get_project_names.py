import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.secrets
import anvil.server


@anvil.server.callable
def get_project_names():

  projectlist =   list({(r['project_name']) for r in app_tables.sales_orders_stage_changes.search(tables.order_by('project_name'))})
  
  # list({(r['project_name']) for r in app_tables.sales_orders_stage_changes.search(tables.order_by('project_name'))})
  
  # [(str(row['project_name']), row) for row in app_tables.sales_orders_stage_changes.search(tables.order_by('project_name'))]
 
  # list( set([row['project_name'] for row in app_tables.sales_orders_stage_changes.search(tables.order_by('project_name'))] ))
 
  # [(str(row['application_area']), row) for row in app_tables.application_area.search(tables.order_by('application_area'))]
  return projectlist