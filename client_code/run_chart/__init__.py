from ._anvil_designer import run_chartTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, time , date , timedelta

class run_chart(run_chartTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    print('Syd')
    # records,Total_Order_Value , Total_WIP_VaLUE , Average_WIP, number_of_records = anvil.server.call('testprojects')
    line_plots = anvil.server.call('wip_run_chart')
    # projects = anvil.server.call('project_list')
    # self.project_drop_down.items = projects
    # Specify the layout
    # layout = {
    #   'title': 'Run Chart of Project Work Flow Rate created at ' + datetime.now().strftime('%d %B %Y %H:%M'),
    #   'yaxis': {'title': '£ Value'},
    #   'yaxis_range':[0,1500000],
    #    'autosize' : False, 
    #    'width': 700, 
    #    'height': 2400,
    #    'showlegend': True
    #   # 'xaxis': {
    #   #   'tickmode': 'array',
    #   #   'tickvals': list(range(27)),
    #   #   'ticktext': data['year'],
    #   # },
    # }
    print(line_plots)
    # # Make the multi-bar plot
    self.plot_1.figure = line_plots
    # self.plot_1.layout = layout


    # anvil.server.call('send_pdf_email')

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('send_pdf_email')

  def populate_Burndown_click(self, **event_args):
    """This method is called when the button is clicked"""
    dicts = anvil.server.call('burndown')
    # self.repeating_panel_1.items = dicts
    pass

  def indivindividual_projects_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('individual_projects')
    # dicts, projects = anvil.server.call('show_progress',self.project_drop_down.selected_value)

    # self.project_drop_down.items = projects
    # self.repeating_panel_1.items = dicts
    pass

  def project_drop_down_change(self, **event_args):
    """This method is called when an item is selected"""
    dicts = anvil.server.call('show_progress', self.project_drop_down.selected_value)

    layout = {
        'title': 'Run Chart of Project Work Flow Rate created at ' + datetime.now().strftime('%d %B %Y %H:%M') + ' for ' + self.project_drop_down.selected_value,
        'yaxis': {'title': 'Percentage complete'},
        # 'xaxis': {
        #   'tickmode': 'array',
        #   'tickvals': list(range(27)),
        #   'ticktext': data['year'],
        # },
      }
    line_plots = anvil.server.call('individual_chart',self.project_drop_down.selected_value)
    self.plot_2.layout = layout
    self.plot_2.data = line_plots
    # self.project_drop_down.items = projects
    self.repeating_panel_1.items = dicts
    pass
    pass

  def projects_by_manager_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('manager_projects')
    pass
