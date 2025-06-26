from ._anvil_designer import pie_chartTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class pie_chart(pie_chartTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    piedata, fig = anvil.server.call('piechart')
    print('piedata', piedata)
    self.plot_1.figure =fig
    # Any code you write here will run before the form opens.
    self.text_box_1.text = piedata['Sum_on_hold'] + piedata['Sum_in_Progress']+ piedata['Sum_in_Waiting_to_Start']
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Work_in_Progress')
    pass
 