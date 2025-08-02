import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.secrets
import anvil.server


@anvil.server.callable
def orders(kwargs):
#   stages = ['Awaiting Sign-Off','Work In Progress - 4S', 'Pre-requisites in progress' ,'Ready for GoLive', 'Ready for UAT','Ready to Start','UAT WIP', 'On Hold','Order Approved', 'Order Submitted for Approval','Ordered']
#   if stagegroup == 'Work in Progress':
#         stages = ['Awaiting Sign-Off','Work In Progress - 4S', 'Pre-requisites in progress' ,'Ready for GoLive', 'Ready for UAT','Ready to Start','UAT WIP']
#   elif stagegroup == 'On Hold':
#         stages = ['On Hold']
#   elif stagegroup == 'Waiting to Start':
#     stages = [ 'Order Approved', 'Order Submitted for Approval','Ordered']
#   elif stagegroup == 'Closed':
#      stages = ['Closed']

# # Setup search dictionary
#   kwargs ={}


# #Project Name
#   if partname:
#      kwargs['project_name'] =  q.ilike('%' + partname +'%')

# #stage
#   if stagegroup:
#     kwargs['stage'] =  q.any_of(*stages)  
  if kwargs:
    orders = app_tables.sales_orders_all.search(q.fetch_only("order_no","project_name","stage"), **kwargs)
  else:
    orders = app_tables.sales_orders_all.search(q.fetch_only("order_no","project_name","stage"))
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
