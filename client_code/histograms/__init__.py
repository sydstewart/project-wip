from ._anvil_designer import histogramsTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from datetime import datetime, time , date , timedelta
from anvil.tables import app_tables

class histograms(histogramsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    project_count, line_plots = anvil.server.call('show_histograms')
    layout = {
        'title': 'Histogram of Elapsed days created at ' + datetime.now().strftime('%d %B %Y %H:%M'),
        'yaxis': {'title': 'Percentage of projects', 'range' :[-5, 104]},
        'xaxis': {'x0': 0,'title': 'Days Elapsed Bins'}, 
     
      }
    self.plot_1.data = line_plots
    self.plot_1.layout = layout
    # Any code you write here will run before the form opens.
