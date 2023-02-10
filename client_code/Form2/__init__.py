from ._anvil_designer import Form2Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Form2(Form2Template):
  def __init__(self, project_board, project_column, **properties):
  
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.project_board_textbox.text = project_board
    self.project_column_textbox.text = project_column
    # Any code you write here will run before the form opens.
    print('Project board of line', project_board, project_column)
    self.repeating_panel_1.items = app_tables.projects.search(project_board=project_board, project_column=project_column)