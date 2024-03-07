from ._anvil_designer import TestProjectTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import plotly.graph_objects as go

class TestProject(TestProjectTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

        # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # records,Total_Order_Value , Total_WIP_VaLUE , Average_WIP, number_of_records = anvil.server.call('testprojects')
    data = anvil.server.call('get_run_chart')
    line_plots = [
   
      go.Scatter(x=data['Date_entered'], y=data['delta_work'], name='Delta Work Completed', marker=dict(color='#e50000')),

    ]
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
    # self.plot_1.data = line_plots
    # self.plot_1.layout = layout
    # self.text_box_1.text = number_of_records
    # self.text_box_2.text = Total_Order_Value
    # self.text_box_3.text = Average_WIP
    # self.text_box_4.text = Total_WIP_VaLUE
    # self.repeating_panel_1.items = records
    # # self.repeating_panel_2.items =totals
    # Any code you write here will run before the form opens.
