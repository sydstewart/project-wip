from ._anvil_designer import Dev_board_formTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Dev_board_form(Dev_board_formTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    boards =list({(r['project_board']) for r in app_tables.projects_stages.search(tables.order_by('project_board'))})
    self.board_dropdown.items = boards
    records = app_tables.projects_stages.search(tables.order_by('project_column'),project_board= self.board_dropdown.selected_value)
#     self.plot_1.layout.title= self.board_dropdown.selected_value
#     self.plot_1.data = go.Bar(x=[r['project_column'] for r in records],
#                               y=[r['count'] for r in records])
    

  def board_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""

    records = app_tables.projects_stages.search(project_board= self.board_dropdown.selected_value)
    self.plot_1.layout.title= self.board_dropdown.selected_value
    if self.board_dropdown.selected_value == 'Development':
        self.plot_1.data = go.Bar(x=['Scheduled', 'In Progress','Awaiting Feedback', 'Done'],#r['project_column'] for r in records],
                              y=[r['count'] for r in records])
    pass

