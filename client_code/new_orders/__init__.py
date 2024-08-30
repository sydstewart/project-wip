from ._anvil_designer import new_ordersTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.media
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class new_orders(new_ordersTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    dicts, XMedia  = anvil.server.call('get_changes')
   
    self.repeating_panel_1.items = dicts
    # anvil.media.download(Y)
    # Any code you write here will run before the form opens.

  def check_box_1_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    
    if self.check_box_1.checked:
      self.repeating_panel_1.items = sorted(
        self.repeating_panel_1.items,
        key=lambda row: row["Update_Date"],
        reverse=True,
      )

    else:
        dicts = anvil.server.call('get_changes')
        self.repeating_panel_1.items = dicts

  # def button_1_click(self, **event_args):
  #   """This method is called when the button is clicked"""
  #   anvil.media.download(csv_file)
  #   pass

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    dicts , Xmedia = anvil.server.call('get_changes')
    download(Xmedia)
    pass


