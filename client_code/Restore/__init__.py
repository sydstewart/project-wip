from ._anvil_designer import RestoreTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Restore(RestoreTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def upload_stage_translate_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call(upload_stagetranslate)
    pass

  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    anvil.server.call('store_data',file, self.select_table_dropdown.selected_value)
    pass