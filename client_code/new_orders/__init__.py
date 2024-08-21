from ._anvil_designer import new_ordersTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class new_orders(new_ordersTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    dicts = anvil.server.call('show_new_orders')
   
    self.repeating_panel_1.items = dicts
    # Any code you write here will run before the form opens.
