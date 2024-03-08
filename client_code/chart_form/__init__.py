from ._anvil_designer import chart_formTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class chart_form(chart_formTemplate):
  def __init__(self, **properties):
   def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # records,Total_Order_Value , Total_WIP_VaLUE , Average_WIP, number_of_records = anvil.server.call('testprojects')
    line_plots = anvil.server.call('get_run_chart')
    
    # Specify the layout
    layout = {
      'title': 'Work Completion',
      'yaxis': {'title': 'Value'},
      # 'xaxis': {
      #   'tickmode': 'array',
      #   'tickvals': list(range(27)),
      #   'ticktext': data['year'],
      # },
    }

    # # Make the multi-bar plot
    self.plot_1.data = line_plots
    self.plot_1.layout = layout

   
    anvil.server.call('send_pdf_email')