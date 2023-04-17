from ._anvil_designer import Form4Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..search_using_kwargs import search_using_kwargs
class Form4(Form4Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
#-------------------------------------------------------------------------
# Loading Dropdowns
#--------------------------------------------------------------------------------
    boards =list({(r['project_board']) for r in app_tables.projects.search(tables.order_by('project_board'))})
    self.board_dropdown.items = boards
    new_stages =list({(r['new_stages']['new_column']) for r in app_tables.projects.search(tables.order_by('project_column'))})
    self.New_stage_dropdown.items = new_stages
    
    self.repeating_panel_1.items = app_tables.projects.search()
    self.no_of_projects_found.text = len(self.repeating_panel_1.items )
    t = app_tables.last_date_refreshed.get(date_id =1 )
    self.last_refresh_date.text = t['last_date_refreshed']
    # Any code you write here will run before the form opens.

  def board_dropdown_change(self, **event_args):
    """This method is called when the selected values change"""
    search_using_kwargs(self)
    pass

  def New_stage_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    search_using_kwargs(self)
    pass

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.board_dropdown.selected = None
    self.New_stage_dropdown.selected_value = None
    self.exclude_archived_completed.checked= False
    self.repeating_panel_1.items = app_tables.projects.search()
    self.no_of_projects_found.text = len(self.repeating_panel_1.items )
    pass



  def exclude_archived_completed_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    search_using_kwargs(self)
    pass






