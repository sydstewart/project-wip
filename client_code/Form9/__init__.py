from ._anvil_designer import Form9Template
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.email
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, time, date, timedelta

class Form9(Form9Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # line_plots = anvil.server.call('testform')

    # layout = {
    #   'title': 'Total Order Value and Work Still to be Done Value', #+ '<br>' + 'created at ' + datetime.now().strftime('%d %B %Y %H:%M'),
    #   'yaxis': {'title': '£ Value'},
    #   'yaxis_range':[0,500000],
    #   'autosize' : False, 
    #   'width': 700, 
    #   'height': 4400,
    #   'showlegend': True
    #   # 'xaxis': {
    #   #   'tickmode': 'array',
    #   #   'tickvals': list(range(27)),
    #   #   'ticktext': data['year'],
    #   # },
    # }

    # # # Make the multi-bar plot
    # self.plot_1.figure = line_plots
    # self.plot_1.layout = layout
    # # Any code you write here will run before the form opens.
