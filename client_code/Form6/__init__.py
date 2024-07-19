from ._anvil_designer import Form6Template
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, time , date , timedelta

class Form6(Form6Template):
  def __init__(self, **properties):
     
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    print('Syd')
    # records,Total_Order_Value , Total_WIP_VaLUE , Average_WIP, number_of_records = anvil.server.call('testprojects')
    line_plots = anvil.server.call('wip_run_chart')
    # projects = anvil.server.call('project_list')
    # self.project_drop_down.items = projects
    # Specify the layout
    layout = {
      'title': 'Run Chart of Project Work Flow Rate created at ' + datetime.now().strftime('%d %B %Y %H:%M'),
      'yaxis': {'title': '£ Value'},
      'yaxis_range':[0,1500000],
       'autosize' : False, 
       'width': 700, 
       'height': 2400,
       'showlegend': True
      # 'xaxis': {
      #   'tickmode': 'array',
      #   'tickvals': list(range(27)),
      #   'ticktext': data['year'],
      # },
    }

    # # Make the multi-bar plot
    self.plot_1.figure = line_plots
    self.plot_1.layout = layout
