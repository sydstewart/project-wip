from ._anvil_designer import burndown_recordsTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class burndown_records(burndown_recordsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
   self.Order_no_dropdown.items =  
   self.repeating_panel_2.items = app_tables.burndown.search()
    # Any code you write here will run before the form opens.

  def Order_no_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    self.repeating_panel_2.items = app_tables.burndown.search(order_no=self.Order_no_dropdown.selected_value)
    pass
