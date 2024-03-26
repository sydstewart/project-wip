from ._anvil_designer import Email_chartTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, time , date , timedelta

class Email_chart(Email_chartTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        print('Syd')
        # records,Total_Order_Value , Total_WIP_VaLUE , Average_WIP, number_of_records = anvil.server.call('testprojects')
        line_plots = anvil.server.call('get_run_chart')
        projects = anvil.server.call('project_list')
        self.project_drop_down.items = projetc
        # Specify the layout
        layout = {
          'title': 'Run Chart of Project Work Flow Rate created at ' + datetime.now().strftime('%d %B %Y %H:%M'),
          'yaxis': {'title': '£ Value'},
          # 'xaxis': {
          #   'tickmode': 'array',
          #   'tickvals': list(range(27)),
          #   'ticktext': data['year'],
          # },
        }
    
        # # Make the multi-bar plot
        self.plot_1.data = line_plots
        self.plot_1.layout = layout
    
      
        # anvil.server.call('send_pdf_email')

    def button_1_click(self, **event_args):
      """This method is called when the button is clicked"""
      anvil.server.call('send_pdf_email')

    def populate_Burndown_click(self, **event_args):
      """This method is called when the button is clicked"""
      dicts = anvil.server.call('burndown')
      projects =list({(r['project_namea']) for r in app_tables.project_master.search(tables.order_by('project_name'))})
      self.project_drop_down.items = dicts['project_name']
      self.repeating_panel_1.items = dicts
      pass

    def button_2_click(self, **event_args):
      """This method is called when the button is clicked"""
      dicts, projects = anvil.server.call('show_progress',self.project_drop_down.selected_value)
      
      self.project_drop_down.items = projects
      self.repeating_panel_1.items = dicts
      pass

    def project_drop_down_change(self, **event_args):
      """This method is called when an item is selected"""
      dicts, projects = anvil.server.call('show_progress', self.project_drop_down.selected_value)
      
      self.project_drop_down.items = projects
      self.repeating_panel_1.items = dicts
      pass
      pass

