from ._anvil_designer import project_listTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class project_list(project_listTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
   self.init_components(**properties)
#    self.repeating_panel_1.items = app_tables.projects.search(project_board = project_board, project_column=projectcolumn)