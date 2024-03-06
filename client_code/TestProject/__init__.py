from ._anvil_designer import TestProjectTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class TestProject(TestProjectTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

        # Set Form properties and Data Bindings.
    self.init_components(**properties)
    records = anvil.server.call('testprojects')
    # self.label_1.text = number_of_records
    self.repeating_panel_1.items = records
    # Any code you write here will run before the form opens.
