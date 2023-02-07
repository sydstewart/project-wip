from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from ..Searches import search_using_kwargs 
class Form1(Form1Template):

  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    boards =list({(r['project_board']) for r in app_tables.projects_stages.search(tables.order_by('project_board'))})
    self.boards_dropdown.items = boards
    if self.boards_dropdown.selected_value:
         self.repeating_panel_1.items = app_tables.projects_stages.search(tables.order_by('project_column'))
#          self.hits_textbox.text = len(app_tables.projects_stages.search())
# self.repeating_panel_teams.items = anvil.server.call('get_teams')
    

  def refresh_date_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('listprojects')
    
    pass

  def boards_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    search_using_kwargs(self)
    pass




