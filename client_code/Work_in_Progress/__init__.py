from ._anvil_designer import Work_in_ProgressTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, time , date , timedelta

class Work_in_Progress(Work_in_ProgressTemplate):
  def __init__(self, **properties):
     
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    print('Syd')
    # records, Total_Order_Value , Total_WIP_VaLUE , Average_WIP, number_of_records = anvil.server.call('testprojects')
#=============================================================================    
    line_plots = anvil.server.call('wip_run_chart')
 
    layout = {
      'title': 'Total Order Value and Work Still to be Done Value' + '<br>' + 'created at ' + datetime.now().strftime('%d %B %Y %H:%M'),
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
#============================================================================
    start_date = date(year= 2024, month= 7, day = 17)
    line_plots_1 = anvil.server.call('work_to_do_chart', start_date)
    layout_1 = {
      'title': 'Work Still to be Done Value created at ' + datetime.now().strftime('%d %B %Y %H:%M'),
      'yaxis': {'title': '£ Value'},
      'yaxis_range':[0,600,000],
       'autosize' : False, 
       'width': 700, 
       'height': 2400,
       'showlegend': True
     }
    self.plot_2.figure = line_plots_1
    self.plot_2.layout = layout_1
#===================================================================    
    line_plots_2 = anvil.server.call('orders_chart')
    layout_2 = {
      'title': 'Open Orders Value created at ' + datetime.now().strftime('%d %B %Y %H:%M'),
      'yaxis': {'title': '£ Value'},
      # 'yaxis_range':[0,600,000],
       'autosize' : False, 
       'width': 700, 
       'height': 2400,
       'showlegend': True
     }
    self.plot_3.figure = line_plots_2
    self.plot_3.layout = layout_2
#=======================================================================
    
    dataWIP = anvil.server.call('get_Daily_WIP')
    self.repeating_panel_1.items = dataWIP 

  def changes_list_button_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('new_orders')
      # dicts = anvil.server.call('get_changes')
      
      pass

  def run_chart_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Run_Chart')
    pass

  def projects_list_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    
    open_form('list_projects')
    pass

  def plot_2_click(self, points, **event_args):
    """This method is called when a data point is clicked."""
    pass

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.task = anvil.server.call('stats')
    # anvil.server.call('testprojects')
    
    pass

  def plot_3_click(self, points, **event_args):
    """This method is called when a data point is clicked."""
    pass

  def pivots_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('pivots')
    pass


