import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.secrets
import anvil.server
from Test import connect
import pandas as pd

@anvil.server.callable  
def get_stage_changes():
 
  conn = connect()
  #=============================================================================  
  # Load order changes 
  with conn.cursor() as curaudit:
    curaudit.execute(
      "Select sales_orders_audit.date_created as 'update_date', sales_orders.date_entered as 'date_entered', \
        sales_orders.date_modified, sales_orders.billing_account_id, \
      sales_orders_audit.before_value_string as 'stage_before', sales_orders_audit.after_value_string as 'stage_after', \
      sales_orders_audit.field_name, sales_orders.so_number as 'Order_No', sales_orders.so_stage, \
      sales_orders.amount_usdollar as 'GBP_Excl_Vat', \
      sales_orders.name  as 'name'\
      From sales_orders_audit Inner Join \
      sales_orders On sales_orders.id = sales_orders_audit.parent_id \
    Where sales_orders_audit.date_created > '2025-05-01' And \
    sales_orders_audit.after_value_string In ('Closed', 'On Hold') And \
    sales_orders_audit.field_name = 'so_stage' "  
    )
  records = curaudit.fetchall()
  number_of_records =len(records)
  print('No of changes',number_of_records)
  if number_of_records:
    dicts = [{'order_no': r['Order_No'], 'project_name':r['name'] ,'order_date':r['date_entered'],  'order_value':r['GBP_Excl_Vat'] , 'Update_Date':r['update_date'], \
              'Stage_before':r['stage_before'],'Stage_After':r['stage_after']} for r in records]
    # print(dicts)
  X = pd.DataFrame.from_dict(dicts)
  X['order_value_formated'] = X['order_value'].map("£{:,.0f}".format) 
  dicts =X.to_dict(orient='records')
  return dicts