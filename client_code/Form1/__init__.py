from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

class Form1(Form1Template):

  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.repeating_panel_1.items = app_tables.projects_stages.search()
    self.text_box_1.text = len(app_tables.projects_stages.search())

  def refresh_date_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('listprojects')
    
    pass



