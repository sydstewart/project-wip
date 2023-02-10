import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import *
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from . import Module1
#
#    Module1.say_hello()
#

def show_projects(self):
    entry_copy = dict(list(self.item))
    # Open an alert displaying the 'ArticleEdit' Form
#     print(entry_copy)
      
    result = alert(content=AlertContent(item=entry_copy), title="Update Item", buttons=[], large=True)
    
    if result:
      anvil.server.call('update_change',self.item,entry_copy )

      self.refresh_data_bindings()   
      alert("Record Updated")
    else:
         alert(" Edit Cancelled")