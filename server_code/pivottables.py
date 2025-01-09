import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.secrets
import anvil.server
import pandas as pd

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
@anvil.server.callable
def pivots(dicts):
      
      X = pd.DataFrame.from_dict(dicts)
      pivot3 =pd.pivot_table(X, values="order_value", index=['order_category'], columns = ('assigned_to'),aggfunc=('sum'), margins =True, margins_name='Total')
      print(pivot3)
      # return pivot3 
#
