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
      anvil.server.call('burndown')
      pass

