from ._anvil_designer import RowTemplate9Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...active_projects_by_board_stage_list import active_projects_by_board_stage_list

class RowTemplate9(RowTemplate9Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    

    # Any code you write here will run before the form opens.


  def projects_by_project_board_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    result = alert(content=active_projects_by_board_stage_list(self.item['project_board'],self.item['new_column']), title="Projects", buttons=[], large=True)
    pass


